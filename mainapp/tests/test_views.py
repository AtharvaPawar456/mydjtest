from django.test import TestCase, override_settings

from . import factories


class PublicPagesRenderTests(TestCase):
    """Every public page should return 200 with a bit of fixture data present."""

    @classmethod
    def setUpTestData(cls):
        cls.product = factories.make_product()
        cls.member = factories.make_team_member()
        cls.intern = factories.make_intern()
        cls.shop = factories.make_shop()
        cls.accessory = factories.make_accessory()
        cls.aicontent = factories.make_aicontent()
        factories.make_earn_task()
        factories.make_home_image()
        factories.make_video()

    def assertOk(self, path):
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200, f"{path} returned {response.status_code}")
        return response

    def test_homepage(self):
        self.assertOk("/")

    def test_dashboard(self):
        self.assertOk("/dashboard/")

    def test_gallery(self):
        self.assertOk("/gallery/")

    def test_engineering_projects_category(self):
        self.assertOk("/engineering-projects/")

    def test_kids_projects(self):
        self.assertOk("/kids-projects/")

    def test_aboutus(self):
        self.assertOk("/aboutus/")

    def test_contactus_has_no_form_and_has_whatsapp(self):
        response = self.assertOk("/contactus/")
        self.assertNotContains(response, '<form action="/contactus/"')
        self.assertContains(response, "wa.me/918169239027")
        self.assertContains(response, "wa.me/919320668111")
        self.assertContains(response, "93206 68111")

    def test_privacy_policy(self):
        self.assertOk("/privacy-policy/")

    def test_terms_of_service(self):
        self.assertOk("/terms-of-service/")

    def test_our_team(self):
        self.assertOk("/ourteam/")

    def test_team_member_profile_found(self):
        response = self.assertOk(f"/ourteam/profile/?name={self.member.name}")
        self.assertContains(response, self.member.name)

    def test_team_member_profile_not_found_is_404(self):
        response = self.client.get("/ourteam/profile/?name=NoSuchPersonXYZ")
        self.assertEqual(response.status_code, 404)

    def test_internship_listing(self):
        self.assertOk("/internship/")

    def test_intern_profile(self):
        self.assertOk(f"/internship/profile/{self.intern.internid}/")

    def test_intern_profile_missing_is_404(self):
        response = self.client.get("/internship/profile/999999/")
        self.assertEqual(response.status_code, 404)

    def test_internship_opportunities(self):
        self.assertOk("/internship/opportunities/")

    def test_youtube_projects(self):
        self.assertOk("/youtube-projects/")

    def test_accessories_list_and_detail(self):
        self.assertOk("/accessories/")
        self.assertOk(f"/accessoriesview/{self.accessory.apid}/")

    def test_aicontent_list_and_detail(self):
        self.assertOk("/aicontent/")
        self.assertOk(f"/aicontent/{self.aicontent.aiid}/")

    def test_product_list_and_detail(self):
        self.assertOk("/productlist/")
        self.assertOk(
            f"/productinfo/{self.product.category_slug}/{self.product.prodid}/"
        )
        # Legacy product URL still resolves (redirect)
        r = self.client.get(f"/productinfo/{self.product.prodid}/")
        self.assertIn(r.status_code, (200, 301, 302))

    def test_product_detail_missing_is_404(self):
        response = self.client.get("/productinfo/999999/")
        self.assertEqual(response.status_code, 404)

    def test_earn_tasks(self):
        self.assertOk("/earn-tasks/")

    def test_affiliateinfo(self):
        self.assertOk("/affiliateinfo/")

    def test_all_shops_and_detail(self):
        self.assertOk("/allshops/")
        self.assertOk(f"/shop/{self.shop.bname}/")

    def test_shop_missing_is_404(self):
        response = self.client.get("/shop/NoSuchShopXYZ/")
        self.assertEqual(response.status_code, 404)

    def test_global_search(self):
        response = self.assertOk(f"/search/?q={self.product.productname}")
        self.assertContains(response, self.product.productname)

    def test_global_search_empty_query(self):
        self.assertOk("/search/")

    def test_robots_txt(self):
        response = self.assertOk("/robots.txt")
        self.assertIn(b"Sitemap:", response.content)

    def test_sitemap_xml(self):
        response = self.assertOk("/sitemap.xml")
        self.assertIn(b"<urlset", response.content)
        self.assertIn(b"xmlns:image", response.content)


class RemovedFeaturesAreGoneTests(TestCase):
    """Task 7 I3: userdashboard/profile/add-to-favorites no longer exist."""

    def test_userdashboard_is_404(self):
        self.assertEqual(self.client.get("/userdashboard/").status_code, 404)

    def test_profile_is_404(self):
        self.assertEqual(self.client.get("/profile/").status_code, 404)

    def test_add_to_favorites_is_404(self):
        self.assertEqual(self.client.get("/add-to-favorites/1/").status_code, 404)

    def test_login_is_404(self):
        self.assertEqual(self.client.get("/login/").status_code, 404)

    def test_register_is_404(self):
        self.assertEqual(self.client.get("/register/").status_code, 404)


class AdminGatedViewsRedirectToAdminLoginTests(TestCase):
    """Task 7 I3: the only login page left is the Django admin's."""

    def assertRedirectsToAdminLogin(self, path):
        response = self.client.get(path)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/hpmadmin/login/"), response.url)

    def test_addproduct_redirects_to_admin_login(self):
        self.assertRedirectsToAdminLogin("/addproduct/")

    def test_add_developer_redirects_to_admin_login(self):
        self.assertRedirectsToAdminLogin("/add-developer/")

    def test_add_intern_redirects_to_admin_login(self):
        self.assertRedirectsToAdminLogin("/add-intern/")

    def test_edit_hero_images_redirects_to_admin_login(self):
        self.assertRedirectsToAdminLogin("/edit_hero_images/")

    def test_analysis_redirects_to_admin_login(self):
        self.assertRedirectsToAdminLogin("/analysis/")

    def test_edit_product_redirects_to_admin_login(self):
        p = factories.make_product()
        self.assertRedirectsToAdminLogin(f"/edit-product/{p.prodid}/")


class CustomErrorPagesTests(TestCase):
    @override_settings(DEBUG=False, ALLOWED_HOSTS=["*"])
    def test_404_page_is_branded(self):
        response = self.client.get("/this-page-does-not-exist/")
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "HandMadeProjects", status_code=404)
        self.assertContains(response, "404", status_code=404)
