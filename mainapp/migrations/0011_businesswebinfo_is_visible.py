from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0010_businesswebinfo"),
    ]

    operations = [
        migrations.AddField(
            model_name="businesswebinfo",
            name="is_visible",
            field=models.BooleanField(
                default=True,
                help_text="If unchecked/hidden, shop is hidden from the public directory.",
            ),
        ),
    ]
