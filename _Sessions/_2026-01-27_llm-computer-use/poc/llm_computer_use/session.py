"""Agent session management for LLM computer use."""
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum

from .screen_capture import ScreenCapture
from .actions import Action, ActionResult, ActionType, execute_action, parse_anthropic_action, is_high_risk
from .providers.anthropic_provider import AnthropicProvider

class SessionStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    MAX_ITERATIONS = "max_iterations_reached"

@dataclass
class AgentSession:
    """Manages an automation session with the LLM."""
    
    task_prompt: str
    max_iterations: int = 10
    dry_run: bool = True
    model: str = "claude-sonnet-4-5"
    
    session_id: str = field(default_factory=lambda: datetime.now().strftime("%Y%m%d_%H%M%S"))
    status: SessionStatus = SessionStatus.PENDING
    current_iteration: int = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_api_latency_ms: float = 0.0
    start_time: datetime = field(default=None)
    end_time: datetime = field(default=None)
    actions_log: List[Dict[str, Any]] = field(default_factory=list)
    messages: List[Dict[str, Any]] = field(default_factory=list)
    
    _screen_capture: ScreenCapture = field(default=None, repr=False)
    _provider: AnthropicProvider = field(default=None, repr=False)
    _confirm_callback: Optional[Callable[[Action], bool]] = field(default=None, repr=False)
    
    def __post_init__(self):
        if self._screen_capture is None:
            self._screen_capture = ScreenCapture()
        if self._provider is None:
            display_info = self._screen_capture.get_display_info()
            primary = display_info["monitors"][1] if len(display_info["monitors"]) > 1 else display_info["monitors"][0]
            self._provider = AnthropicProvider(
                model=self.model,
                display_width=min(primary["width"], 1568),
                display_height=min(primary["height"], 980),
            )
    
    def set_confirm_callback(self, callback: Callable[[Action], bool]):
        """Set callback for high-risk action confirmation."""
        self._confirm_callback = callback
    
    def _log_action(self, action: Action, result: ActionResult, screenshot_before: str = None, screenshot_after: str = None):
        """Log an executed action."""
        self.actions_log.append({
            "iteration": self.current_iteration,
            "timestamp": datetime.now().isoformat(),
            "action": {
                "type": action.action_type.value,
                "coordinate": action.coordinate,
                "text": action.text,
                "key": action.key,
            },
            "result": {
                "success": result.success,
                "error": result.error_message,
                "execution_ms": result.execution_time_ms,
            },
            "dry_run": self.dry_run,
        })
    
    def _capture_screenshot(self) -> Dict[str, Any]:
        """Capture screenshot for API."""
        return self._screen_capture.capture_for_api()
    
    def run(self, verbose: bool = True) -> Dict[str, Any]:
        """Run the automation session.
        
        Args:
            verbose: Print progress to console
            
        Returns:
            Session summary with status, actions, and token usage
        """
        self.status = SessionStatus.RUNNING
        self.start_time = datetime.now()
        
        if verbose:
            print(f"\n{'='*60}")
            print(f"Session {self.session_id} started")
            print(f"Task: {self.task_prompt[:80]}...")
            print(f"Max iterations: {self.max_iterations}")
            print(f"Dry run: {self.dry_run}")
            print(f"{'='*60}\n")
        
        screenshot = self._capture_screenshot()
        initial_message = self._provider.create_user_message(
            text=self.task_prompt,
            screenshot_base64=screenshot["base64"],
        )
        self.messages.append(initial_message)
        
        while self.current_iteration < self.max_iterations:
            self.current_iteration += 1
            
            if verbose:
                print(f"\n--- Iteration {self.current_iteration}/{self.max_iterations} ---")
            
            try:
                response = self._provider.send_message(self.messages)
            except Exception as e:
                if verbose:
                    print(f"API Error: {e}")
                self.status = SessionStatus.FAILED
                return self._get_summary(error=str(e))
            
            self.total_input_tokens += response["usage"]["input_tokens"]
            self.total_output_tokens += response["usage"]["output_tokens"]
            self.total_api_latency_ms += response.get("latency_ms", 0)
            
            text_response = self._provider.extract_text(response)
            if text_response and verbose:
                print(f"Model: {text_response[:200]}...")
            
            actions = self._provider.extract_actions(response)
            
            if not actions:
                if verbose:
                    print("No actions requested - task complete")
                self.status = SessionStatus.COMPLETED
                return self._get_summary()
            
            self.messages.append({"role": "assistant", "content": response["content"]})
            
            tool_results = []
            for action_data in actions:
                action = parse_anthropic_action(action_data["input"])
                
                if verbose:
                    print(f"Action: {action.action_type.value}", end="")
                    if action.coordinate:
                        print(f" at {action.coordinate}", end="")
                    if action.text:
                        print(f" text='{action.text[:30]}...'", end="")
                    if action.key:
                        print(f" key={action.key}", end="")
                    print()
                
                if action.action_type == ActionType.SCREENSHOT:
                    screenshot = self._capture_screenshot()
                    tool_results.append(self._provider.create_tool_result(
                        tool_use_id=action_data["id"],
                        screenshot_base64=screenshot["base64"],
                    ))
                    continue
                
                if not self.dry_run and is_high_risk(action):
                    if self._confirm_callback:
                        if not self._confirm_callback(action):
                            if verbose:
                                print("High-risk action rejected by user")
                            self.status = SessionStatus.CANCELLED
                            return self._get_summary(error="High-risk action rejected")
                    else:
                        if verbose:
                            print(f"WARNING: High-risk action detected, skipping (no confirmation callback)")
                        tool_results.append(self._provider.create_tool_result(
                            tool_use_id=action_data["id"],
                            error="High-risk action requires confirmation",
                        ))
                        continue
                
                result = execute_action(action, dry_run=self.dry_run)
                self._log_action(action, result)
                
                if verbose:
                    status = "OK" if result.success else f"FAILED: {result.error_message}"
                    mode = "(dry-run)" if self.dry_run else ""
                    print(f"  -> {status} {mode} ({result.execution_time_ms:.1f}ms)")
                
                if not self.dry_run:
                    time.sleep(0.1)
                
                screenshot = self._capture_screenshot()
                
                if result.success:
                    tool_results.append(self._provider.create_tool_result(
                        tool_use_id=action_data["id"],
                        screenshot_base64=screenshot["base64"],
                    ))
                else:
                    tool_results.append(self._provider.create_tool_result(
                        tool_use_id=action_data["id"],
                        error=result.error_message,
                    ))
            
            self.messages.append({"role": "user", "content": tool_results})
        
        if verbose:
            print(f"\nMax iterations ({self.max_iterations}) reached")
        self.status = SessionStatus.MAX_ITERATIONS
        return self._get_summary()
    
    def _estimate_cost(self) -> float:
        """Estimate cost in USD based on model pricing."""
        pricing = {
            "claude-sonnet-4-5": (3.0, 15.0),
            "claude-opus-4-5": (15.0, 75.0),
            "claude-haiku-4-5": (0.80, 4.0),
        }
        input_rate, output_rate = pricing.get(self.model, (3.0, 15.0))
        input_cost = (self.total_input_tokens / 1_000_000) * input_rate
        output_cost = (self.total_output_tokens / 1_000_000) * output_rate
        return round(input_cost + output_cost, 6)
    
    def _get_summary(self, error: str = None) -> Dict[str, Any]:
        """Get session summary."""
        self.end_time = datetime.now()
        duration_ms = 0
        if self.start_time:
            duration_ms = (self.end_time - self.start_time).total_seconds() * 1000
        return {
            "session_id": self.session_id,
            "status": self.status.value,
            "model": self.model,
            "iterations": self.current_iteration,
            "max_iterations": self.max_iterations,
            "dry_run": self.dry_run,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_api_latency_ms": round(self.total_api_latency_ms, 2),
            "total_duration_ms": round(duration_ms, 2),
            "actions_count": len(self.actions_log),
            "estimated_cost_usd": self._estimate_cost(),
            "error": error,
        }
    
    def save_log(self, path: str = None):
        """Save session log to JSON file."""
        if path is None:
            path = f"session_{self.session_id}.json"
        
        log_data = {
            "session_id": self.session_id,
            "task_prompt": self.task_prompt,
            "status": self.status.value,
            "iterations": self.current_iteration,
            "dry_run": self.dry_run,
            "tokens": {
                "input": self.total_input_tokens,
                "output": self.total_output_tokens,
            },
            "actions": self.actions_log,
        }
        
        with open(path, "w") as f:
            json.dump(log_data, f, indent=2)
        
        return path
