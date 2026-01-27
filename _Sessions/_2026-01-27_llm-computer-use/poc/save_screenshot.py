from llm_computer_use_v2 import ScreenCapture
import base64

sc = ScreenCapture()
result = sc.capture_for_api()

with open('example_screenshot.jpg', 'wb') as f:
    f.write(base64.b64decode(result['base64']))

print(f"Screenshot saved: example_screenshot.jpg")
print(f"Original size: {result['original_size']}")
print(f"Resized to: {result['resized_size']}")
print(f"Capture time: {result['capture_ms']}ms")
print(f"Base64 length: {len(result['base64'])} chars")
