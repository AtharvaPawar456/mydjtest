# Prompt for ideas-15.json

**Save ChatGPT reply as:** test/project-ideas/ideas-15.json

| Meta | Value |
|------|-------|
| idea number | 15 |
| prodid | 59 |
| category_slug | hardware |
| product_name | Smart Respiratory Monitoring System using IoT Sensors |
| DB status | already-enriched (optional re-gen) |

---

## Copy everything below this line into ChatGPT

---

You are writing the full product-detail content for one HandMadeProjects catalog page.

### Project identity (do not change)
- product_name: Smart Respiratory Monitoring System using IoT Sensors
- prodid: 59
- category_slug: hardware

### Existing site context (use as grounding; expand into full professional detail)
- highlighttitle: An advanced IoT-based healthcare device designed to monitor breathing patterns and environmental factors to detect respiratory abnormalities in real-time.
- prodtags: IoT Healthcare, Respiratory Monitoring, ESP32, Airflow Sensing, Remote Patient Monitoring, Biomedical Instrumentation, Arduino IDE, Cloud Dashboard, Health Informatics, Asthma Tracking, COPD Monitoring, Real-time Data Logging, Environmental Sensing, Wireless Health Monitoring, OLED Interface, Smart Health
- existing short text: Tech ESP32, Arduino IDE, Airflow Sensor, DHT11 Temperature and Humidity Sensor, OLED Display, Wi-Fi, IoT Dashboard, MQTT/HTTP Protocol Abstract The Smart Respiratory Monitoring System is an integrated IoT solution designed to track respiratory health by monitoring airflow and environmental conditions. Utilizing an ESP32 microcontroller, the system captures real-time data from an airflow sensor to analyze breathing rates and patterns, while a DHT11 sensor monitors ambient temperature and humidity, which are critical triggers for asthma and COPD patients. The collected data is processed locally and displayed on an OLED screen for immediate patient feedback, while simultaneously being transmitted via Wi-Fi to a cloud-based IoT dashboard for remote clinical monitoring. The objective is to provide a non-invasive, continuous monitoring tool that can alert healthcare providers to abnormal respi…

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
- Be specific to **Smart Respiratory Monitoring System using IoT Sensors** — avoid copy-paste generic IoT fluff.
- Include prodid=59 and category_slug="hardware" and product_name exactly as given.

After you produce the JSON, I will save it as ideas-15.json.
