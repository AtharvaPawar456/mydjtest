"""
Canonical product categories (seed + resolution helpers).

These six stay stable in ProductCategory; products link via FK instead of free text.
"""

DEFAULT_CATEGORIES = [
    {
        "name": "Software",
        "slug": "software",
        "legacy_slugs": "softwareprojects",
        "hashtags": (
            "ai, ml, genai, django, flask, webapp, mobileapp, api, backend, frontend, "
            "fullstack, saas, automation, chatbot, nlp, computerVision, datascience, "
            "blockchain, devops, cloud"
        ),
        "description": "Django, ML, SaaS and web/app projects for demos and portfolios.",
        "sort_order": 10,
    },
    {
        "name": "Hardware",
        "slug": "hardware",
        "legacy_slugs": "hardwareprojects",
        "hashtags": (
            "iot, esp32, arduino, raspberrypi, stm32, robotics, embedded, sensors, "
            "automation, smartHome, wearables, edgeAi, pcb, hardwareAi, industrialIoT, "
            "bluetooth, wifi, mqtt, serialComm, powerManagement"
        ),
        "description": "ESP32, Arduino, sensors and IoT / embedded kits.",
        "sort_order": 20,
    },
    {
        "name": "Mechanical",
        "slug": "mechanical",
        "legacy_slugs": "mechanicalprojects",
        "hashtags": "cad, 3dprint, enclosures, mechanisms, gears, chassis, prototype",
        "description": "CAD, mechanisms and mechanical project builds.",
        "sort_order": 30,
    },
    {
        "name": "Simulation",
        "slug": "simulation",
        "legacy_slugs": "simulationprojects",
        "hashtags": "matlab, simulink, multisim, proteus, ansys, modelling, circuit-sim",
        "description": "Circuit, system and physics simulation projects.",
        "sort_order": 40,
    },
    {
        "name": "Science",
        "slug": "science",
        "legacy_slugs": "kidsscience",
        "hashtags": (
            "chemistry, physics, biology, experiment, stem, magnets, electricity, solar, "
            "plants, water, light, sound, density, reaction, environment, weather, space, "
            "simpleMachine, microscope, diyLab"
        ),
        "description": "Hands-on science experiments and STEM demos.",
        "sort_order": 50,
    },
    {
        "name": "Craft",
        "slug": "craft",
        "legacy_slugs": "kidscraft",
        "hashtags": (
            "origami, paperCraft, diy, painting, clay, recycling, beads, woodcraft, "
            "handmade, festival, decor, collage, popup, cardboard, sewing, embroidery, "
            "scrapbook, models, creative, art"
        ),
        "description": "Origami, DIY, painting and handmade craft projects.",
        "sort_order": 60,
    },
]

# Map any known free-text / legacy value → canonical slug
LEGACY_TO_SLUG = {
    "software": "software",
    "softwareprojects": "software",
    "hardware": "hardware",
    "hardwareprojects": "hardware",
    "mechanical": "mechanical",
    "mechanicalprojects": "mechanical",
    "simulation": "simulation",
    "simulationprojects": "simulation",
    "science": "science",
    "kidsscience": "science",
    "craft": "craft",
    "kidscraft": "craft",
}


def canonical_slug(value: str) -> str:
    v = (value or "").strip().lower()
    return LEGACY_TO_SLUG.get(v, v)
