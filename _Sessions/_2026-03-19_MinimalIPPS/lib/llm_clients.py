"""Anthropic and OpenAI API clients with custom retry logic."""
import logging
import random
import time

import anthropic
import openai

log = logging.getLogger(__name__)

# Retryable HTTP status codes for OpenAI
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}
MAX_RETRIES = 3


class APIError(Exception):
    """Raised when API call fails after all retries."""

    def __init__(self, message: str, retries: int, last_error: Exception):
        super().__init__(message)
        self.retries = retries
        self.last_error = last_error


class AnthropicClient:
    """Anthropic API client with prompt caching and retry logic."""

    def __init__(self, config: dict):
        model_config = config["models"]["mother"]
        self.model = model_config["model"]
        self.thinking = model_config.get("thinking", False)
        self.max_context = model_config.get("max_context", 200000)
        self.client = anthropic.Anthropic(
            timeout=config.get("api_timeout_seconds", 120),
            max_retries=0,
        )

    def call_with_cache(
        self, bundle: str, prompt: str, ttl: str = "1h"
    ) -> tuple[str, dict]:
        """Call Anthropic with cached bundle as system prompt.

        Args:
            bundle: Full file bundle to cache as system prompt
            prompt: User message prompt
            ttl: Cache Time To Live (default "1h")

        Returns:
            (response_text, usage_dict) tuple
        """
        messages = [{"role": "user", "content": prompt}]
        system = [
            {
                "type": "text",
                "text": bundle,
                "cache_control": {"type": "ephemeral"},
            }
        ]

        kwargs = {
            "model": self.model,
            "max_tokens": 16384,
            "system": system,
            "messages": messages,
        }
        if self.thinking:
            kwargs["thinking"] = {"type": "enabled", "budget_tokens": 10000}

        last_error = None
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = self.client.messages.create(**kwargs)
                # Extract text from content blocks (skip thinking blocks)
                text_parts = [
                    block.text
                    for block in response.content
                    if hasattr(block, "text")
                ]
                text = "\n".join(text_parts)
                usage = {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                    "cache_creation_input_tokens": getattr(
                        response.usage, "cache_creation_input_tokens", 0
                    ),
                    "cache_read_input_tokens": getattr(
                        response.usage, "cache_read_input_tokens", 0
                    ),
                }
                log.info(
                    "Anthropic call OK: model='%s', input=%d, output=%d, "
                    "cache_read=%d, cache_write=%d",
                    self.model,
                    usage["input_tokens"],
                    usage["output_tokens"],
                    usage["cache_read_input_tokens"],
                    usage["cache_creation_input_tokens"],
                )
                return text, usage

            except anthropic.RateLimitError as exc:
                last_error = exc
                retry_after = _parse_retry_after(exc)
                log.warning(
                    "Anthropic rate limit (attempt %d/%d), waiting %.1fs...",
                    attempt, MAX_RETRIES, retry_after,
                )
                time.sleep(retry_after)

            except (anthropic.APITimeoutError, anthropic.APIConnectionError) as exc:
                last_error = exc
                delay = _backoff_delay(attempt)
                log.warning(
                    "Anthropic timeout/connection error (attempt %d/%d), "
                    "retrying in %.1fs: %s",
                    attempt, MAX_RETRIES, delay, exc,
                )
                time.sleep(delay)

            except anthropic.APIError as exc:
                raise APIError(
                    f"Anthropic non-retryable error: {exc}",
                    retries=attempt,
                    last_error=exc,
                ) from exc

        raise APIError(
            f"Anthropic call failed after {MAX_RETRIES} retries: {last_error}",
            retries=MAX_RETRIES,
            last_error=last_error,
        )


class OpenAIClient:
    """OpenAI API client with retry logic for verification calls."""

    def __init__(self, config: dict):
        model_config = config["models"]["verification"]
        self.model = model_config["model"]
        self.client = openai.OpenAI(
            timeout=config.get("api_timeout_seconds", 120),
            max_retries=0,
        )

    def call(self, prompt: str, max_tokens: int = 500) -> tuple[str, dict]:
        """Call OpenAI Chat Completions API.

        Args:
            prompt: User message content
            max_tokens: Max output tokens (default 500, sufficient for score + feedback)

        Returns:
            (response_text, usage_dict) tuple
        """
        last_error = None
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                )
                text = response.choices[0].message.content
                usage = {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                }
                request_id = getattr(response, "_request_id", "unknown")
                log.info(
                    "OpenAI call OK: model='%s', prompt_tokens=%d, "
                    "completion_tokens=%d, request_id='%s'",
                    self.model,
                    usage["prompt_tokens"],
                    usage["completion_tokens"],
                    request_id,
                )
                return text, usage

            except openai.RateLimitError as exc:
                last_error = exc
                retry_after = _parse_retry_after(exc)
                log.warning(
                    "OpenAI rate limit (attempt %d/%d), waiting %.1fs...",
                    attempt, MAX_RETRIES, retry_after,
                )
                time.sleep(retry_after)

            except (openai.APITimeoutError, openai.APIConnectionError) as exc:
                last_error = exc
                delay = _backoff_delay(attempt)
                log.warning(
                    "OpenAI timeout/connection error (attempt %d/%d), "
                    "retrying in %.1fs: %s",
                    attempt, MAX_RETRIES, delay, exc,
                )
                time.sleep(delay)

            except openai.APIStatusError as exc:
                if exc.status_code in RETRYABLE_STATUS_CODES:
                    last_error = exc
                    delay = _backoff_delay(attempt)
                    log.warning(
                        "OpenAI retryable error %d (attempt %d/%d), "
                        "retrying in %.1fs: %s",
                        exc.status_code, attempt, MAX_RETRIES, delay, exc,
                    )
                    time.sleep(delay)
                else:
                    raise APIError(
                        f"OpenAI non-retryable error ({exc.status_code}): {exc}",
                        retries=attempt,
                        last_error=exc,
                    ) from exc

        raise APIError(
            f"OpenAI call failed after {MAX_RETRIES} retries: {last_error}",
            retries=MAX_RETRIES,
            last_error=last_error,
        )


def _backoff_delay(attempt: int) -> float:
    """Exponential backoff with jitter: base * 2^(attempt-1) * (1 + random(0, 0.5))."""
    base = 2.0
    delay = base * (2 ** (attempt - 1))
    jitter = delay * random.uniform(0, 0.5)
    return delay + jitter


def _parse_retry_after(exc: Exception) -> float:
    """Extract Retry-After header value from exception, default to 5s."""
    if hasattr(exc, "response") and exc.response is not None:
        retry_after = exc.response.headers.get("retry-after")
        if retry_after:
            try:
                return float(retry_after)
            except (ValueError, TypeError):
                pass
    return 5.0
