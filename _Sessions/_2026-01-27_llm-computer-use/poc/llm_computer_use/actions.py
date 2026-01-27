"""Action execution module for mouse and keyboard control."""
import time
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum

class ActionType(Enum):
    SCREENSHOT = "screenshot"
    LEFT_CLICK = "left_click"
    RIGHT_CLICK = "right_click"
    MIDDLE_CLICK = "middle_click"
    DOUBLE_CLICK = "double_click"
    TRIPLE_CLICK = "triple_click"
    MOUSE_MOVE = "mouse_move"
    SCROLL = "scroll"
    TYPE = "type"
    KEY = "key"
    HOLD_KEY = "hold_key"
    WAIT = "wait"
    LEFT_CLICK_DRAG = "left_click_drag"
    LEFT_MOUSE_DOWN = "left_mouse_down"
    LEFT_MOUSE_UP = "left_mouse_up"

@dataclass
class Action:
    """Represents an action to execute."""
    action_type: ActionType
    coordinate: Optional[Tuple[int, int]] = None
    text: Optional[str] = None
    key: Optional[str] = None
    direction: Optional[str] = None
    amount: Optional[int] = None
    duration_seconds: Optional[float] = None
    start_coordinate: Optional[Tuple[int, int]] = None
    end_coordinate: Optional[Tuple[int, int]] = None

@dataclass
class ActionResult:
    """Result of executing an action."""
    success: bool
    error_message: Optional[str] = None
    execution_time_ms: float = 0.0

HIGH_RISK_PATTERNS = [
    "alt+f4",
    "ctrl+alt+delete",
    "del ",
    "rm ",
    "format",
    "shutdown",
    "reboot",
]

def is_high_risk(action: Action) -> bool:
    """Check if action is high-risk and requires confirmation."""
    if action.action_type == ActionType.KEY and action.key:
        key_lower = action.key.lower()
        for pattern in HIGH_RISK_PATTERNS:
            if pattern in key_lower:
                return True
    if action.action_type == ActionType.TYPE and action.text:
        text_lower = action.text.lower()
        for pattern in HIGH_RISK_PATTERNS:
            if pattern in text_lower:
                return True
    return False

def execute_action(action: Action, dry_run: bool = False) -> ActionResult:
    """Execute a single action.
    
    Args:
        action: Action to execute
        dry_run: If True, log but don't execute
        
    Returns:
        ActionResult with success status and timing
    """
    start = time.perf_counter()
    
    if dry_run:
        elapsed = (time.perf_counter() - start) * 1000
        return ActionResult(success=True, execution_time_ms=elapsed)
    
    try:
        import pyautogui
        pyautogui.FAILSAFE = True
        
        if action.action_type == ActionType.SCREENSHOT:
            pass
            
        elif action.action_type == ActionType.LEFT_CLICK:
            if action.coordinate:
                pyautogui.click(action.coordinate[0], action.coordinate[1], button='left')
            else:
                pyautogui.click(button='left')
                
        elif action.action_type == ActionType.RIGHT_CLICK:
            if action.coordinate:
                pyautogui.click(action.coordinate[0], action.coordinate[1], button='right')
            else:
                pyautogui.click(button='right')
                
        elif action.action_type == ActionType.MIDDLE_CLICK:
            if action.coordinate:
                pyautogui.click(action.coordinate[0], action.coordinate[1], button='middle')
            else:
                pyautogui.click(button='middle')
                
        elif action.action_type == ActionType.DOUBLE_CLICK:
            if action.coordinate:
                pyautogui.doubleClick(action.coordinate[0], action.coordinate[1])
            else:
                pyautogui.doubleClick()
                
        elif action.action_type == ActionType.TRIPLE_CLICK:
            if action.coordinate:
                pyautogui.tripleClick(action.coordinate[0], action.coordinate[1])
            else:
                pyautogui.tripleClick()
                
        elif action.action_type == ActionType.MOUSE_MOVE:
            if action.coordinate:
                pyautogui.moveTo(action.coordinate[0], action.coordinate[1])
                
        elif action.action_type == ActionType.SCROLL:
            amount = action.amount or 3
            x, y = action.coordinate if action.coordinate else (None, None)
            if action.direction == "up":
                pyautogui.scroll(amount, x, y)
            elif action.direction == "down":
                pyautogui.scroll(-amount, x, y)
            elif action.direction == "left":
                pyautogui.hscroll(-amount, x, y)
            elif action.direction == "right":
                pyautogui.hscroll(amount, x, y)
                
        elif action.action_type == ActionType.TYPE:
            if action.text:
                pyautogui.write(action.text, interval=0.02)
                
        elif action.action_type == ActionType.KEY:
            if action.key:
                keys = action.key.lower().split('+')
                pyautogui.hotkey(*keys)
                
        elif action.action_type == ActionType.HOLD_KEY:
            if action.key and action.duration_seconds:
                pyautogui.keyDown(action.key)
                time.sleep(action.duration_seconds)
                pyautogui.keyUp(action.key)
                
        elif action.action_type == ActionType.WAIT:
            if action.duration_seconds:
                time.sleep(action.duration_seconds)
                
        elif action.action_type == ActionType.LEFT_CLICK_DRAG:
            if action.start_coordinate and action.end_coordinate:
                pyautogui.moveTo(action.start_coordinate[0], action.start_coordinate[1])
                pyautogui.drag(
                    action.end_coordinate[0] - action.start_coordinate[0],
                    action.end_coordinate[1] - action.start_coordinate[1],
                    button='left'
                )
                
        elif action.action_type == ActionType.LEFT_MOUSE_DOWN:
            if action.coordinate:
                pyautogui.mouseDown(action.coordinate[0], action.coordinate[1], button='left')
            else:
                pyautogui.mouseDown(button='left')
                
        elif action.action_type == ActionType.LEFT_MOUSE_UP:
            if action.coordinate:
                pyautogui.mouseUp(action.coordinate[0], action.coordinate[1], button='left')
            else:
                pyautogui.mouseUp(button='left')
        
        elapsed = (time.perf_counter() - start) * 1000
        return ActionResult(success=True, execution_time_ms=elapsed)
        
    except Exception as e:
        elapsed = (time.perf_counter() - start) * 1000
        return ActionResult(success=False, error_message=str(e), execution_time_ms=elapsed)

def parse_anthropic_action(tool_input: Dict[str, Any]) -> Action:
    """Parse Anthropic tool_use input into Action object.
    
    Args:
        tool_input: The 'input' field from Anthropic tool_use response
        
    Returns:
        Action object ready for execution
    """
    action_str = tool_input.get("action", "screenshot")
    
    try:
        action_type = ActionType(action_str)
    except ValueError:
        action_type = ActionType.SCREENSHOT
    
    coordinate = None
    if "coordinate" in tool_input:
        coord = tool_input["coordinate"]
        coordinate = (int(coord[0]), int(coord[1]))
    
    start_coordinate = None
    if "start_coordinate" in tool_input:
        coord = tool_input["start_coordinate"]
        start_coordinate = (int(coord[0]), int(coord[1]))
    
    end_coordinate = None
    if "end_coordinate" in tool_input:
        coord = tool_input["end_coordinate"]
        end_coordinate = (int(coord[0]), int(coord[1]))
    
    return Action(
        action_type=action_type,
        coordinate=coordinate,
        text=tool_input.get("text"),
        key=tool_input.get("key"),
        direction=tool_input.get("direction"),
        amount=tool_input.get("amount"),
        duration_seconds=tool_input.get("duration_seconds"),
        start_coordinate=start_coordinate,
        end_coordinate=end_coordinate,
    )
