# Prompt for ideas-06.json

**Save ChatGPT reply as:** test/project-ideas/ideas-06.json

| Meta | Value |
|------|-------|
| idea number | 06 |
| prodid | 49 |
| category_slug | hardware |
| product_name | Smart Touchless Water Dispenser |
| DB status | already-enriched (optional re-gen) |

---

## Copy everything below this line into ChatGPT

---

You are writing the full product-detail content for one HandMadeProjects catalog page.

### Project identity (do not change)
- product_name: Smart Touchless Water Dispenser
- prodid: 49
- category_slug: hardware

### Existing site context (use as grounding; expand into full professional detail)
- highlighttitle: An automatic water tap system using IR sensors for contactless and efficient water usage to enhance hygiene and reduce wastage.
- prodtags: IR Sensor, Arduino Nano, Water Automation, Contactless Dispenser, Hygiene Technology, DC Water Pump, Relay Circuit, Water Conservation, Embedded Systems, Proximity Sensing, Smart Tap, Automation Prototype, Microcontroller, Touchless System, Electronic Switching, Sanitation Hardware
- existing short text: Tech Arduino Nano, IR Sensor, DC Water Pump, Relay Module, LED Indicators, Piezo Buzzer Abstract This project presents a prototype of an automatic water tap designed to operate without physical contact to mitigate the spread of germs and bacteria. The system utilizes an infrared (IR) sensor to detect the presence of a user's hand, which triggers the Arduino Nano microcontroller to activate a miniature water pump via a relay. To prevent overflow and conserve water, the pump is programmed to dispense water for a fixed duration of 30 seconds per trigger. The integration of LED indicators and a buzzer provides real-time operational feedback, ensuring a user-friendly experience. Built on a simulated cardboard structure, this prototype demonstrates a cost-effective, power-efficient approach to automation in sanitation, serving as a foundational model for industrial-grade touchless dispensing s…

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
- Be specific to **Smart Touchless Water Dispenser** — avoid copy-paste generic IoT fluff.
- Include prodid=49 and category_slug="hardware" and product_name exactly as given.

After you produce the JSON, I will save it as ideas-06.json.
