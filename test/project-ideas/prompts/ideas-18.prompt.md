# Prompt for ideas-18.json

**Save ChatGPT reply as:** test/project-ideas/ideas-18.json

| Meta | Value |
|------|-------|
| idea number | 18 |
| prodid | 62 |
| category_slug | hardware |
| product_name | Automated Seed Sowing Robot for Precision Farming |
| DB status | already-enriched (optional re-gen) |

---

## Copy everything below this line into ChatGPT

---

You are writing the full product-detail content for one HandMadeProjects catalog page.

### Project identity (do not change)
- product_name: Automated Seed Sowing Robot for Precision Farming
- prodid: 62
- category_slug: hardware

### Existing site context (use as grounding; expand into full professional detail)
- highlighttitle: A robotic farming machine that automatically plants seeds at predefined distances and depths to reduce manual effort and improve farming efficiency.
- prodtags: Precision Farming, Agricultural Robotics, Automated Sowing, Arduino Mega, ESP32, Seed Dispenser, Autonomous Navigation, GPS Tracking, Ultrasonic Sensing, Motor Control, Smart Agriculture, Agri-Tech, Embedded Systems, Crop Optimization, Robotic Chassis, Servo Mechanism
- existing short text: Tech Arduino Mega/ESP32, Arduino IDE, L298N Motor Drivers, DC Gear Motors, Ultrasonic Sensors, Servo Motors, GPS Module, Agricultural Automation Abstract The Automated Seed Sowing Robot is designed to modernize traditional planting methods by introducing precision and automation into the sowing process. The system utilizes an Arduino Mega/ESP32 microcontroller to coordinate the movement of a mobile chassis and a seed dispensing mechanism. By integrating ultrasonic sensors for obstacle avoidance and a GPS module for spatial tracking, the robot ensures that seeds are planted at consistent intervals and specific depths, minimizing seed wastage and optimizing crop yield. The mechanism employs a servo-controlled hopper to release seeds precisely. This project aims to bridge the gap between manual labor-intensive farming and high-cost industrial machinery, providing a scalable, low-cost soluti…

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
- Be specific to **Automated Seed Sowing Robot for Precision Farming** — avoid copy-paste generic IoT fluff.
- Include prodid=62 and category_slug="hardware" and product_name exactly as given.

After you produce the JSON, I will save it as ideas-18.json.
