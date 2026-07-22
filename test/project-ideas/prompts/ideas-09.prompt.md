# Prompt for ideas-09.json

**Save ChatGPT reply as:** test/project-ideas/ideas-09.json

| Meta | Value |
|------|-------|
| idea number | 09 |
| prodid | 52 |
| category_slug | hardware |
| product_name | Smart Staircase Lighting System |
| DB status | already-enriched (optional re-gen) |

---

## Copy everything below this line into ChatGPT

---

You are writing the full product-detail content for one HandMadeProjects catalog page.

### Project identity (do not change)
- product_name: Smart Staircase Lighting System
- prodid: 52
- category_slug: hardware

### Existing site context (use as grounding; expand into full professional detail)
- highlighttitle: Automatically illuminates staircase when human motion is detected for safer navigation and energy efficiency.
- prodtags: staircase lighting, IR sensor, Arduino Nano, motion detection, home automation, LED array, energy saving, smart lighting, embedded systems, human presence detection, automated switches, home safety, microcontroller project, infrared sensing, low power lighting, smart home prototype
- existing short text: Tech Arduino Nano, IR Sensors, LED Lighting, Motion Detection, Automation, Embedded C Abstract The Smart Staircase Lighting System is an automated home safety solution designed to provide hands-free illumination during staircase navigation. The system utilizes infrared (IR) sensors strategically placed at the entry and exit points of the stairs to detect human presence. Upon detection, the Arduino Nano microcontroller triggers a sequence of LED lights to illuminate the path, ensuring safe movement in dark environments. The lights remain active for a predefined duration and automatically switch off after a period of inactivity to minimize power consumption. This project integrates basic sensor interfacing and microcontroller programming to create a responsive, low-cost automation system. The result is a practical prototype that enhances residential safety while promoting energy conservati…

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
- Be specific to **Smart Staircase Lighting System** — avoid copy-paste generic IoT fluff.
- Include prodid=52 and category_slug="hardware" and product_name exactly as given.

After you produce the JSON, I will save it as ideas-09.json.
