# Prompt for ideas-01.json

**Save ChatGPT reply as:** test/project-ideas/ideas-01.json

| Meta | Value |
|------|-------|
| idea number | 01 |
| prodid | 44 |
| category_slug | hardware |
| product_name | Smart Gas Leakage Detector with Safety Alert System |
| DB status | already-enriched (optional re-gen) |

---

## Copy everything below this line into ChatGPT

---

You are writing the full product-detail content for one HandMadeProjects catalog page.

### Project identity (do not change)
- product_name: Smart Gas Leakage Detector with Safety Alert System
- prodid: 44
- category_slug: hardware

### Existing site context (use as grounding; expand into full professional detail)
- highlighttitle: A compact, automated safety system designed to detect combustible gas leaks and trigger immediate ventilation and audible alerts to prevent fire hazards.
- prodtags: Gas Sensor, Arduino Nano, MQ-2, MQ-6, LPG Detection, Exhaust Fan, Buzzer Alert, Embedded Control, Real-time Monitoring, Fire Prevention, Combustible Gas, Analog Input, Safety Automation, Household Safety, Industrial Safety, Threshold Logic
- existing short text: Tech Arduino Nano, MQ-Series Gas Sensors, DC Motor Control, Analog Signal Processing, Embedded Systems Abstract The Smart Gas Leakage Detector is a low-cost, high-reliability safety device engineered for residential and small-scale industrial environments. Utilizing an MQ-series gas sensor, the system continuously monitors ambient air for the presence of combustible gases such as LPG, propane, or methane. An Arduino Nano microcontroller processes the analog sensor data, applying threshold-based logic to differentiate between normal atmospheric levels and hazardous leaks. Upon detection of a leak, the system executes a multi-modal response: triggering a piezo buzzer and LED indicators for immediate human notification, while simultaneously activating a DC exhaust fan to dilute gas concentration. This prototype demonstrates an effective integration of sensing and actuation to mitigate the r…

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
- Be specific to **Smart Gas Leakage Detector with Safety Alert System** — avoid copy-paste generic IoT fluff.
- Include prodid=44 and category_slug="hardware" and product_name exactly as given.

After you produce the JSON, I will save it as ideas-01.json.
