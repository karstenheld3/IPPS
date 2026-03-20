# Judge Answer

Score how well the model answer matches the reference answer.

Scoring (0-5):
- **5**: Perfect match, all key information, no errors
- **4**: Minor omissions or phrasing differences, core facts correct
- **3**: Some key information present, some missing
- **2**: Significant errors or omissions, partially correct
- **1**: Mostly incorrect or irrelevant
- **0**: Completely incorrect or no relevant content

Question: {question}
Reference Answer: {reference_answer}
Model Answer: {model_answer}

Respond with ONLY a JSON object:
```json
{
  "score": <0-5>,
  "rationale": "<brief explanation>"
}
```