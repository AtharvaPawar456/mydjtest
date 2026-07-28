"""Directory shop seed data (Task 3 I1). Used by management command."""

def _img(label: str, color: str = "4f46e5") -> str:
    text = label.replace(" ", "+").replace("&", "and")
    return f"https://placehold.co/960x600/{color}/ffffff?text={text}"


SHOPS = [
    {
        "bname": "Circuit-Craft-Lab",
        "bcat": "Electronics & components",
        "btags": "arduino, esp32, sensors, iot, components, student-kits",
        "bhighlight": "Arduino, ESP32, sensors & starter kits for college projects.",
        "binfo": "<p>Campus-friendly electronics counter for makers building IoT and final-year hardware projects.</p><ul><li>Dev boards & sensors</li><li>Starter kits</li><li>Project part lists</li></ul>",
        "color": "2563eb",
    },
    {
        "bname": "PCB-Prototyping-Hub",
        "bcat": "Hardware services",
        "btags": "pcb, prototype, assembly, hardware, fabrication",
        "bhighlight": "Fast PCB prototype & assembly guidance for final-year teams.",
        "binfo": "<p>Turn schematics into boards with prototyping guidance and assembly tips for student teams.</p>",
        "color": "ea580c",
    },
    {
        "bname": "3D-Print-Works",
        "bcat": "Digital fabrication",
        "btags": "3d-print, pla, abs, enclosures, mechanical",
        "bhighlight": "PLA/ABS prints, enclosures, and project casings.",
        "binfo": "<p>Print custom enclosures and mechanical parts for robotics and product mockups.</p>",
        "color": "059669",
    },
    {
        "bname": "Robotics-Garage",
        "bcat": "Education / robotics",
        "btags": "robotics, workshop, kits, stem, weekend-lab",
        "bhighlight": "Weekend robotics labs for school & engineering students.",
        "binfo": "<p>Hands-on robotics workshops with kits, mentors, and demo-ready builds.</p>",
        "color": "7c3aed",
    },
    {
        "bname": "EmbedLab-Studio",
        "bcat": "Embedded systems",
        "btags": "stm32, raspberry-pi, embedded, firmware, mentorship",
        "bhighlight": "Mentored embedded builds with demo-ready documentation.",
        "binfo": "<p>Embedded systems studio for firmware, sensors, and polished project documentation.</p>",
        "color": "0f766e",
    },
    {
        "bname": "PixelPrompt-AI",
        "bcat": "AI content studio",
        "btags": "ai, product-photos, banners, social, creatives",
        "bhighlight": "Product photos, banners & social creatives for local brands.",
        "binfo": "<p>AI content packs for e-commerce listings, ads, and social campaigns.</p>",
        "color": "db2777",
    },
    {
        "bname": "CodeMentor-Desk",
        "bcat": "EdTech / mentoring",
        "btags": "django, ml, mentoring, code-review, students",
        "bhighlight": "Doubt-solving & project review for Django, ML & web apps.",
        "binfo": "<p>1:1 and small-group mentoring for software project delivery and viva prep.</p>",
        "color": "4f46e5",
    },
    {
        "bname": "WebCraft-MiniSites",
        "bcat": "Web design",
        "btags": "landing-page, web, small-business, portfolio",
        "bhighlight": "Launch a clean one-page site for your shop in days.",
        "binfo": "<p>Single-page websites for local businesses and student portfolios.</p>",
        "color": "0284c7",
    },
    {
        "bname": "DataStory-Charts",
        "bcat": "Analytics freelancers",
        "btags": "dashboards, sheets, analytics, campus-clubs",
        "bhighlight": "Simple dashboards & report packs for campus clubs.",
        "binfo": "<p>Lightweight analytics and chart packs for events, clubs, and small teams.</p>",
        "color": "ca8a04",
    },
    {
        "bname": "Resume-Forge-Studio",
        "bcat": "Career services",
        "btags": "resume, portfolio, github, placements",
        "bhighlight": "Project-first resumes and GitHub portfolio polish.",
        "binfo": "<p>Career studio focused on project storytelling for placements and internships.</p>",
        "color": "334155",
    },
    {
        "bname": "Campus-Print-Point",
        "bcat": "Printing & binding",
        "btags": "print, thesis, posters, binding, campus",
        "bhighlight": "Project reports, posters & thesis binding near campus.",
        "binfo": "<p>Print shop for reports, posters, and final submission packs.</p>",
        "color": "64748b",
    },
    {
        "bname": "Maker-Cafe-Collab",
        "bcat": "Co-working / cafe",
        "btags": "coworking, cafe, whiteboards, team-meet",
        "bhighlight": "Wi-Fi, whiteboards & group project tables.",
        "binfo": "<p>Cafe + co-work tables for project groups and mentor sessions.</p>",
        "color": "b45309",
    },
    {
        "bname": "SkillSprint-Workshops",
        "bcat": "Training",
        "btags": "iot, python, tailwind, workshops, short-courses",
        "bhighlight": "Short courses: IoT basics, Python, UI with Tailwind.",
        "binfo": "<p>Sprint-style workshops for practical maker and web skills.</p>",
        "color": "9333ea",
    },
    {
        "bname": "Project-Docs-Desk",
        "bcat": "Documentation",
        "btags": "synopsis, ppt, demo-script, documentation",
        "bhighlight": "Synopsis, PPT & demo script writing support.",
        "binfo": "<p>Documentation desk for project reports, slides, and viva scripts.</p>",
        "color": "475569",
    },
    {
        "bname": "Internship-Connect-Desk",
        "bcat": "Career / internships",
        "btags": "internship, mock-interview, prep, career",
        "bhighlight": "Curated internship prep & mock interviews.",
        "binfo": "<p>Prep desk aligned with HandMadeProjects internship tracks.</p>",
        "color": "16a34a",
    },
    {
        "bname": "Hotel-Mauli-Dadar-East",
        "bcat": "Restaurant, Hotel",
        "btags": "hotel, restaurant, malvani, maharashtrian, dadar, hospitality",
        "bhighlight": "Authentic Malvani / Maharashtrian food. Veg / Non-Veg Family Hotel. Contact: 99303 28511 / 70397 64610",
        "binfo": (
            "<p><strong>Hotel Mauli (Dadar East)</strong> — family hotel serving authentic "
            "Malvani / Maharashtrian cuisine (veg &amp; non-veg).</p>"
            "<p><strong>Contact:</strong> 99303 28511 / 70397 64610</p>"
            "<p>Featured on HandMadeProjects as a local business showcase (AI content samples).</p>"
        ),
        # Prefer jsDelivr CDN (more reliable in browsers than raw.githubusercontent.com)
        "bmainimg": "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/assets/shops-section/shop-1-mauli/file_2.png",
        "bgallery": (
            "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/assets/shops-section/shop-1-mauli/file_5.jpeg;"
            "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/assets/shops-section/shop-1-mauli/file_11.jpeg;"
            "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/assets/shops-section/shop-1-mauli/file_4.jpeg;"
            "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/assets/shops-section/shop-1-mauli/file_1.jpeg;"
            "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/assets/shops-section/shop-1-mauli/file_10.png;"
            "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/assets/shops-section/shop-1-mauli/file_12.png;"
            "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/assets/shops-section/shop-1-mauli/file_3.jpeg;"
            "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/assets/shops-section/shop-1-mauli/file_6.png;"
            "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/assets/shops-section/shop-1-mauli/file_7.png;"
            "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/assets/shops-section/shop-1-mauli/file_8.jpeg;"
            "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/assets/shops-section/shop-1-mauli/file_9.jpeg;"
            "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/assets/shops-section/shop-1-mauli/videos/file_1.mp4;"
            "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/assets/shops-section/shop-1-mauli/videos/file_2.mp4;"
            "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/assets/shops-section/shop-1-mauli/videos/file_3.mp4;"
            "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/assets/shops-section/shop-1-mauli/videos/file_4.mp4;"
            "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/assets/shops-section/shop-1-mauli/videos/file_5.mp4;"
            "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/assets/shops-section/shop-1-mauli/videos/file_6.mp4"
        ),
        "color": "1e293b",
    },
    {
        "bname": "FreshBite-Tiffin",
        "bcat": "Food services",
        "btags": "tiffin, food, students, delivery",
        "bhighlight": "Homestyle tiffins for students & working professionals.",
        "binfo": "<p>Local tiffin service demo listing for student-heavy neighborhoods.</p>",
        "color": "dc2626",
    },
    {
        "bname": "BrightLook-Salon",
        "bcat": "Beauty / salon",
        "btags": "salon, grooming, festival-looks, ai-before-after",
        "bhighlight": "Grooming packages with festival-ready looks.",
        "binfo": "<p>Salon showcase suitable for AI before/after creative packs.</p>",
        "color": "e11d48",
    },
    {
        "bname": "QuickFix-Mobile-Care",
        "bcat": "Repair",
        "btags": "mobile-repair, screen, battery, same-day",
        "bhighlight": "Screen & battery repair with same-day options.",
        "binfo": "<p>Device repair counter popular with students and remote workers.</p>",
        "color": "0891b2",
    },
    {
        "bname": "GreenLeaf-Nursery",
        "bcat": "Lifestyle",
        "btags": "plants, nursery, hostel, desk-greenery",
        "bhighlight": "Indoor plants & desk greenery for hostels.",
        "binfo": "<p>Plant nursery listing with strong visual gallery potential.</p>",
        "color": "15803d",
    },
    {
        "bname": "Ganpati-Decor-Designs",
        "bcat": "Festival decoration",
        "btags": "ganpati, decoration, mandap, eco-friendly, traditional, LED, premium, Mumbai, seasonal, AI-designs",
        "bhighlight": "Browse 100+ Ganpati decoration design concepts—eco, traditional, LED & premium themes—then request a custom quote.",
        "binfo": (
            "<h3>About</h3><p>Design gallery for Ganpati decoration concepts—from eco home setups to premium mandaps. "
            "AI-assisted mockups help clients pick a theme before on-site execution.</p>"
            "<h3>Styles</h3><ul><li>Eco-friendly</li><li>Traditional</li><li>LED modern</li><li>Premium luxury</li>"
            "<li>Budget / hostel compact</li></ul>"
            "<h3>How to book</h3><p>Share preferred theme + space photos. Book 2–6 weeks before Chaturthi when possible.</p>"
            "<p><em>Gallery images may include AI concept art; final on-site materials can differ.</em></p>"
        ),
        "color": "f59e0b",
    },
    {
        "bname": "Festive-Lights-Co",
        "bcat": "Event lighting",
        "btags": "led, fairy-lights, stage, event-lighting",
        "bhighlight": "LED curtains, fairy lights & stage wash ideas.",
        "binfo": "<p>Event lighting concepts that pair with festival décor shops.</p>",
        "color": "fbbf24",
    },
    {
        "bname": "Mandap-Florals-Studio",
        "bcat": "Florals",
        "btags": "florals, mandap, marigold, artificial-flowers",
        "bhighlight": "Fresh & artificial floral themes for celebrations.",
        "binfo": "<p>Floral themes for mandaps, entrances, and home shrines.</p>",
        "color": "ec4899",
    },
    {
        "bname": "Eco-Idol-Concepts",
        "bcat": "Eco festival",
        "btags": "eco-idol, clay, sustainable, festival",
        "bhighlight": "Clay & eco-friendly idol presentation themes.",
        "binfo": "<p>Eco idol presentation and sustainable festival styling ideas.</p>",
        "color": "65a30d",
    },
    {
        "bname": "Event-Photo-Booth",
        "bcat": "Events / photo",
        "btags": "photobooth, backdrop, society-events, props",
        "bhighlight": "Backdrop & booth designs for society events.",
        "binfo": "<p>Photo booth and backdrop concepts for campus and society festivals.</p>",
        "color": "8b5cf6",
    },
    {
        "bname": "Drone-View-Media",
        "bcat": "Aerial media",
        "btags": "drone, aerial, media, mapping",
        "bhighlight": "Aerial media & campus mapping clips for demos and events.",
        "binfo": "<p>Drone media services bridging hardware interests and visual storytelling.</p>",
        "color": "0ea5e9",
    },
    {
        "bname": "Solar-Kit-India",
        "bcat": "Green energy",
        "btags": "solar, green-energy, kits, hardware",
        "bhighlight": "Student-friendly solar demo kits & green energy project ideas.",
        "binfo": "<p>Solar learning kits aligned with hardware and sustainability projects.</p>",
        "color": "facc15",
    },
    {
        "bname": "SmartHome-Installers",
        "bcat": "IoT services",
        "btags": "smarthome, install, mqtt, iot-services",
        "bhighlight": "Home automation install support for IoT project graduates.",
        "binfo": "<p>From student IoT kits to practical smart-home installation guidance.</p>",
        "color": "6366f1",
    },
    {
        "bname": "College-Merch-Press",
        "bcat": "Merch / print",
        "btags": "merch, tshirts, stickers, campus-clubs",
        "bhighlight": "Club merch, stickers & event print for campus teams.",
        "binfo": "<p>Merchandise press for college clubs and tech events.</p>",
        "color": "f43f5e",
    },
    {
        "bname": "Open-Source-Meetup",
        "bcat": "Community",
        "btags": "opensource, meetup, community, github",
        "bhighlight": "Community meetups for open-source contributors and student coders.",
        "binfo": "<p>Non-commercial community card for OSS learning circles and meetups.</p>",
        "color": "111827",
    },
    {
        "bname": "MacNet-Technology",
        "bcat": "Electronics & components",
        "btags": "robotics, electronics, motors, modules, components, Mumbai, Grant-Road, MacNet",
        "bhighlight": (
            "Robotics & electronics components, motors, modules & more. "
            "Contact: +91 90043 04565 (Manohar) · Grant Road, Mumbai."
        ),
        "binfo": (
            "<h3>About</h3>"
            "<p>MacNet Technology stocks a wide range of <strong>robotics and electronics components</strong> — "
            "motors, modules, sensors, boards and related parts for students, makers and project teams.</p>"
            "<h3>Contact</h3>"
            "<p><strong>Manohar</strong> — "
            "<a href=\"tel:+919004304565\">+91 90043 04565</a></p>"
            "<h3>Address</h3>"
            "<p>1st floor, Shree Ganesh Bhuvan, Police Station, 18, opp. Lamington Road, "
            "Krishna Kunj, Grant Road East, Shapur Baug, Grant Road, Mumbai, Maharashtra 400007</p>"
            "<p><em>Listed on HandMadeProjects as a local electronics &amp; robotics components partner.</em></p>"
        ),
        # Prefer jsDelivr CDN (more reliable in browsers than raw.githubusercontent.com)
        "bmainimg": "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/assets/shops-section/shop-2-macnet/file_1.jpeg",
        "bgallery": (
            "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/assets/shops-section/shop-2-macnet/file_1.jpeg;"
            "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/assets/shops-section/shop-2-macnet/file_2.jpeg;"
            "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/assets/shops-section/shop-2-macnet/file_3.jpeg;"
            "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/assets/shops-section/shop-2-macnet/file_4.jpeg;"
            "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/assets/shops-section/shop-2-macnet/file_5.jpeg"
        ),
        "color": "1d4ed8",
    },
    {
        "bname": "Yerunkar-Corner",
        "bcat": "Food dealer, Sweets & snacks",
        "btags": (
            "food, sweets, laddu, ladu, methi, besan, nachani, moong, "
            "mithai, Prabhadevi, Mumbai, Yerunkar, food-dealer"
        ),
        "bhighlight": (
            "Homestyle laddus — every type ₹30 each (80 g). Box of 12 = ₹360. "
            "Food dealer: Mr. Ganesh Yerunkar · +91 98694 32812 · Prabhadevi, Mumbai."
        ),
        "binfo": (
            "<h3>About</h3>"
            "<p><strong>Yerunkar Corner</strong> is a local food dealer from "
            "<strong>Prabhadevi, Mumbai</strong>, known for fresh, homemade-style "
            "<strong>laddus (लाडू)</strong>.</p>"
            "<h3>Food Dealer</h3>"
            "<p><strong>Mr. Ganesh Yerunkar</strong></p>"
            "<h3>Contact</h3>"
            "<p>"
            "<a href=\"tel:+919869432812\">+91 98694 32812</a>"
            " · "
            "<a href=\"https://wa.me/919869432812\" target=\"_blank\" rel=\"noopener noreferrer\">WhatsApp</a>"
            "</p>"
            "<h3>Location</h3>"
            "<p>Prabhadevi, Mumbai, India</p>"
            "<h3>Pricing (all laddu types)</h3>"
            "<ul>"
            "<li><strong>₹30</strong> per laddu</li>"
            "<li>Each laddu: <strong>80 grams</strong></li>"
            "<li>Box of 12: 12 × ₹30 = <strong>₹360</strong></li>"
            "</ul>"
            "<h3>Laddu menu / लाडू प्रकार</h3>"
            "<ul>"
            "<li><strong>मेथी लाडू</strong> — Methi Laddu (Fenugreek laddu)</li>"
            "<li><strong>बिगर मेथी लाडू</strong> — Bigar Methi Laddu (Plain / without methi laddu)</li>"
            "<li><strong>नाचणी लाडू</strong> — Nachani Laddu (Finger millet / ragi laddu)</li>"
            "<li><strong>मुग लाडू (साली सकट पौष्टिक लाडू)</strong> — Moong Laddu "
            "(nutritious moong dal laddu with skin / wholesome moong laddu)</li>"
            "<li><strong>बेसन लाडू</strong> — Besan Laddu (Gram flour laddu)</li>"
            "</ul>"
            "<p><em>Listed on HandMadeProjects as a local food &amp; sweets partner.</em></p>"
        ),
        "bmainimg": (
            "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/"
            "assets/shops-section/shop-3-yerunkar-corner/main.jpg"
        ),
        # New gallery only — old basan-ladu / rava-ladu images removed
        "bgallery": (
            "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/"
            "assets/shops-section/shop-3-yerunkar-corner/main.jpg;"
            "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/"
            "assets/shops-section/shop-3-yerunkar-corner/l1.jpg;"
            "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/"
            "assets/shops-section/shop-3-yerunkar-corner/l1p.jpg;"
            "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/"
            "assets/shops-section/shop-3-yerunkar-corner/l2.jpg;"
            "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/"
            "assets/shops-section/shop-3-yerunkar-corner/l2p.jpg;"
            "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/"
            "assets/shops-section/shop-3-yerunkar-corner/l3.jpg;"
            "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/"
            "assets/shops-section/shop-3-yerunkar-corner/l3p.jpg;"
            "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/"
            "assets/shops-section/shop-3-yerunkar-corner/l4.jpg;"
            "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/"
            "assets/shops-section/shop-3-yerunkar-corner/l4p.jpg"
        ),
        "color": "c2410c",
    },
]


def shop_payload(item: dict) -> dict:
    label = item["bname"].replace("-", " ")
    main = item.get("bmainimg") or _img(label, item.get("color", "4f46e5"))
    gallery = item.get("bgallery") or main
    return {
        "bname": item["bname"],
        "bcat": item["bcat"],
        "btags": item["btags"],
        "bhighlight": item["bhighlight"],
        "binfo": item["binfo"],
        "bmainimg": main,
        "bownerimgs": item.get("bownerimgs", "*"),
        "bgallery": gallery,
        "bytlinks": item.get("bytlinks", "*"),
        "bweblinks": item.get("bweblinks", "*"),
        "is_visible": True,
    }
