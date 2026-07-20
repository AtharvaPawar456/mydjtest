"""Copy legacy ProductInfo rows into per-category product tables."""
from django.core.management.base import BaseCommand
from django.db import connection

from mainapp.models import ProductInfo
from mainapp.product_categories_data import canonical_slug
from mainapp.product_catalog import (
    CATEGORY_PRODUCT_MODELS,
    PRODUCT_FIELD_NAMES,
    get_product_model,
)


class Command(BaseCommand):
    help = (
        "Split ProductInfo into Project_Software / Project_Hardware / … tables "
        "(preserves prodid). Safe to re-run (skips existing PKs)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear-target",
            action="store_true",
            help="Delete all rows in category product tables before copy.",
        )

    def handle(self, *args, **options):
        if options["clear_target"]:
            for Model in CATEGORY_PRODUCT_MODELS.values():
                n, _ = Model.objects.all().delete()
                self.stdout.write(f"Cleared {Model.__name__}: {n}")

        counts = {slug: 0 for slug in CATEGORY_PRODUCT_MODELS}
        skipped = unmatched = 0

        for src in ProductInfo.objects.all().iterator():
            slug = ""
            if src.category_id and getattr(src.category, "slug", None):
                slug = canonical_slug(src.category.slug)
            else:
                slug = canonical_slug(src.productcat)

            Model = get_product_model(slug)
            if Model is None:
                unmatched += 1
                self.stdout.write(
                    self.style.WARNING(
                        f"Unmatched #{src.prodid} cat={src.productcat!r}"
                    )
                )
                continue

            if Model.objects.filter(prodid=src.prodid).exists():
                skipped += 1
                continue

            payload = {f: getattr(src, f) for f in PRODUCT_FIELD_NAMES}
            # Preserve original primary key
            obj = Model(**payload)
            obj.save(force_insert=True)
            counts[Model.category_slug] += 1

        # Reset SQLite autoincrement sequences so new inserts don't collide
        if connection.vendor == "sqlite":
            with connection.cursor() as cursor:
                for Model in CATEGORY_PRODUCT_MODELS.values():
                    table = Model._meta.db_table
                    cursor.execute(f"SELECT MAX(prodid) FROM {table}")
                    row = cursor.fetchone()
                    max_id = row[0] or 0
                    cursor.execute(
                        "DELETE FROM sqlite_sequence WHERE name=%s",
                        [table],
                    )
                    if max_id:
                        cursor.execute(
                            "INSERT INTO sqlite_sequence(name, seq) VALUES (%s, %s)",
                            [table, max_id],
                        )

        for slug, n in counts.items():
            self.stdout.write(self.style.SUCCESS(f"{slug}: copied {n}"))
        self.stdout.write(
            self.style.SUCCESS(
                f"Done. skipped_existing={skipped} unmatched={unmatched} "
                f"source_total={ProductInfo.objects.count()}"
            )
        )
