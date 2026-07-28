"""
Seed data for the July/Aug 2026 hardware project idea shortlist (projectdetails.txt).
Used by the `seed_new_project_ideas` management command.
"""

DEFAULT_IMG = "https://raw.githubusercontent.com/AtharvaPawar456/HandMadeProjects/refs/heads/main/siteimages/promoimg.png"

PRODINFO_TEMPLATE = """<div class="py-8 text-gray-900 font-sans bg-white">
  <h2 class="text-lg font-bold text-gray-800 border-b border-gray-300 pb-1">Project Name</h2>
  <p class="mt-2 text-gray-800">{title}</p>

  <h2 class="text-lg font-bold text-gray-800 border-b border-gray-300 pb-1 mt-6">Description</h2>
  <p class="mt-2 text-gray-800">{description}</p>

  <h2 class="text-lg font-bold text-gray-800 border-b border-gray-300 pb-1 mt-6">Technologies</h2>
  <p class="mt-2 text-gray-800">{technologies}</p>

  <h2 class="text-lg font-bold text-gray-800 border-b border-gray-300 pb-1 mt-6">Applications</h2>
  <p class="mt-2 text-gray-800">{applications}</p>

  <h2 class="text-lg font-bold text-gray-800 border-b border-gray-300 pb-1 mt-6">Report Contents</h2>
  <ul class="list-disc pl-5 mt-2 text-gray-800 space-y-1">
    <li>Components List (BOM: Bill of Material)</li>
    <li>Block Diagram</li>
    <li>Flow Chart</li>
    <li>Components : Name, Images, Details</li>
    <li>Circuit Diagram</li>
    <li>Problem Statement</li>
    <li>Abstract</li>
    <li>Introduction</li>
    <li>Methodology</li>
    <li>Challenges and Solutions</li>
    <li>Performance Analysis</li>
    <li>Advantages</li>
    <li>Limitation</li>
    <li>Application</li>
    <li>Future Scope</li>
    <li>Conclusion</li>
    <li>Output Images</li>
  </ul>

  <h2 class="text-lg font-bold text-gray-800 border-b border-gray-300 pb-1 mt-6">Project Deliverables</h2>
  <ul class="list-disc pl-5 mt-2 text-gray-800 space-y-1">
    <li>Project Hardware</li>
    <li>Project Report</li>
    <li>Project Simulation</li>
  </ul>
</div>"""


