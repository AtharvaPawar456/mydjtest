# Prompt for ideas-05.json

**Save ChatGPT reply as:** test/project-ideas/ideas-05.json

| Meta | Value |
|------|-------|
| idea number | 05 |
| prodid | 48 |
| category_slug | hardware |
| product_name | Smart Dual-Axis Solar Tracker System |
| DB status | already-enriched (optional re-gen) |

---

## Copy everything below this line into ChatGPT

---

You are writing the full product-detail content for one HandMadeProjects catalog page.

### Project identity (do not change)
- product_name: Smart Dual-Axis Solar Tracker System
- prodid: 48
- category_slug: hardware

### Existing site context (use as grounding; expand into full professional detail)
- highlighttitle: An automatic solar tracking system using LDR sensors and servo motors for efficient sunlight alignment.
- prodtags: Solar Tracker, Dual-Axis Tracking, Renewable Energy, LDR Sensor, Arduino Nano, Servo Motor, Photovoltaic Efficiency, Automation, Energy Harvesting, Sustainability, Azimuth Angle, Elevation Angle, Light Intensity, Embedded Systems, Green Technology, Automatic Alignment
- existing short text: Tech Arduino Nano, LDR Sensors, Servo Motors, Solar Energy Harvesting Abstract This project presents a compact, low-cost dual-axis solar tracker designed to maximize the efficiency of photovoltaic panels. Utilizing an Arduino Nano microcontroller, the system employs four Light Dependent Resistors (LDRs) to detect sunlight intensity from different directions. By comparing the analog values from these sensors, the system automatically adjusts two servo motors to align the solar panel both horizontally (azimuth) and vertically (elevation). Unlike static solar installations, which suffer from cosine loss as the sun moves, this active tracking mechanism ensures the panel remains perpendicular to the sun's rays. The prototype is constructed on a lightweight cardboard model for academic demonstration, integrating LEDs and a buzzer for operational feedback. The result is a sustainable engineerin…

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
- Be specific to **Smart Dual-Axis Solar Tracker System** — avoid copy-paste generic IoT fluff.
- Include prodid=48 and category_slug="hardware" and product_name exactly as given.

After you produce the JSON, I will save it as ideas-05.json.
