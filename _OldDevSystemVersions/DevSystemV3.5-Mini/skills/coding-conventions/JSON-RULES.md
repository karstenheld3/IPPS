# JSON Coding Conventions

## Field Naming

- Spell out field names, no abbreviations: `temperature_factor`, `max_tokens`, `config`
- Use snake_case: `temperature_factor` not `temperatureFactor`
- Prefix provider-specific fields: `openai_reasoning_effort`, `anthropic_thinking_factor`

## Formatting

- 2-space indentation
- 2D tables: one line per row, align columns
  ```json
  "effort_mapping": {
    "none":    { "temperature_factor": 0.0,  "openai_effort": "none",    "output_factor": 0.25 },
    "minimal": { "temperature_factor": 0.1,  "openai_effort": "minimal", "output_factor": 0.5 }
  }
  ```

## Structure

- Separate concerns into distinct files
- Use `_comment` field for inline documentation
- Include metadata at top: `_version`, `_updated`, `_comment`

## Values

- Use `null` for "not set" / "disabled by default" (not `0` or omission)
- Use factors (0.0-1.0) for values that depend on model limits