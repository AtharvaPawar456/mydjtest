# Prompt for ideas-19.json

**Save ChatGPT reply as:** test/project-ideas/ideas-19.json

| Meta | Value |
|------|-------|
| idea number | 19 |
| prodid | 63 |
| category_slug | hardware |
| product_name | Smart Agricultural Weather Prediction and Decision Support System |
| DB status | needs generation |

---

## Copy everything below this line into ChatGPT

---

You are writing the full product-detail content for one HandMadeProjects catalog page.

### Project identity (do not change)
- product_name: Smart Agricultural Weather Prediction and Decision Support System
- prodid: 63
- category_slug: hardware

### Existing site context (use as grounding; expand into full professional detail)
- highlighttitle: A weather monitoring system that collects environmental data and predicts farming conditions.
- prodtags: ESP32, Arduino IDE, temperature sensor, humidity sensor, rain sensor, pressure sensor, cloud analytics, Weather-based farming decisions
- existing short text: Project Name Smart Agricultural Weather Prediction and Decision Support System Description A weather monitoring system that collects environmental data and predicts farming conditions. Farmers receive recommendations for irrigation and crop protection. Technologies ESP32, Arduino IDE, temperature sensor, humidity sensor, rain sensor, pressure sensor, cloud analytics Applications Weather-based farming decisions Report Contents Components List (BOM: Bill of Material) Block Diagram Flow Chart Components : Name, Images, Details Circuit Diagram Problem Statement Abstract Introduction Methodology Challenges and Solutions Performance Analysis Advantages Limitation Application Future Scope Conclusion Output Images Project Deliverables Project Hardware Project Report Project Simulation

### Output requirement
Return **ONLY a single JSON object** (no markdown code fences, no commentary) with **exactly** these keys and the requested detail:

{
  "product_name": "string — exact project title",
  "prodid": "integer — copy from this prompt",
  "category_slug": "string — e.g. hardware",
  "highlighttitle": "string — one sentence product highlight (max ~40 words)",
  "tech": "string — comma-separated technologies / modules (Tech section)",
  "abstract": "string — 120 to 160 words, formal project abstract",
  "keywords": [
    "12 to 20 technical keyword terms"
  ],
  "project_description": "string — 220 to 350 words: problem, objectives, approach, value",
  "project_features": [
    "8 to 12 short bullet feature lines (product-sheet style, not long paragraphs)"
  ],
  "hardware_components": "string — comma-separated major hardware parts",
  "software_components": "string — comma-separated tools/platforms",
  "applications": [
    "5 to 8 short application scenarios"
  ],
  "advantages": [
    "5 to 8 short points"
  ],
  "limitations": [
    "4 to 6 realistic constraints"
  ],
  "future_scope": [
    "4 to 6 upgrade / extension ideas"
  ],
  "conclusion": "string — 120 to 180 words"
}

### Quality bar
- Match the depth and style of a strong catalog page like iBin (hardware product 33): concrete tech stack, clear problem to solution narrative, realistic student-lab hardware/software lists, practical features/applications/limitations.
- Abstract and Conclusion must be self-contained paragraphs (not bullet lists).
- Project Features must be short, scannable bullets (not 80-word essays).
- Keywords: 12 to 20 distinct technical terms relevant to this project.
- Be specific to **Smart Agricultural Weather Prediction and Decision Support System** — avoid copy-paste generic IoT fluff.
- Include prodid=63 and category_slug="hardware" and product_name exactly as given.

After you produce the JSON, I will save it as ideas-19.json.
