from django.test import TestCase

from mainapp.project_documents import parse_documents
from . import factories


class ParseDocumentsTests(TestCase):
    def test_empty_and_star(self):
        self.assertEqual(parse_documents(None), [])
        self.assertEqual(parse_documents(""), [])
        self.assertEqual(parse_documents("*"), [])

    def test_bare_pptx_url(self):
        url = (
            "https://raw.githubusercontent.com/AtharvaPawar456/hmp_assets/"
            "refs/heads/main/assets/project_data/hardware/_15_Smart_Pill_Reminder/"
            "AI-Based Smart Medicine Reminder and Dispensing System.pptx"
        )
        items = parse_documents(url)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["ext"], "pptx")
        self.assertEqual(items[0]["type_label"], "PowerPoint")
        self.assertEqual(items[0]["url"], url)
        self.assertIn("officeapps.live.com", items[0]["view_url"])
        self.assertTrue(items[0]["label"])

    def test_label_pipe_url(self):
        raw = "Project Report|https://example.com/docs/report.pdf"
        items = parse_documents(raw)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["label"], "Project Report")
        self.assertEqual(items[0]["ext"], "pdf")
        self.assertEqual(items[0]["view_url"], "https://example.com/docs/report.pdf")

    def test_multiple_semicolon(self):
        raw = (
            "Slides|https://cdn.example.com/a.pptx;"
            "https://cdn.example.com/b.pdf"
        )
        items = parse_documents(raw)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["ext"], "pptx")
        self.assertEqual(items[1]["ext"], "pdf")

    def test_productinfo_renders_documents(self):
        url = "https://example.com/files/demo.pptx"
        product = factories.make_product(
            documents=f"Demo Deck|{url}",
            productname="Doc Test Product",
        )
        response = self.client.get(
            f"/productinfo/{product.category_slug}/{product.prodid}/"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Project Documents")
        self.assertContains(response, "Demo Deck")
        self.assertContains(response, "Download")
        self.assertContains(response, "View")
        self.assertContains(response, url)
