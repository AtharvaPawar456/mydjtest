from django.core.management.base import BaseCommand

from mainapp.models import ProductCategory
from mainapp.product_categories_data import DEFAULT_CATEGORIES


class Command(BaseCommand):
    help = "Seed ProductCategory metadata rows (Software…Craft)."

    def handle(self, *args, **options):
        created_n = updated_n = 0
        for row in DEFAULT_CATEGORIES:
            obj, created = ProductCategory.objects.update_or_create(
                slug=row["slug"],
                defaults={
                    "name": row["name"],
                    "legacy_slugs": row.get("legacy_slugs", ""),
                    "hashtags": row.get("hashtags", ""),
                    "description": row.get("description", ""),
                    "sort_order": row.get("sort_order", 0),
                    "is_active": True,
                },
            )
            if created:
                created_n += 1
                self.stdout.write(self.style.SUCCESS(f"Created category {obj.name}"))
            else:
                updated_n += 1
                self.stdout.write(f"Updated category {obj.name}")
        self.stdout.write(
            self.style.SUCCESS(f"Done. created={created_n} updated={updated_n}")
        )
