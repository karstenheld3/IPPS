"""Anthropic Computer Use provider."""
import os
import time
from typing import Dict, Any, List, Optional

class AnthropicProvider:
    """Provider for Anthropic Computer Use API."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-sonnet-4-5",
        max_tokens: int = 1024,
        display_width: int = 1568,
        display_height: int = 980,
        timeout: float = 60.0,
        max_retries: int = 2,
    ):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.model = model
        self.max_tokens = max_tokens
        self.display_width = display_width
        self.display_height = display_height
        self.timeout = timeout
        self.max_retries = max_retries
        self._client = None
        
        self.tool_version = "computer_20250124"
        self.beta_flag = "computer-use-2025-01-24"
    
    def _get_client(self):
        if self._client is None:
            import anthropic
            self._client = anthropic.Anthropic(
                api_key=self.api_key,
                timeout=self.timeout,
                max_retries=self.max_retries,
            )
        return self._client
    
    def _build_tools(self) -> List[Dict[str, Any]]:
        """Build tool definitions for the API request."""
        return [
            {
                "type": self.tool_version,
                "name": "computer",
                "display_width_px": self.display_width,
                "display_height_px": self.display_height,
                "display_number": 1,
            }
        ]
    
    def _build_image_content(self, base64_image: str, media_type: str = "image/jpeg") -> Dict[str, Any]:
        """Build image content block for API request."""
        return {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": media_type,
                "data": base64_image,
            }
        }
    
    def send_message(
        self,
        messages: List[Dict[str, Any]],
        system_prompt: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Send message to Anthropic API.
        
        Args:
            messages: Conversation messages
            system_prompt: Optional system prompt
            
        Returns:
            API response with content blocks
        """
        client = self._get_client()
        
        kwargs = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "tools": self._build_tools(),
            "messages": messages,
            "betas": [self.beta_flag],
        }
        
        if system_prompt:
            kwargs["system"] = system_prompt
        
        start = time.perf_counter()
        response = client.beta.messages.create(**kwargs)
        elapsed_ms = (time.perf_counter() - start) * 1000
        
        return {
            "id": response.id,
            "content": response.content,
            "stop_reason": response.stop_reason,
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
            },
            "latency_ms": round(elapsed_ms, 2),
        }
    
    def create_user_message(
        self,
        text: str,
        screenshot_base64: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a user message with optional screenshot.
        
        Args:
            text: User text prompt
            screenshot_base64: Optional base64-encoded screenshot
            
        Returns:
            Message dict ready for API
        """
        content = []
        
        if screenshot_base64:
            content.append(self._build_image_content(screenshot_base64))
        
        content.append({"type": "text", "text": text})
        
        return {"role": "user", "content": content}
    
    def create_tool_result(
        self,
        tool_use_id: str,
        screenshot_base64: Optional[str] = None,
        error: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a tool result message.
        
        Args:
            tool_use_id: ID from the tool_use block
            screenshot_base64: Screenshot after action execution
            error: Error message if action failed
            
        Returns:
            Tool result message dict
        """
        content = []
        
        if error:
            content.append({"type": "text", "text": f"Error: {error}"})
        elif screenshot_base64:
            content.append(self._build_image_content(screenshot_base64))
        
        return {
            "type": "tool_result",
            "tool_use_id": tool_use_id,
            "content": content if content else [{"type": "text", "text": "Action completed"}],
        }
    
    def extract_actions(self, response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract tool_use blocks from response.
        
        Args:
            response: API response
            
        Returns:
            List of tool_use blocks with id, name, input
        """
        actions = []
        for block in response.get("content", []):
            if hasattr(block, "type") and block.type == "tool_use":
                actions.append({
                    "id": block.id,
                    "name": block.name,
                    "input": block.input,
                })
            elif isinstance(block, dict) and block.get("type") == "tool_use":
                actions.append({
                    "id": block["id"],
                    "name": block["name"],
                    "input": block["input"],
                })
        return actions
    
    def extract_text(self, response: Dict[str, Any]) -> str:
        """Extract text content from response.
        
        Args:
            response: API response
            
        Returns:
            Concatenated text from all text blocks
        """
        texts = []
        for block in response.get("content", []):
            if hasattr(block, "type") and block.type == "text":
                texts.append(block.text)
            elif isinstance(block, dict) and block.get("type") == "text":
                texts.append(block["text"])
        return "\n".join(texts)
    
    def is_complete(self, response: Dict[str, Any]) -> bool:
        """Check if the response indicates task completion.
        
        Returns True if no tool_use blocks (model finished) or stop_reason is end_turn.
        """
        actions = self.extract_actions(response)
        if not actions:
            return True
        return response.get("stop_reason") == "end_turn" and not actions
