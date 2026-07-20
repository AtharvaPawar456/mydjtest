from django.core.management.base import BaseCommand

from mainapp.intern_opportunities_data import parse_opportunities_file
from mainapp.models import InternOpportunity


class Command(BaseCommand):
    help = (
        "Seed / update InternOpportunity rows from "
        "ai-space/ai-suggestion/intern-ops.txt "
        "(| after ID = visible, - after ID = hidden)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Overwrite all fields from the file (default: update_or_create always applies file data).",
        )
        parser.add_argument(
            "--visible-only",
            action="store_true",
            help="Only seed rows marked visible (|) in the file; skip hidden (-) rows.",
        )

    def handle(self, *args, **options):
        rows = parse_opportunities_file()
        if not rows:
            self.stderr.write(self.style.ERROR("No rows parsed from intern-ops.txt"))
            return

        if options["visible_only"]:
            rows = [r for r in rows if r.get("is_visible")]

        created_n = updated_n = 0
        for row in rows:
            opid = row["opid"]
            defaults = {k: v for k, v in row.items() if k != "opid"}
            obj, created = InternOpportunity.objects.update_or_create(
                opid=opid,
                defaults=defaults,
            )
            label = f"#{obj.opid} {obj.title} ({'visible' if obj.is_visible else 'hidden'})"
            if created:
                created_n += 1
                self.stdout.write(self.style.SUCCESS(f"Created {label}"))
            else:
                updated_n += 1
                self.stdout.write(f"Updated {label}")

        visible = InternOpportunity.objects.filter(is_visible=True).count()
        hidden = InternOpportunity.objects.filter(is_visible=False).count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Done. created={created_n} updated={updated_n} "
                f"db_visible={visible} db_hidden={hidden} file_rows={len(rows)}"
            )
        )
