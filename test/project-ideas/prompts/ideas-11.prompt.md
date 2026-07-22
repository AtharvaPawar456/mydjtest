# Prompt for ideas-11.json

**Save ChatGPT reply as:** test/project-ideas/ideas-11.json

| Meta | Value |
|------|-------|
| idea number | 11 |
| prodid | 54 |
| category_slug | hardware |
| product_name | LiFi Audio Transmission Mini System |
| DB status | already-enriched (optional re-gen) |

---

## Copy everything below this line into ChatGPT

---

You are writing the full product-detail content for one HandMadeProjects catalog page.

### Project identity (do not change)
- product_name: LiFi Audio Transmission Mini System
- prodid: 54
- category_slug: hardware

### Existing site context (use as grounding; expand into full professional detail)
- highlighttitle: Wireless audio transmission using LED light and solar panel conversion for simple listening applications.
- prodtags: LiFi, LED communication, audio transmission, solar panel, light-to-electric conversion, audio amplifier, wireless technology, IoT, mini project, low-cost electronics, energy harvesting, light fidelity, optical wireless, analog modulation, photovoltaic cell, signal processing, VLC, visible light communication
- existing short text: Tech Optical Wireless Communication, Analog Signal Modulation, Photovoltaic Conversion, Audio Amplification Abstract The LiFi Audio Transmission Mini System is an educational prototype designed to demonstrate the principles of Light Fidelity (LiFi) by transmitting audio signals through visible light. The system utilizes a high-brightness LED as the transmitter, which modulates the intensity of light according to the analog audio signal from a source. On the receiving end, a small solar panel acts as a photodetector, converting the modulated light back into an electrical current. This signal is then processed through an audio amplifier to restore the original sound and output it via a speaker. This project provides a tangible demonstration of how data can be carried on light waves, offering a low-cost, RF-free alternative for short-range wireless communication and introducing students to …

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
- Be specific to **LiFi Audio Transmission Mini System** — avoid copy-paste generic IoT fluff.
- Include prodid=54 and category_slug="hardware" and product_name exactly as given.

After you produce the JSON, I will save it as ideas-11.json.
