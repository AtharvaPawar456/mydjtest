# Prompt for ideas-08.json

**Save ChatGPT reply as:** test/project-ideas/ideas-08.json

| Meta | Value |
|------|-------|
| idea number | 08 |
| prodid | 51 |
| category_slug | hardware |
| product_name | Smart Rain-Activated Car Wiper |
| DB status | already-enriched (optional re-gen) |

---

## Copy everything below this line into ChatGPT

---

You are writing the full product-detail content for one HandMadeProjects catalog page.

### Project identity (do not change)
- product_name: Smart Rain-Activated Car Wiper
- prodid: 51
- category_slug: hardware

### Existing site context (use as grounding; expand into full professional detail)
- highlighttitle: Automatically activates car wipers using rain detection for safer and convenient driving.
- prodtags: Rain Sensor, Arduino Nano, Servo Motor, Automated Wipers, Embedded C, Analog Sensing, PWM Control, Automotive Electronics, Weather Detection, Driver Assistance, Mechatronics, Smart Car System, Real-time Monitoring, Prototype Development, Safety Device, Automation
- existing short text: Tech Embedded Systems, Sensor Integration, Mechatronics, Pulse Width Modulation (PWM), Analog-to-Digital Conversion Abstract The Smart Rain-Activated Car Wiper project focuses on creating an automated windshield cleaning system using affordable electronic components and a microcontroller. The system employs a rain sensor to detect moisture levels on the windshield, which triggers a servo motor to actuate the wiper arm. An Arduino Nano serves as the central processing unit, interpreting analog signals from the sensor and converting them into precise angular movements for the servo. To enhance driver awareness, the system integrates LED indicators and a buzzer that provide visual and audio alerts upon rain detection. The design also incorporates a periodic wiping function to maintain visibility during light drizzle or dew. This prototype serves as a practical demonstration of automation in…

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
- Be specific to **Smart Rain-Activated Car Wiper** — avoid copy-paste generic IoT fluff.
- Include prodid=51 and category_slug="hardware" and product_name exactly as given.

After you produce the JSON, I will save it as ideas-08.json.
