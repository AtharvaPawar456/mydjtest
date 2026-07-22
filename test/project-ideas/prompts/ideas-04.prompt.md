# Prompt for ideas-04.json

**Save ChatGPT reply as:** test/project-ideas/ideas-04.json

| Meta | Value |
|------|-------|
| idea number | 04 |
| prodid | 47 |
| category_slug | hardware |
| product_name | Smart 1-Axis Solar Tracker System |
| DB status | already-enriched (optional re-gen) |

---

## Copy everything below this line into ChatGPT

---

You are writing the full product-detail content for one HandMadeProjects catalog page.

### Project identity (do not change)
- product_name: Smart 1-Axis Solar Tracker System
- prodid: 47
- category_slug: hardware

### Existing site context (use as grounding; expand into full professional detail)
- highlighttitle: An automatic solar tracking system using LDR sensors to maximize sunlight absorption and energy efficiency.
- prodtags: Solar Tracker, LDR Sensor, Arduino Nano, Servo Motor, Renewable Energy, Automatic Alignment, Solar Panel, Green Technology, Low Power System, Efficiency Improvement, Photovoltaic, Analog Sensing, Mechatronics, Embedded Systems, Energy Harvesting, Light Intensity, Single Axis Tracking, Sustainable Power
- existing short text: Tech Arduino Nano, LDR Sensors, Servo Motor, Photovoltaic Panel, Analog-to-Digital Conversion, Proportional Control Logic Abstract This project implements a low-cost one-axis solar tracker designed to automatically orient a photovoltaic panel toward the sun to maximize energy capture. The system utilizes a pair of Light Dependent Resistors (LDRs) to detect directional irradiance differences. An Arduino Nano processes these analog signals, computes the illumination error, and drives a hobby servo motor to rotate the panel until the light intensity is balanced across both sensors. Visual indicators via LEDs and an optional buzzer provide real-time status feedback and calibration alerts. By maintaining a perpendicular angle to the sun's rays, the system significantly increases the effective incident sunlight compared to static mounts, demonstrating a practical approach to improving renewabl…

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
- Be specific to **Smart 1-Axis Solar Tracker System** — avoid copy-paste generic IoT fluff.
- Include prodid=47 and category_slug="hardware" and product_name exactly as given.

After you produce the JSON, I will save it as ideas-04.json.
