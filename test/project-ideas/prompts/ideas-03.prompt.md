# Prompt for ideas-03.json

**Save ChatGPT reply as:** test/project-ideas/ideas-03.json

| Meta | Value |
|------|-------|
| idea number | 03 |
| prodid | 46 |
| category_slug | hardware |
| product_name | Smart Automatic Street Light System |
| DB status | already-enriched (optional re-gen) |

---

## Copy everything below this line into ChatGPT

---

You are writing the full product-detail content for one HandMadeProjects catalog page.

### Project identity (do not change)
- product_name: Smart Automatic Street Light System
- prodid: 46
- category_slug: hardware

### Existing site context (use as grounding; expand into full professional detail)
- highlighttitle: Automatic street light control using LDR and Arduino for efficient energy saving and automated illumination.
- prodtags: Street light automation, Arduino Nano, LDR sensor, Energy efficiency, Relay module, Smart lighting, Daylight detection, Embedded systems, Sustainable infrastructure, Automatic switching, Smart city project, Ambient light sensing, Power conservation, IoT hardware, Light intensity threshold, Automated circuitry
- existing short text: Tech Arduino Nano, LDR Sensor, Relay Module, LED Lighting, Embedded C Abstract This project focuses on the design and implementation of an automated street lighting system aimed at reducing energy wastage in urban environments. The system utilizes a Light Dependent Resistor (LDR) to continuously monitor ambient light intensity, which is then processed by an Arduino Nano microcontroller. Based on a predefined threshold, the controller triggers a relay module to switch the street lights ON during darkness and OFF during daylight hours. By eliminating the need for manual operation, the system ensures consistent illumination for road safety while significantly lowering electricity consumption. The prototype demonstrates a cost-effective, scalable approach to smart city infrastructure, integrating basic sensing technology with embedded control to achieve sustainable energy management. Keyword…

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
- Be specific to **Smart Automatic Street Light System** — avoid copy-paste generic IoT fluff.
- Include prodid=46 and category_slug="hardware" and product_name exactly as given.

After you produce the JSON, I will save it as ideas-03.json.
