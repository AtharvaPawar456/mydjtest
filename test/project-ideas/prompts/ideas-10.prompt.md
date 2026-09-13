# Prompt for ideas-10.json

**Save ChatGPT reply as:** test/project-ideas/ideas-10.json

| Meta | Value |
|------|-------|
| idea number | 10 |
| prodid | 53 |
| category_slug | hardware |
| product_name | Mini Wireless Power Transfer Module |
| DB status | already-enriched (optional re-gen) |

---

## Copy everything below this line into ChatGPT

---

You are writing the full product-detail content for one HandMadeProjects catalog page.

### Project identity (do not change)
- product_name: Mini Wireless Power Transfer Module
- prodid: 53
- category_slug: hardware

### Existing site context (use as grounding; expand into full professional detail)
- highlighttitle: Wirelessly transfer low voltage power between coils using electromagnetic induction for LED loads.
- prodtags: Wireless Power Transfer, Electromagnetic Induction, Inductive Coupling, Copper Coil, Power MOSFET, Magnetic Field, Resonant Energy Transfer, Low Voltage DC, Faraday's Law, Circuit Design, Energy Harvesting, DIY Electronics, Switching Frequency, Mutual Inductance, EMF, Power Electronics
- existing short text: Tech Copper Coil, Power MOSFET, LEDs, DC Power Supply, Electromagnetic Induction, Resonant Coupling Abstract The Mini Wireless Power Transfer Module is designed to demonstrate the fundamental principles of inductive coupling and wireless energy transmission. The system utilizes a primary transmitter coil and a secondary receiver coil to transfer electrical energy without physical connectors. By employing a power MOSFET as a high-speed switch, the DC input is converted into a high-frequency alternating current, generating a fluctuating magnetic field. This field induces an electromotive force (EMF) in the secondary coil, which is then used to power low-voltage loads such as LEDs. This project provides a practical implementation of Maxwell's equations and Faraday's Law of Induction, offering a compact, low-cost prototype for educational visualization of energy transfer efficiency and magne…

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
- Be specific to **Mini Wireless Power Transfer Module** — avoid copy-paste generic IoT fluff.
- Include prodid=53 and category_slug="hardware" and product_name exactly as given.

After you produce the JSON, I will save it as ideas-10.json.
