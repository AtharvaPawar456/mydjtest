from django.template import Context, Template
from django.test import TestCase

from . import factories


class PriceFilterTests(TestCase):
    def render(self, value):
        template = Template("{% load price_filters %}{{ v|price }}")
        return template.render(Context({"v": value}))

    def test_formats_thousands(self):
        self.assertEqual(self.render("15000"), "15,000")

    def test_passes_through_placeholder(self):
        self.assertEqual(self.render("*"), "*")

    def test_passes_through_non_numeric(self):
        self.assertEqual(self.render("call for price"), "call for price")

    def test_passes_through_none(self):
        self.assertEqual(self.render(None), "None")

    def test_handles_already_small_numbers(self):
        self.assertEqual(self.render("500"), "500")


class ContactContextProcessorTests(TestCase):
    def test_phone_appears_on_homepage(self):
        response = self.client.get("/")
        self.assertContains(response, "81692 39027")
        self.assertContains(response, "tel:+918169239027")
        self.assertContains(response, "wa.me/918169239027")
        # Alternate contact number
        self.assertContains(response, "93206 68111")
        self.assertContains(response, "tel:+919320668111")
        self.assertContains(response, "wa.me/919320668111")


class PaginationTests(TestCase):
    def test_productlist_paginates_past_page_size(self):
        for i in range(30):
            factories.make_product(productname=f"Widget {i}")
        response = self.client.get("/productlist/")
        self.assertContains(response, 'aria-label="Pagination"')

        page2 = self.client.get("/productlist/?page=2")
        self.assertEqual(page2.status_code, 200)

    def test_out_of_range_page_does_not_500(self):
        factories.make_product()
        response = self.client.get("/productlist/?page=9999")
        self.assertEqual(response.status_code, 200)

    def test_pagination_preserves_filters(self):
        factories.make_product(productcat="hardware")
        response = self.client.get("/productlist/?productcat=hardware")
        if b'aria-label="Pagination"' in response.content:
            self.assertIn(b"productcat=hardware", response.content)

    def test_small_lists_show_no_pagination(self):
        factories.make_shop()
        response = self.client.get("/allshops/")
        self.assertNotContains(response, 'aria-label="Pagination"')


class AjaxFilterPartialTests(TestCase):
    def test_productlist_ajax_returns_partial_not_full_page(self):
        factories.make_product()
        response = self.client.get("/productlist/", HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"<!DOCTYPE html>", response.content)

    def test_internship_listing_ajax_returns_partial(self):
        factories.make_intern()
        response = self.client.get("/internship/?stipend=stipend", HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"<!DOCTYPE html>", response.content)
