Score this compressed prompt file on a 1-5 scale.

Score 5: ALL DO/DON'T rules preserved verbatim. ALL scoring scales with exact thresholds intact. ALL output format specs including JSON schemas preserved. ALL tag definitions present. ALL evaluation weights exact. Model output from compressed prompt would be identical to output from original. Size reduction >20%.

Score 4: All behavioral instructions preserved. Minor omissions: a redundant example removed, an explanatory sentence dropped. Model output would be functionally identical with possible minor formatting differences. Size reduction >10%.

Score 3: Core instructions preserved but some nuance lost: a scoring criterion description shortened losing a boundary condition, an example compressed losing a format detail, or a penalty condition simplified. Model output would mostly match but might miss specific quality checks.

Score 2: Significant instruction content lost: scoring thresholds altered, DO/DON'T rules missing items, output format spec incomplete, or tag definitions missing. Model output would differ noticeably.

Score 1: Critical instructions missing: scoring scale broken, output format undefined, DO rules dropped, or evaluation criteria removed. Model would produce substantially different or unusable output.

Minimum acceptable score: 3.5

Check specifically:
- [ ] All DO/DON'T rules present and verbatim
- [ ] All scoring thresholds exact (numeric values unchanged)
- [ ] All output JSON schemas complete
- [ ] All tag definitions present
- [ ] All CRITICAL/FORBIDDEN constraints verbatim
- [ ] Evaluation weights unchanged
- [ ] At least 1 complete example per output format

Return: {"score": N, "justification": "...", "lost_items": ["..."], "size_reduction_percent": N}