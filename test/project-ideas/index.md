# Project ideas index (manual ChatGPT generation)

Save each ChatGPT JSON reply as ideas-<NN>.json in this folder (zero-padded).

| # | File | prodid | category | status | Project |
|---|------|--------|----------|--------|---------|
| 01 | ideas-01.json | 44 | hardware | already-enriched (optional re-gen) | Smart Gas Leakage Detector with Safety Alert System |
| 02 | ideas-02.json | 45 | hardware | already-enriched (optional re-gen) | Smart Plant Irrigation and Humidity Control System |
| 03 | ideas-03.json | 46 | hardware | already-enriched (optional re-gen) | Smart Automatic Street Light System |
| 04 | ideas-04.json | 47 | hardware | already-enriched (optional re-gen) | Smart 1-Axis Solar Tracker System |
| 05 | ideas-05.json | 48 | hardware | already-enriched (optional re-gen) | Smart Dual-Axis Solar Tracker System |
| 06 | ideas-06.json | 49 | hardware | already-enriched (optional re-gen) | Smart Touchless Water Dispenser |
| 07 | ideas-07.json | 50 | hardware | already-enriched (optional re-gen) | Smart Water Level Indicator Using Arduino |
| 08 | ideas-08.json | 51 | hardware | already-enriched (optional re-gen) | Smart Rain-Activated Car Wiper |
| 09 | ideas-09.json | 52 | hardware | already-enriched (optional re-gen) | Smart Staircase Lighting System |
| 10 | ideas-10.json | 53 | hardware | already-enriched (optional re-gen) | Mini Wireless Power Transfer Module |
| 11 | ideas-11.json | 54 | hardware | already-enriched (optional re-gen) | LiFi Audio Transmission Mini System |
| 12 | ideas-12.json | 55 | hardware | already-enriched (optional re-gen) | BLE-Controlled Smart Car Using ESP32 |
| 13 | ideas-13.json | 57 | hardware | already-enriched (optional re-gen) | AI-Based Smart Medicine Reminder and Dispensing System |
| 14 | ideas-14.json | 58 | hardware | already-enriched (optional re-gen) | AI-Based Fall Detection and Alert System for Senior Citizens |
| 15 | ideas-15.json | 59 | hardware | already-enriched (optional re-gen) | Smart Respiratory Monitoring System using IoT Sensors |
| 16 | ideas-16.json | 60 | hardware | already-enriched (optional re-gen) | Smart Soil Quality Analysis and Automated Fertilizer Recommendation System |
| 17 | ideas-17.json | 61 | hardware | already-enriched (optional re-gen) | IoT-Based Smart Greenhouse Monitoring and Climate Control System |
| 18 | ideas-18.json | 62 | hardware | already-enriched (optional re-gen) | Automated Seed Sowing Robot for Precision Farming |
| 19 | ideas-19.json | 63 | hardware | needs generation | Smart Agricultural Weather Prediction and Decision Support System |
| 20 | ideas-20.json | 64 | hardware | needs generation | Smart Kitchen Safety Monitoring and Automation System |
| 21 | ideas-21.json | 65 | hardware | needs generation | Smart Waste Segregation System for Residential Applications |
| 22 | ideas-22.json | 66 | hardware | needs generation | Smart Water Consumption Monitoring System for Homes |
| 23 | ideas-23.json | 67 | hardware | needs generation | Autonomous Fire Detection and Rescue Robot |
| 24 | ideas-24.json | 68 | hardware | needs generation | Hybrid Renewable Energy Monitoring and Control System |
| 25 | ideas-25.json | 69 | hardware | needs generation | Smart Parking Slot Detection and Reservation System |
| 26 | ideas-26.json | 70 | hardware | needs generation | IoT-Based Smart Street Lighting with Adaptive Control |
| 27 | ideas-27.json | 71 | hardware | needs generation | Smart Pollution Monitoring and Prediction System |
| 28 | ideas-28.json | 72 | hardware | needs generation | Automated Inventory Management System using RFID and IoT |
| 29 | ideas-29.json | 73 | hardware | needs generation | IoT-Based Noise Pollution Monitoring System |
| 30 | ideas-30.json | 74 | hardware | needs generation | Smart Forest Fire Detection and Alert System |
| 31 | ideas-31.json | 75 | hardware | needs generation | Smart RFID-Based Attendance and Access Management System |
| 32 | ideas-32.json | 76 | hardware | needs generation | IoT-Based Smart Locker System with Remote Access |
| 33 | ideas-33.json | 77 | hardware | needs generation | Smart Wearable Navigation Assistant for Blind People |
| 34 | ideas-34.json | 78 | hardware | needs generation | Smart IV Drip Rate Monitoring and Alert System |
| 35 | ideas-35.json | 79 | hardware | needs generation | Wearable Health Vitals Monitoring Band with Emergency SOS |
| 36 | ideas-36.json | 80 | hardware | needs generation | Automated Poultry Farm Climate and Feed Monitoring System |
| 37 | ideas-37.json | 81 | hardware | needs generation | Smart Drip Irrigation Control System based on Soil Moisture and Weather Forecast |
| 38 | ideas-38.json | 82 | hardware | needs generation | IoT-Based Smart Fire Extinguisher Cabinet with Auto Alert |
| 39 | ideas-39.json | 83 | hardware | needs generation | Smart Home Intrusion Detection and Automated Response System |
| 40 | ideas-40.json | 84 | hardware | needs generation | Solar-Powered Smart Dustbin with Fill-Level Monitoring |
| 41 | ideas-41.json | 85 | hardware | needs generation | IoT-Based Smart Helmet for Rider Safety and Accident Alert |
| 42 | ideas-42.json | 86 | hardware | needs generation | Smart Library Book Tracking and Automated Return System using RFID |
| 43 | ideas-43.json | 87 | hardware | needs generation | AI-Based Smart Traffic Signal Control System for Congestion Management |
| 44 | ideas-44.json | 56 | simulation | needs generation | Automated Parking Gate Controller |

