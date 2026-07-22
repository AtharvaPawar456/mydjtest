# Prompt for ideas-07.json

**Save ChatGPT reply as:** test/project-ideas/ideas-07.json

| Meta | Value |
|------|-------|
| idea number | 07 |
| prodid | 50 |
| category_slug | hardware |
| product_name | Smart Water Level Indicator Using Arduino |
| DB status | already-enriched (optional re-gen) |

---

## Copy everything below this line into ChatGPT

---

You are writing the full product-detail content for one HandMadeProjects catalog page.

### Project identity (do not change)
- product_name: Smart Water Level Indicator Using Arduino
- prodid: 50
- category_slug: hardware

### Existing site context (use as grounding; expand into full professional detail)
- highlighttitle: An efficient Arduino-based monitoring system providing real-time visual and audible alerts to prevent water overflow and shortage.
- prodtags: Water Level Monitoring, Arduino Nano, Liquid Level Sensor, Overflow Detection, Embedded Systems, Automation, Buzzer Alert, LED Indicators, Analog Signal Processing, Water Management, Smart Home, IoT Hardware, Resource Conservation, Real-time Monitoring, Circuit Design
- existing short text: Tech Arduino Nano, Water Level Sensor, LED Indicators, Piezo Buzzer, Embedded C Abstract This project implements a Smart Water Level Indicator designed to automate the monitoring of liquid levels in storage tanks using an Arduino Nano. The system utilizes a water level sensor to detect the depth of water and translates this analog data into specific visual and auditory signals. Three LEDs are employed to represent low, medium, and high water levels, providing an immediate status update to the user. To prevent water wastage, a piezo buzzer is integrated to trigger an alarm when the tank reaches its maximum capacity (overflow condition). The project focuses on creating a cost-effective, low-power solution for residential and small-scale industrial use, demonstrating the practical application of embedded systems in solving common household resource management challenges. Keywords Water Leve…

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
- Be specific to **Smart Water Level Indicator Using Arduino** — avoid copy-paste generic IoT fluff.
- Include prodid=50 and category_slug="hardware" and product_name exactly as given.

After you produce the JSON, I will save it as ideas-07.json.
