"""Screen capture module with resize and encoding for LLM APIs."""
import base64
import time
from io import BytesIO
from typing import Optional, Tuple, Dict, Any

class ScreenCapture:
    """Fast screenshot capture with resize for LLM APIs."""
    
    def __init__(self, max_edge: int = 1568, jpeg_quality: int = 85):
        self.max_edge = max_edge
        self.jpeg_quality = jpeg_quality
        self._mss = None
    
    def _get_mss(self):
        if self._mss is None:
            import mss
            self._mss = mss.mss()
        return self._mss
    
    def capture_raw(self, monitor: int = 1):
        """Capture screenshot as PIL Image.
        
        Args:
            monitor: Monitor index (0=all, 1=primary, 2+=secondary)
        
        Returns:
            PIL.Image.Image: Captured screenshot
        """
        from PIL import Image
        sct = self._get_mss()
        screenshot = sct.grab(sct.monitors[monitor])
        return Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
    
    def resize_if_needed(self, img) -> 'Image':
        """Resize image if larger than max_edge, preserving aspect ratio.
        
        Args:
            img: PIL Image to resize
            
        Returns:
            PIL.Image.Image: Resized image (or original if small enough)
        """
        from PIL import Image
        w, h = img.size
        if w <= self.max_edge and h <= self.max_edge:
            return img
        if w > h:
            new_w = self.max_edge
            new_h = int(h * (self.max_edge / w))
        else:
            new_h = self.max_edge
            new_w = int(w * (self.max_edge / h))
        return img.resize((new_w, new_h), resample=Image.Resampling.LANCZOS)
    
    def to_jpeg_bytes(self, img) -> bytes:
        """Convert PIL Image to JPEG bytes."""
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=self.jpeg_quality)
        return buffer.getvalue()
    
    def to_base64(self, img) -> str:
        """Convert PIL Image to JPEG base64 string."""
        return base64.b64encode(self.to_jpeg_bytes(img)).decode("utf-8")
    
    def capture_for_api(self, monitor: int = 1) -> Dict[str, Any]:
        """Capture, resize, and encode - ready for Anthropic API.
        
        Args:
            monitor: Monitor index (0=all, 1=primary)
            
        Returns:
            dict: {
                "base64": str,
                "media_type": "image/jpeg",
                "original_size": (w, h),
                "resized_size": (w, h),
            }
        """
        start = time.perf_counter()
        img = self.capture_raw(monitor)
        original_size = img.size
        resized = self.resize_if_needed(img)
        b64 = self.to_base64(resized)
        elapsed_ms = (time.perf_counter() - start) * 1000
        
        return {
            "base64": b64,
            "media_type": "image/jpeg",
            "original_size": original_size,
            "resized_size": resized.size,
            "capture_ms": round(elapsed_ms, 2),
        }
    
    def save_screenshot(self, path: str, monitor: int = 1, resize: bool = True) -> Dict[str, Any]:
        """Capture and save to file.
        
        Args:
            path: Output file path
            monitor: Monitor index
            resize: Whether to resize before saving
            
        Returns:
            dict: {"path": str, "size": (w, h)}
        """
        img = self.capture_raw(monitor)
        if resize:
            img = self.resize_if_needed(img)
        img.save(path, format="JPEG", quality=self.jpeg_quality)
        return {"path": str(path), "size": img.size}
    
    def get_display_info(self) -> Dict[str, Any]:
        """Get information about available displays.
        
        Returns:
            dict: Display information including monitor count and sizes
        """
        sct = self._get_mss()
        monitors = []
        for i, mon in enumerate(sct.monitors):
            monitors.append({
                "index": i,
                "left": mon["left"],
                "top": mon["top"],
                "width": mon["width"],
                "height": mon["height"],
            })
        return {
            "monitor_count": len(monitors) - 1,
            "monitors": monitors,
        }
