from django.test import TestCase

from mainapp.product_media import (
    build_carousel_images,
    find_block_diagram_url,
    parse_media_list,
)
from . import factories


class ProductMediaHelpersTests(TestCase):
    def test_parse_gallery_urls(self):
        raw = (
            "https://cdn.example.com/a.png;"
            "Block Diagram|https://cdn.example.com/block.png\n"
            "https://cdn.example.com/clip.mp4"
        )
        items = parse_media_list(raw)
        self.assertEqual(len(items), 3)
        self.assertTrue(items[0]["is_image"])
        self.assertEqual(items[1]["label"], "Block Diagram")
        self.assertTrue(items[2]["is_video"])

    def test_carousel_main_first_dedupe(self):
        main = "https://cdn.example.com/main.jpg"
        gallery = parse_media_list(
            f"{main};https://cdn.example.com/g2.jpg;https://cdn.example.com/v.mp4"
        )
        slides = build_carousel_images(main, gallery)
        self.assertEqual(slides[0]["src"], main)
        self.assertEqual(len(slides), 2)  # main + g2 (video skipped, main deduped)

    def test_block_diagram_hint(self):
        items = parse_media_list(
            "https://cdn.example.com/photo.png;"
            "https://cdn.example.com/my_block_diagram.png"
        )
        url = find_block_diagram_url(items)
        self.assertIn("block_diagram", url)

    def test_productinfo_order_and_features(self):
        product = factories.make_product(
            productname="Carousel Demo Project",
            mainimgbasetxt="https://cdn.example.com/main.png",
            gallery=(
                "https://cdn.example.com/g1.png;"
                "Block Diagram|https://cdn.example.com/block.png"
            ),
            components="Resistor|https://cdn.example.com/r1.png",
            prodinfo="<p>About paragraph for export test.</p>",
        )
        response = self.client.get(
            f"/productinfo/{product.category_slug}/{product.prodid}/"
        )
        self.assertEqual(response.status_code, 200)
        html = response.content.decode("utf-8")
        # Section order: gallery id before about details id
        self.assertLess(html.find('id="gallery"'), html.find('id="details"'))
        self.assertIn("heroCarousel", html)
        self.assertIn("media-dl-btn", html)
        self.assertIn("Download Block Diagram", html)
        self.assertIn('id="components"', html)
        self.assertIn("downloadAboutTxt", html)
        self.assertIn("text-white/90", html)  # CTA on-dark phone labels
        self.assertIn("border-2 border-white", html)  # Call/WA white border on CTA
        self.assertIn("Payment Policy", html)
        self.assertIn("Step 1", html)
        # Option A WhatsApp prefill includes project interest + URL
        self.assertIn("wa.me/", html)
        self.assertIn("I%27m%20interested%20in%20this%20project", html)
        self.assertIn("Carousel%20Demo%20Project", html)
        self.assertIn(f"productinfo/{product.category_slug}/{product.prodid}", html)
        # Share project buttons
        self.assertIn("share-project-btn", html)
        self.assertIn("Share this project", html)
