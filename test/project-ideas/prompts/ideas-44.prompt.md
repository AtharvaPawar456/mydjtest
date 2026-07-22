# Prompt for ideas-44.json

**Save ChatGPT reply as:** test/project-ideas/ideas-44.json

| Meta | Value |
|------|-------|
| idea number | 44 |
| prodid | 56 |
| category_slug | simulation |
| product_name | Automated Parking Gate Controller |
| DB status | needs generation |

---

## Copy everything below this line into ChatGPT

---

You are writing the full product-detail content for one HandMadeProjects catalog page.

### Project identity (do not change)
- product_name: Automated Parking Gate Controller
- prodid: 56
- category_slug: simulation

### Existing site context (use as grounding; expand into full professional detail)
- highlighttitle: A simplified automated parking gate system simulated using Proteus, demonstrating basic sensor-actuator control.
- prodtags: Arduino Nano, Proteus Simulation, IR Sensor, Servo Motor, Parking System,  Automated Gate,  I2C LCD, Embedded System,  Microcontroller, Simulation Software,  Real-time Control.
- existing short text: Keywords: Arduino Nano, Proteus Simulation, IR Sensor, Servo Motor, Parking System, Automated Gate, I2C LCD, Embedded System, Microcontroller, Simulation Software, Real-time Control. Objective: This project aims to design and simulate a basic automated parking gate controller using an Arduino Nano within the Proteus simulation environment. The system will utilize infrared (IR) sensors to detect vehicle entry and exit, controlling a servo motor to open and close the gate accordingly. The current number of parked vehicles will be displayed on a 16x2 I2C LCD. This project focuses on demonstrating fundamental microcontroller programming, sensor integration, and actuator control within a simulated environment to provide a hands-on learning experience without the complexities of real-world hardware integration. Abstract: This mini-project presents a simulated automated parking gate system impl…

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
- Be specific to **Automated Parking Gate Controller** — avoid copy-paste generic IoT fluff.
- Include prodid=56 and category_slug="simulation" and product_name exactly as given.

After you produce the JSON, I will save it as ideas-44.json.
