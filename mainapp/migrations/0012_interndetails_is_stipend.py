from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0011_businesswebinfo_is_visible"),
    ]

    operations = [
        migrations.AddField(
            model_name="interndetails",
            name="is_stipend",
            field=models.BooleanField(
                default=False,
                help_text="Toggle ON for stipend (paid) internship; OFF for unstipend (unpaid).",
            ),
        ),
    ]
