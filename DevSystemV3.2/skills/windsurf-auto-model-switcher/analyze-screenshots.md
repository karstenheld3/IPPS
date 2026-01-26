# Analyze Model Selector Screenshots

Please analyze the screenshots in `selector-screenshots/` folder and extract:

1. Model name (exact as shown in UI)
2. Cost factor (e.g., "2x", "Free", "0.5x")

From each screenshot, list all visible models in the selector popup.

## Screenshots to analyze:
- section_01.png through section_10.png

## Output format (JSON):

```json
{
  "models": [
    { "name": "Claude 3.5 Sonnet", "cost": "2x" },
    { "name": "Claude 3.7 Sonnet", "cost": "2x" },
    ...
  ]
}
```

## Instructions:
1. Look at the model selector popup (right side of screen)
2. Extract each model name and its cost
3. Skip duplicates
4. Include all models from all 10 screenshots
5. Output as valid JSON

Start with section_01.png and work through section_10.png.
