"""Step 5: Generate compression and evaluation prompts per file type (FR-05)."""
import json
import logging
from pathlib import Path

log = logging.getLogger(__name__)


def generate_compression_prompts(
    client,
    bundle: str,
    strategy: str,
    file_types: list[str],
    prompt_template: str,
) -> dict:
    """Call Mother to generate transform + eval prompt pairs per file type.

    Args:
        client: LLMClient instance (Anthropic)
        bundle: Full file bundle content (cached)
        strategy: Content of _03_FILE_COMPRESSION_STRATEGY.md
        file_types: List of file type names from config file_type_map values
        prompt_template: Content of s5_generate_prompts.md

    Returns:
        Dict mapping type name to {"transform": str, "eval": str}
    """
    types_list = "\n".join(f"- {t}" for t in file_types)
    prompt = (
        f"{prompt_template}\n\n"
        f"## Compression Strategy\n\n{strategy}\n\n"
    ).replace("{file_types_list}", types_list)

    result = client.call_with_cache(bundle, prompt)
    text, usage = result["text"], result["usage"]
    log.info(
        "Generated prompts for %d file types (%d output tokens)",
        len(file_types), usage["output_tokens"],
    )

    # Parse JSON response - try to extract JSON block from response
    prompts = _parse_prompts_response(text, file_types)
    return prompts


def _parse_prompts_response(text: str, file_types: list[str]) -> dict:
    """Parse Mother's response into prompt dict. Handles JSON in code blocks."""
    # Try direct JSON parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try extracting JSON from code block
    import re
    json_match = re.search(r"```(?:json)?\s*\n(.*?)\n```", text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass

    # Fallback: create placeholder prompts
    log.warning("Could not parse prompt JSON from Mother response, using placeholders")
    result = {}
    for ft in file_types:
        result[ft] = {
            "transform": f"Compress this {ft} file. Keep all functional content. Remove verbose examples and redundant explanations.",
            "eval": f"Score this compressed {ft} file 1-5. 5=all content preserved with good reduction. 1=critical content missing.",
        }
    if "compress_other" not in result:
        result["compress_other"] = {
            "transform": "Compress this file. Keep all functional content. Remove verbose examples and redundant explanations.",
            "eval": "Score this compressed file 1-5. 5=all content preserved with good reduction. 1=critical content missing.",
        }
    return result


def save_prompts(prompts: dict, transform_dir: Path, eval_dir: Path) -> None:
    """Write prompt pairs to transform/ and eval/ directories.

    Args:
        prompts: Dict from generate_compression_prompts
        transform_dir: Directory for transform prompts
        eval_dir: Directory for eval prompts
    """
    transform_dir.mkdir(parents=True, exist_ok=True)
    eval_dir.mkdir(parents=True, exist_ok=True)

    for type_name, pair in prompts.items():
        transform_path = transform_dir / f"{type_name}.md"
        eval_path = eval_dir / f"{type_name}.md"
        transform_path.write_text(pair["transform"], encoding="utf-8")
        eval_path.write_text(pair["eval"], encoding="utf-8")

    log.info(
        "Saved %d prompt pairs to '%s' and '%s'",
        len(prompts), transform_dir, eval_dir,
    )
