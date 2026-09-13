from django.test import TestCase

from . import factories


class ModelCreationTests(TestCase):
    """Sanity-checks that every core model can be created and stringified."""

    def test_product_info(self):
        p = factories.make_product()
        self.assertTrue(p.prodid)
        self.assertIn(p.productname, str(p))

    def test_team_member(self):
        m = factories.make_team_member()
        self.assertTrue(m.devid)
        self.assertIn(m.name, str(m))

    def test_intern_details(self):
        i = factories.make_intern()
        self.assertTrue(i.internid)
        self.assertIn("stipend", str(i))

    def test_intern_details_unstipend_str(self):
        i = factories.make_intern(is_stipend=False)
        self.assertIn("unstipend", str(i))

    def test_business_webinfo(self):
        s = factories.make_shop()
        self.assertTrue(s.bid)
        self.assertIn("visible", str(s))

    def test_business_webinfo_hidden_str(self):
        s = factories.make_shop(bname="Hidden-Shop", is_visible=False)
        self.assertIn("hidden", str(s))

    def test_accessories_prod(self):
        a = factories.make_accessory()
        self.assertTrue(a.apid)

    def test_aicontent_prod(self):
        c = factories.make_aicontent()
        self.assertTrue(c.aiid)

    def test_earn_task(self):
        t = factories.make_earn_task()
        self.assertTrue(t.etid)

    def test_home_image(self):
        h = factories.make_home_image()
        self.assertTrue(h.hiid)

    def test_yt_video(self):
        v = factories.make_video()
        self.assertTrue(v.ytid)

    def test_contact_message(self):
        c = factories.make_contact_message()
        self.assertTrue(c.cid)

    def test_user_details_and_fav_projects_models_removed(self):
        """Task 7 I3 removed the dead-end user-account subsystem entirely."""
        from .. import models
        self.assertFalse(hasattr(models, "UserDetails"))
        self.assertFalse(hasattr(models, "UserFavProjects"))
