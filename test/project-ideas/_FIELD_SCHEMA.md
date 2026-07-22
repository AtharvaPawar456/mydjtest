# Field schema reference (productinfo/hardware/33 style)

| JSON key | Page heading | Format |
|----------|--------------|--------|
| tech | Tech | paragraph, comma-separated stack |
| abstract | Abstract | 120–160 words |
| keywords | Keywords | array of 12–20 terms (rendered comma-separated) |
| project_description | Project Description | 220–350 words |
| project_features | Project Features | array of 8–12 short bullets |
| hardware_components | Specifications → Hardware components | string |
| software_components | Specifications → Software components | string |
| applications | Applications | array 5–8 bullets |
| advantages | Advantages | array 5–8 bullets |
| limitations | Limitations | array 4–6 bullets |
| future_scope | Future Scope | array 4–6 bullets |
| conclusion | Conclusion | 120–180 words |
| highlighttitle | (page highlight / card subtitle) | ~1 sentence |
| product_name, prodid, category_slug | identity | must match prompt |

Depth inspiration (fold into description/abstract/conclusion; do not invent extra top-level keys):
Problem Statement, Background, Objectives, Motivation — covered inside project_description.
