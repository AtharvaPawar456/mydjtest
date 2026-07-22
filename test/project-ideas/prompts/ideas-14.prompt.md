# Prompt for ideas-14.json

**Save ChatGPT reply as:** test/project-ideas/ideas-14.json

| Meta | Value |
|------|-------|
| idea number | 14 |
| prodid | 58 |
| category_slug | hardware |
| product_name | AI-Based Fall Detection and Alert System for Senior Citizens |
| DB status | already-enriched (optional re-gen) |

---

## Copy everything below this line into ChatGPT

---

You are writing the full product-detail content for one HandMadeProjects catalog page.

### Project identity (do not change)
- product_name: AI-Based Fall Detection and Alert System for Senior Citizens
- prodid: 58
- category_slug: hardware

### Existing site context (use as grounding; expand into full professional detail)
- highlighttitle: A wearable safety device that detects sudden falls using motion sensors and automatically sends emergency notifications to caregivers.
- prodtags: ESP32, MPU6050, Fall Detection, Machine Learning, GPS Tracking, GSM Alert, Elderly Care, Wearable Technology, Inertial Measurement Unit, Healthcare IoT, Emergency Response, Accelerometer, Gyroscope, Remote Monitoring, Patient Safety, Cloud Integration
- existing short text: Tech ESP32, Arduino IDE, MPU6050 Accelerometer and Gyroscope, GPS Module, GSM Module, AI/ML Model, Cloud Platform Abstract This project presents an intelligent wearable system designed to enhance the safety of senior citizens by providing automated fall detection and emergency alerting. Utilizing an ESP32 microcontroller integrated with an MPU6050 inertial measurement unit, the system continuously monitors the wearer's orientation and acceleration. To minimize false alarms—a common failure in threshold-based systems—an AI/ML model is employed to analyze movement patterns and distinguish actual falls from activities of daily living (ADL). Upon detecting a fall, the system retrieves the precise location via a GPS module and transmits an emergency alert via a GSM module to designated caregivers. The integration of cloud connectivity allows for real-time monitoring and data logging, ensuring…

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
- Be specific to **AI-Based Fall Detection and Alert System for Senior Citizens** — avoid copy-paste generic IoT fluff.
- Include prodid=58 and category_slug="hardware" and product_name exactly as given.

After you produce the JSON, I will save it as ideas-14.json.
