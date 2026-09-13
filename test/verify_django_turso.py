"""Smoke-check that Django ORM is using Turso and can read/write migrated rows."""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "handmadeprojects.settings")

import django

django.setup()

from django.conf import settings
from django.contrib.auth.models import User
from django.db import connection
from django.db.migrations.recorder import MigrationRecorder

from mainapp.models import (
    Businesswebinfo,
    Contactus,
    InternOpportunity,
    ProductCategory,
    Project_Hardware,
)


def main():
    engine = settings.DATABASES["default"]["ENGINE"]
    print("engine:", engine)
    if engine != "django_libsql":
        raise SystemExit(f"Expected django_libsql, got {engine}")

    print("vendor:", connection.vendor)
    print("users:", User.objects.count())
    print("hardware:", Project_Hardware.objects.count())
    print("categories:", ProductCategory.objects.count())
    print("internships:", InternOpportunity.objects.count())
    print("shops:", Businesswebinfo.objects.count())

    product = Project_Hardware.objects.get(prodid=77)
    print("product 77:", product.productname)

    applied = list(
        MigrationRecorder.Migration.objects.filter(app="mainapp")
        .order_by("name")
        .values_list("name", flat=True)
    )
    print("mainapp migrations:", ", ".join(applied))
    if "0020_product_components_field" not in applied:
        raise SystemExit("mainapp.0020 is missing on Turso")

    probe = Contactus.objects.create(
        name="turso-migration-probe",
        emailid="probe@example.com",
        msg="write-roundtrip",
    )
    fetched = Contactus.objects.get(pk=probe.pk)
    if fetched.msg != "write-roundtrip":
        raise SystemExit("Turso write round-trip failed")
    Contactus.objects.filter(pk=probe.pk).delete()
    if Contactus.objects.filter(pk=probe.pk).exists():
        raise SystemExit("Turso delete round-trip failed")
    print("write round-trip: ok")
    print("Django ORM smoke check passed.")


if __name__ == "__main__":
    main()
