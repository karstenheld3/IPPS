Score this compressed template file on a 1-5 scale.

Score 5: ALL section headings preserved at correct level. ALL ID format patterns intact. ALL placeholder tokens present. ALL field definitions preserved. Header block structure complete. Size reduction >25%. A document created from this template would have identical structure to one created from the original.

Score 4: Complete structural contract preserved. Minor omissions: a worked example shortened, a BAD/GOOD pair removed (belongs in rules file anyway), explanatory prose between sections trimmed. Output documents would be structurally identical. Size reduction >15%.

Score 3: Core structure preserved but some template guidance lost: a field description simplified losing a constraint, an example format removed (but the placeholder remains), or a section description dropped that clarified non-obvious content expectations. Output documents would mostly match but might miss optional sections.

Score 2: Structural contract broken: section headings missing or wrong level, ID format patterns incomplete, required fields dropped from header block, or checkbox patterns altered. Output documents would differ structurally.

Score 1: Template unusable: major sections missing, header block broken, ID system incompatible with DevSystem standards, or structure so altered that output documents wouldn't conform to system expectations.

Minimum acceptable score: 3.5

Check specifically:
- [ ] All section headings at correct markdown level
- [ ] All ID format patterns preserved exactly
- [ ] Header block complete (Doc ID, Goal, dependencies)
- [ ] All placeholder tokens in brackets present
- [ ] All checkbox patterns preserved
- [ ] Document History section format intact
- [ ] At least 1 example per content type

Return: {"score": N, "justification": "...", "lost_items": ["..."], "size_reduction_percent": N}