from django.core.management.base import BaseCommand

from mainapp.models import Project_Hardware
from mainapp.new_project_ideas_data import IDEAS, product_payload


class Command(BaseCommand):
    help = "Seed / update hardware project ideas into Project_Hardware table."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Overwrite existing product fields (default: skip products that already exist).",
        )

    def handle(self, *args, **options):
        force = options["force"]
        created_n = updated_n = skipped_n = 0
        for idea in IDEAS:
            data = product_payload(idea)
            # product_payload still includes productcat; drop for Project_Hardware
            data.pop("productcat", None)
            data.pop("category", None)
            existing = Project_Hardware.objects.filter(
                productname=data["productname"]
            ).first()
            if existing and not force:
                skipped_n += 1
                self.stdout.write(f"Skipped (exists) {data['productname']}")
                continue
            obj, created = Project_Hardware.objects.update_or_create(
                productname=data["productname"],
                defaults=data,
            )
            if created:
                created_n += 1
                self.stdout.write(self.style.SUCCESS(f"Created {obj.productname}"))
            else:
                updated_n += 1
                self.stdout.write(f"Updated {obj.productname}")
        self.stdout.write(
            self.style.SUCCESS(
                f"Done. created={created_n} updated={updated_n} skipped={skipped_n}"
            )
        )
