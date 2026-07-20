from django.core.management.base import BaseCommand

from mainapp.models import Businesswebinfo
from mainapp.shop_seed_data import SHOPS, shop_payload


class Command(BaseCommand):
    help = "Seed / update all Task-3 I1 directory shops (update_or_create by bname)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--hide-all-new",
            action="store_true",
            help="Create shops as hidden (is_visible=False).",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Overwrite existing shop fields (default: only fill empty/placeholder media).",
        )

    def handle(self, *args, **options):
        hide = options["hide_all_new"]
        force = options["force"]
        created_n = updated_n = skipped_n = 0
        for raw in SHOPS:
            data = shop_payload(raw)
            if hide:
                data["is_visible"] = False
            existing = Businesswebinfo.objects.filter(bname=data["bname"]).first()
            if existing and not force:
                # Preserve real media if seed would only set placehold.co
                for field in ("bmainimg", "bgallery", "binfo", "bhighlight", "bcat", "btags"):
                    cur = getattr(existing, field, "") or ""
                    new = data.get(field, "")
                    if cur and cur != "*" and "placehold.co" not in cur:
                        if "placehold.co" in str(new) or not new:
                            data[field] = cur
                    elif cur and cur != "*" and "placehold.co" in cur and "placehold.co" not in str(new):
                        pass  # allow upgrade from placeholder to real
                    elif cur and cur != "*" and field in ("binfo", "bhighlight") and len(cur) > len(str(new) or ""):
                        # keep richer copy unless force
                        if "placehold" not in cur.lower():
                            data[field] = cur
            obj, created = Businesswebinfo.objects.update_or_create(
                bname=data["bname"],
                defaults=data,
            )
            if created:
                created_n += 1
                self.stdout.write(self.style.SUCCESS(f"Created {obj.bname}"))
            else:
                updated_n += 1
                self.stdout.write(f"Updated {obj.bname}")
        self.stdout.write(
            self.style.SUCCESS(
                f"Done. created={created_n} updated={updated_n} total={len(SHOPS)} force={force}"
            )
        )
