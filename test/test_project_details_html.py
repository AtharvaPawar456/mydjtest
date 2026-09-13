"""Unit tests for pure helpers (no Django, no Ollama). Schema matches product 33."""
from __future__ import annotations

import unittest

from project_details_html import (
    ENRICHED_COMMENT,
    ENRICHED_MARKER,
    abstract_to_highlight,
    extract_json_object,
    is_enriched,
    keywords_to_prodtags,
    normalize_details,
    structure_to_html,
    validate_details,
    word_count,
)


# Minimal valid payload shaped like /productinfo/hardware/33/
SAMPLE = {
    "product_name": "iBin: IoT-Based Smart Waste Sorting and Monitoring System",
    "highlighttitle": "An IoT-powered smart dustbin that sorts wet and dry waste.",
    "tech": "ESP32 Microcontroller, Ultrasonic Sensors, Moisture Sensors, Servo Motor, OLED Display, ThingSpeak",
    "abstract": " ".join(["word"] * 130),
    "keywords": [
        "IoT",
        "Smart Dustbin",
        "ESP32",
        "Servo Motor",
        "Ultrasonic Sensor",
        "OLED Display",
        "Buzzer",
        "ThingSpeak",
        "Garbage Monitoring",
        "Mobile App",
        "Waste Sorting",
        "Cloud Data Logging",
    ],
    "project_description": " ".join(["word"] * 220),
    "project_features": [
        "Automatic lid opening using servo motor and ultrasonic proximity detection",
        "Waste segregation into wet and dry compartments",
        "Real-time waste level monitoring with ultrasonic sensors",
        "Cloud data logging and analytics via ThingSpeak",
        "Mobile app integration for remote monitoring and alerts",
        "OLED display for live status updates",
        "Buzzer alert when threshold is reached",
        "Secure Wi-Fi communication through ESP32",
    ],
    "hardware_components": "ESP32 Microcontroller, Ultrasonic Sensor, Moisture Sensor, Servo Motor, OLED Display, Buzzer",
    "software_components": "Arduino IDE, ThingSpeak Cloud, Custom Mobile App",
    "applications": [
        "Household waste management",
        "Offices and workplaces",
        "Schools and universities",
        "Public parks and community centers",
        "Smart city waste monitoring systems",
    ],
    "advantages": [
        "Reduces human effort in waste segregation",
        "Promotes better hygiene with contactless lid operation",
        "Enables data-driven decision-making for waste collection",
        "Prevents overflow through timely alerts",
        "Scalable for small and large communities",
    ],
    "limitations": [
        "Requires consistent Wi-Fi connectivity for IoT features",
        "Limited waste categorization (wet and dry)",
        "Higher initial cost compared to regular bins",
        "Sensors may require periodic maintenance",
    ],
    "future_scope": [
        "AI for advanced waste categorization",
        "Solar-powered design",
        "Municipal collection system integration",
        "Voice assistant compatibility",
    ],
    "conclusion": " ".join(["word"] * 140),
}


class EnrichmentTests(unittest.TestCase):
    def test_empty_not_enriched(self):
        self.assertFalse(is_enriched(None))
        self.assertFalse(is_enriched(""))
        self.assertFalse(is_enriched("*"))
        self.assertFalse(is_enriched("<p>Short description only</p>"))

    def test_marker_means_enriched(self):
        html = f"{ENRICHED_COMMENT}\n<div><h2>Tech</h2></div>"
        self.assertTrue(is_enriched(html))
        self.assertIn(ENRICHED_MARKER, html)

    def test_seed_template_not_enriched(self):
        seed = """
        <div>
          <h2>Project Name</h2>
          <h2>Description</h2>
          <h2>Report Contents</h2>
          <ul>
            <li>Problem Statement</li>
            <li>Abstract</li>
            <li>Introduction</li>
          </ul>
        </div>
        """
        self.assertFalse(is_enriched(seed))

    def test_product33_style_heuristic(self):
        html = """
        <h2>Project Features</h2>
        <h2>Specifications</h2>
        <h2>Future Scope</h2>
        <h2>Project Description</h2>
        """
        self.assertTrue(is_enriched(html))


class JsonExtractTests(unittest.TestCase):
    def test_pure_json(self):
        data = extract_json_object('{"a": 1, "b": "x"}')
        self.assertEqual(data["a"], 1)

    def test_fenced_json(self):
        raw = '```json\n{"abstract": "hello"}\n```'
        data = extract_json_object(raw)
        self.assertEqual(data["abstract"], "hello")

    def test_prose_wrapper(self):
        raw = 'Here is the result:\n{"abstract": "ok"}\nThanks.'
        data = extract_json_object(raw)
        self.assertEqual(data["abstract"], "ok")


class HtmlRenderTests(unittest.TestCase):
    def test_structure_matches_product33_sections(self):
        html = structure_to_html(SAMPLE)
        self.assertIn(ENRICHED_MARKER, html)
        self.assertIn(ENRICHED_COMMENT, html)
        for heading in (
            "Tech",
            "Abstract",
            "Keywords",
            "Project Description",
            "Project Features",
            "Specifications",
            "Report Contents",
            "Applications",
            "Advantages",
            "Limitations",
            "Future Scope",
            "Conclusion",
        ):
            self.assertIn(heading, html)
        self.assertIn("Hardware components", html)
        self.assertIn("Software components", html)
        self.assertIn("ESP32 Microcontroller", html)
        self.assertIn("Automatic lid opening", html)
        # XSS: model text escaped
        dirty = dict(SAMPLE)
        dirty["abstract"] = "<script>alert(1)</script> unsafe"
        safe_html = structure_to_html(dirty)
        self.assertNotIn("<script>", safe_html)
        self.assertIn("&lt;script&gt;", safe_html)

    def test_normalize_aliases(self):
        d = normalize_details(
            {
                "technologies": "ESP32, sensors",
                "features": ["A", "B"],
                "tags": "iot, esp32, bin",
            },
            product_name="X",
        )
        self.assertEqual(d["tech"], "ESP32, sensors")
        self.assertEqual(d["project_features"], ["A", "B"])
        self.assertEqual(d["keywords"], ["iot", "esp32", "bin"])

    def test_validate_sample_clean(self):
        d = normalize_details(SAMPLE)
        warns = validate_details(d)
        self.assertIsInstance(warns, list)
        # Should not flag missing required keys
        self.assertFalse(any(w.startswith("missing") for w in warns))

    def test_word_count(self):
        self.assertEqual(word_count("one two three"), 3)

    def test_tags_and_highlight(self):
        self.assertEqual(keywords_to_prodtags(["a", "b"]), "a, b")
        hi = abstract_to_highlight(SAMPLE["abstract"], fallback=SAMPLE["highlighttitle"])
        self.assertIn("IoT-powered", hi)


if __name__ == "__main__":
    unittest.main()