# (title, description, technologies, applications)
IDEAS = [
    (
        "AI-Based Smart Medicine Reminder and Dispensing System",
        "An automated medicine management system that reminds users about medicine schedules and dispenses tablets automatically according to predefined timings. It reduces medication errors and helps elderly patients maintain proper medication routines.",
        "ESP32/Arduino, Arduino IDE, RTC module (DS3231), servo motor, LCD/OLED display, buzzer, keypad, IoT cloud platform",
        "Hospitals, elderly homes, personal healthcare",
    ),
    (
        "AI-Based Fall Detection and Alert System for Senior Citizens",
        "A wearable safety device that detects sudden falls using motion sensors and automatically sends emergency notifications to caregivers. AI algorithms improve detection accuracy by analyzing movement patterns.",
        "ESP32, Arduino IDE, MPU6050 sensor, GPS module, GSM module, AI/ML model, cloud platform",
        "Elderly safety, healthcare monitoring, emergency response",
    ),
    (
        "Smart Respiratory Monitoring System using IoT Sensors",
        "A device that monitors breathing patterns and respiratory conditions using environmental and body sensors. It helps detect abnormal breathing conditions and provides alerts.",
        "ESP32, Arduino IDE, airflow sensor, temperature sensor, humidity sensor, OLED display, Wi-Fi, IoT dashboard",
        "Respiratory disease monitoring, healthcare systems",
    ),
    (
        "Smart Soil Quality Analysis and Automated Fertilizer Recommendation System",
        "A farming assistant that analyzes soil conditions such as moisture, pH, and nutrient levels. Based on collected data, it suggests suitable fertilizer requirements.",
        "ESP32, Arduino IDE, soil moisture sensor, pH sensor, NPK sensor, OLED display, Wi-Fi, cloud dashboard",
        "Smart farming, crop management",
    ),
    (
        "IoT-Based Smart Greenhouse Monitoring and Climate Control System",
        "A greenhouse automation system that maintains suitable plant growth conditions by monitoring temperature, humidity, and soil moisture. It automatically controls fans, pumps, and lights.",
        "ESP32, Arduino IDE, DHT22 sensor, soil moisture sensor, relay module, water pump, LDR sensor, IoT dashboard",
        "Commercial farming, research greenhouses",
    ),
    (
        "Automated Seed Sowing Robot for Precision Farming",
        "A robotic farming machine that automatically plants seeds at predefined distances and depths. It reduces manual effort and improves farming efficiency.",
        "Arduino Mega/ESP32, Arduino IDE, motor drivers, DC motors, ultrasonic sensors, servo motors, GPS module",
        "Agricultural automation",
    ),
    (
        "Smart Agricultural Weather Prediction and Decision Support System",
        "A weather monitoring system that collects environmental data and predicts farming conditions. Farmers receive recommendations for irrigation and crop protection.",
        "ESP32, Arduino IDE, temperature sensor, humidity sensor, rain sensor, pressure sensor, cloud analytics",
        "Weather-based farming decisions",
    ),
    (
        "Smart Kitchen Safety Monitoring and Automation System",
        "A kitchen safety system that detects gas leakage, fire hazards, and abnormal temperature conditions. It automatically triggers alerts and safety actions.",
        "ESP32, Arduino IDE, MQ gas sensor, flame sensor, temperature sensor, buzzer, relay module, GSM/Wi-Fi",
        "Residential kitchens, restaurants",
    ),
    (
        "Smart Waste Segregation System for Residential Applications",
        "An automated waste management system that identifies and separates different types of waste such as dry and wet waste. It reduces manual sorting effort and improves recycling efficiency.",
        "ESP32, Arduino IDE, IR sensor, moisture sensor, ultrasonic sensor, servo motor, conveyor mechanism, camera module",
        "Smart homes, municipal waste management",
    ),
    (
        "Smart Water Consumption Monitoring System for Homes",
        "A water management system that measures household water usage and detects wastage. Users can monitor consumption data through a mobile or web dashboard.",
        "ESP32, Arduino IDE, water flow sensor, ultrasonic level sensor, solenoid valve, LCD display, IoT cloud platform",
        "Smart homes, water conservation",
    ),
    (
        "Autonomous Fire Detection and Rescue Robot",
        "A robot that detects fire locations and assists in emergency situations. It can navigate toward fire sources and activate extinguishing mechanisms.",
        "ESP32, Arduino IDE, flame sensor, temperature sensor, gas sensor, water pump, servo motor, camera module",
        "Industrial safety, fire emergency systems",
    ),
    (
        "Hybrid Renewable Energy Monitoring and Control System",
        "A system that monitors and manages multiple renewable energy sources such as solar and wind. It optimizes power generation and usage.",
        "ESP32, Arduino IDE, voltage/current sensors, solar panel, wind sensor, relay modules, LCD display, cloud monitoring",
        "Renewable energy projects, smart grids",
    ),
    (
        "Smart Parking Slot Detection and Reservation System",
        "An automated parking management system that detects available parking spaces and allows users to reserve slots through a mobile/web application. It reduces searching time and improves parking management.",
        "ESP32, Arduino IDE, ultrasonic sensors, IR sensors, RFID module, LCD display, Wi-Fi, Firebase/Blynk",
        "Shopping malls, offices, smart city parking",
    ),
    (
        "IoT-Based Smart Street Lighting with Adaptive Control",
        "A smart lighting system that automatically adjusts street light intensity according to vehicle movement and environmental conditions. It saves electricity by reducing unnecessary power consumption.",
        "ESP32, Arduino IDE, LDR sensor, PIR sensor, LED drivers, relay module, current sensor, IoT cloud",
        "Roads, highways, smart city infrastructure",
    ),
    (
        "Smart Pollution Monitoring and Prediction System",
        "A monitoring device that measures air quality parameters and predicts pollution levels using data analysis. It helps authorities and citizens understand environmental conditions.",
        "ESP32, Arduino IDE, MQ135 gas sensor, CO2 sensor, dust sensor, temperature sensor, humidity sensor, IoT cloud",
        "Environmental monitoring, smart cities",
    ),
    (
        "Automated Inventory Management System using RFID and IoT",
        "A smart inventory tracking system that automatically records product movement and stock levels using RFID technology. It reduces manual inventory management.",
        "ESP32, Arduino IDE, RFID reader, RFID tags, barcode scanner, OLED display, database, Wi-Fi",
        "Warehouses, retail stores",
    ),
    (
        "IoT-Based Noise Pollution Monitoring System",
        "A monitoring device that measures surrounding noise levels and stores environmental data. It helps identify high-noise areas and supports pollution control.",
        "ESP32, Arduino IDE, sound sensor, microphone module, OLED display, Wi-Fi, cloud database",
        "Cities, industrial zones, schools",
    ),
    (
        "Smart Forest Fire Detection and Alert System",
        "A remote monitoring system that detects forest fire conditions at an early stage and sends alerts to authorities. It helps reduce damage caused by wildfires.",
        "ESP32, Arduino IDE, temperature sensor, smoke sensor, flame sensor, GPS module, LoRa/GSM communication",
        "Forest monitoring, disaster management",
    ),
    (
        "Smart RFID-Based Attendance and Access Management System",
        "An automated attendance and security system that uses RFID cards for identification and access control. Records are stored digitally for monitoring.",
        "ESP32, Arduino IDE, RFID reader, RFID tags, LCD display, servo lock, Wi-Fi, database",
        "Schools, offices, industries",
    ),
    (
        "IoT-Based Smart Locker System with Remote Access",
        "A secure smart locker that allows users to lock/unlock remotely using authentication methods. It provides improved security compared to traditional lockers.",
        "ESP32, Arduino IDE, RFID module, fingerprint sensor, servo motor, keypad, mobile application",
        "Banks, offices, smart homes",
    ),
    (
        "Smart Wearable Navigation Assistant for Blind People",
        "A wearable device that assists visually impaired people by detecting obstacles and providing audio navigation guidance.",
        "ESP32, Arduino IDE, ultrasonic sensor, GPS module, audio module, vibration motor, Bluetooth",
        "Assistive technology, smart mobility",
    ),
    # --- Shortlist extension (Aug 2026) ---
    (
        "Smart IV Drip Rate Monitoring and Alert System",
        "A hospital-assist device that monitors intravenous drip rate and fluid level in real time, alerting nursing staff before a bottle runs empty or the flow rate drifts from the prescribed value.",
        "ESP32, Arduino IDE, IR drop-counter sensor, load cell, LCD/OLED display, buzzer, Wi-Fi, IoT dashboard",
        "Hospitals, ICUs, home healthcare",
    ),
    (
        "Wearable Health Vitals Monitoring Band with Emergency SOS",
        "A wrist-worn band that continuously tracks heart rate, SpO2 and body temperature, and sends an emergency alert with GPS location to a caregiver when vitals cross a safe threshold or the wearer presses an SOS button.",
        "ESP32, Arduino IDE, MAX30100/MAX30102 sensor, body temperature sensor, GPS module, GSM/Bluetooth, mobile app",
        "Personal healthcare, elderly monitoring, fitness tracking",
    ),
    (
        "Automated Poultry Farm Climate and Feed Monitoring System",
        "A farm automation system that tracks shed temperature, humidity and ammonia levels while automating feed and water dispensing on a schedule, reducing manual labor and improving bird health outcomes.",
        "ESP32, Arduino IDE, DHT22 sensor, MQ135 gas sensor, servo/motor-driven feeder, relay module, IoT dashboard",
        "Poultry farms, livestock management",
    ),
    (
        "Smart Drip Irrigation Control System based on Soil Moisture and Weather Forecast",
        "An irrigation controller that combines live soil-moisture readings with online weather forecast data to schedule watering cycles automatically, cutting water waste compared to timer-only irrigation.",
        "ESP32, Arduino IDE, soil moisture sensor, solenoid valve, relay module, Wi-Fi, weather API, cloud dashboard",
        "Precision agriculture, home gardens, nurseries",
    ),
    (
        "IoT-Based Smart Fire Extinguisher Cabinet with Auto Alert",
        "A monitored cabinet that checks extinguisher presence, pressure and tamper status, sending an instant alert to facility managers if a unit is missing, low on pressure, or removed without authorization.",
        "ESP32, Arduino IDE, pressure sensor, IR/weight sensor, RFID tag, buzzer, GSM/Wi-Fi, cloud dashboard",
        "Factories, offices, public buildings, fire safety compliance",
    ),
    (
        "Smart Home Intrusion Detection and Automated Response System",
        "A layered home-security system that fuses door/window sensors, PIR motion detection and camera triggers to detect intrusions, automatically locking doors, sounding alarms and notifying the homeowner's phone.",
        "ESP32, Arduino IDE, PIR sensor, magnetic door/window sensor, camera module, relay-controlled lock, GSM/Wi-Fi, mobile app",
        "Smart homes, residential security",
    ),
    (
        "Solar-Powered Smart Dustbin with Fill-Level Monitoring",
        "A solar-charged public dustbin that measures fill level with an ultrasonic sensor and reports status to a municipal dashboard, so collection routes only visit bins that are actually full.",
        "ESP32, Arduino IDE, ultrasonic sensor, solar panel, battery + charge controller, GSM/Wi-Fi, IoT dashboard",
        "Smart cities, municipal waste collection",
    ),
    (
        "IoT-Based Smart Helmet for Rider Safety and Accident Alert",
        "A two-wheeler helmet that checks for helmet-wear and alcohol before allowing ignition, and automatically sends an accident alert with GPS coordinates to emergency contacts if a crash is detected.",
        "ESP32, Arduino IDE, MPU6050 accelerometer, alcohol (MQ3) sensor, IR wear-detection sensor, GPS module, GSM module",
        "Road safety, two-wheeler rider protection",
    ),
    (
        "Smart Library Book Tracking and Automated Return System using RFID",
        "A library automation system that tags books with RFID for instant issue/return logging and shelf-location tracking, reducing manual bookkeeping and helping locate misplaced books quickly.",
        "ESP32, Arduino IDE, RFID reader, RFID tags, OLED display, database, Wi-Fi",
        "School and college libraries, public libraries",
    ),
    (
        "AI-Based Smart Traffic Signal Control System for Congestion Management",
        "An adaptive traffic signal controller that uses live vehicle-density sensing to adjust green-light duration per lane in real time, reducing average wait times at congested intersections compared to fixed-timer signals.",
        "ESP32, Arduino IDE, IR/ultrasonic vehicle sensors, camera module, AI/ML density model, relay-driven signal lights, cloud analytics",
        "Smart city traffic management, congested urban intersections",
    ),
]


def _highlight(description):
    first_sentence = description.split(". ")[0].strip()
    if not first_sentence.endswith("."):
        first_sentence += "."
    return first_sentence


def _tags(technologies, applications):
    tech_parts = [t.strip() for t in technologies.split(",") if t.strip()]
    app_parts = [a.strip() for a in applications.split(",") if a.strip()]
    return ", ".join(tech_parts + app_parts)


def product_payload(idea, category=None):
    title, description, technologies, applications = idea
    data = {
        "productname": title,
        "productcat": "hardware",
        "mainimgbasetxt": DEFAULT_IMG,
        "prodtags": _tags(technologies, applications),
        "prodcost": "*",
        "highlighttitle": _highlight(description),
        "prodinfo": PRODINFO_TEMPLATE.format(
            title=title,
            description=description,
            technologies=technologies,
            applications=applications,
        ),
        "gallery": "*",
        "ytlinks": "*",
        "documents": "*",
    }
    if category is not None:
        data["category"] = category
        data["productcat"] = category.slug
    return data
