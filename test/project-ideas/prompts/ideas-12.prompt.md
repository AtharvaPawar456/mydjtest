# Prompt for ideas-12.json

**Save ChatGPT reply as:** test/project-ideas/ideas-12.json

| Meta | Value |
|------|-------|
| idea number | 12 |
| prodid | 55 |
| category_slug | hardware |
| product_name | BLE-Controlled Smart Car Using ESP32 |
| DB status | already-enriched (optional re-gen) |

---

## Copy everything below this line into ChatGPT

---

You are writing the full product-detail content for one HandMadeProjects catalog page.

### Project identity (do not change)
- product_name: BLE-Controlled Smart Car Using ESP32
- prodid: 55
- category_slug: hardware

### Existing site context (use as grounding; expand into full professional detail)
- highlighttitle: A four-wheel car controlled via mobile Bluetooth using ESP32 for wireless navigation.
- prodtags: ESP32, Bluetooth Low Energy, BLE, Motor Driver, L298N, DC Gear Motors, Wireless Control, IoT, Smart Vehicle, Robotics, Embedded Systems, Mobile App Control, H-Bridge, PWM Control, Arduino IDE, Remote Navigation
- existing short text: Tech ESP32, Bluetooth Low Energy (BLE), L298N Motor Driver, DC Gear Motors, Mobile Application Abstract This project focuses on the design and implementation of a BLE-controlled smart car utilizing the ESP32 microcontroller. The primary objective is to create a low-cost, compact robotic vehicle capable of wireless navigation via a mobile device. By leveraging Bluetooth Low Energy (BLE), the system establishes a stable, low-power communication link between a smartphone application and the vehicle. The ESP32 processes incoming wireless commands to actuate a four-wheel drive system through an H-bridge motor driver, enabling precise movements such as forward, backward, and directional turns. Integrated LEDs provide real-time operational status indicators. The outcome is a functional educational platform that demonstrates the integration of embedded systems, wireless protocols, and basic robo…

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
- Be specific to **BLE-Controlled Smart Car Using ESP32** — avoid copy-paste generic IoT fluff.
- Include prodid=55 and category_slug="hardware" and product_name exactly as given.

After you produce the JSON, I will save it as ideas-12.json.