## How to use

1. Open _SYSTEM_PROMPT.md once and paste into ChatGPT custom instructions (optional but helps).
2. Open prompts/ideas-NN.prompt.md, copy the block under **Copy everything below**.
3. Paste into ChatGPT → get JSON → overwrite ideas-NN.json (remove _todo placeholders).
4. When ready: python test/project-ideas/apply_ideas_json.py (or --only 07).

## Needs generation first (skip already-enriched if you want)

- **19** — prodid 63 — Smart Agricultural Weather Prediction and Decision Support System
- **20** — prodid 64 — Smart Kitchen Safety Monitoring and Automation System
- **21** — prodid 65 — Smart Waste Segregation System for Residential Applications
- **22** — prodid 66 — Smart Water Consumption Monitoring System for Homes
- **23** — prodid 67 — Autonomous Fire Detection and Rescue Robot
- **24** — prodid 68 — Hybrid Renewable Energy Monitoring and Control System
- **25** — prodid 69 — Smart Parking Slot Detection and Reservation System
- **26** — prodid 70 — IoT-Based Smart Street Lighting with Adaptive Control
- **27** — prodid 71 — Smart Pollution Monitoring and Prediction System
- **28** — prodid 72 — Automated Inventory Management System using RFID and IoT
- **29** — prodid 73 — IoT-Based Noise Pollution Monitoring System
- **30** — prodid 74 — Smart Forest Fire Detection and Alert System
- **31** — prodid 75 — Smart RFID-Based Attendance and Access Management System
- **32** — prodid 76 — IoT-Based Smart Locker System with Remote Access
- **33** — prodid 77 — Smart Wearable Navigation Assistant for Blind People
- **34** — prodid 78 — Smart IV Drip Rate Monitoring and Alert System
- **35** — prodid 79 — Wearable Health Vitals Monitoring Band with Emergency SOS
- **36** — prodid 80 — Automated Poultry Farm Climate and Feed Monitoring System
- **37** — prodid 81 — Smart Drip Irrigation Control System based on Soil Moisture and Weather Forecast
- **38** — prodid 82 — IoT-Based Smart Fire Extinguisher Cabinet with Auto Alert
- **39** — prodid 83 — Smart Home Intrusion Detection and Automated Response System
- **40** — prodid 84 — Solar-Powered Smart Dustbin with Fill-Level Monitoring
- **41** — prodid 85 — IoT-Based Smart Helmet for Rider Safety and Accident Alert
- **42** — prodid 86 — Smart Library Book Tracking and Automated Return System using RFID
- **43** — prodid 87 — AI-Based Smart Traffic Signal Control System for Congestion Management
- **44** — prodid 56 — Automated Parking Gate Controller
