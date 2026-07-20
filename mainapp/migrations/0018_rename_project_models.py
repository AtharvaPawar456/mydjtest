from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0017_split_product_models"),
    ]

    operations = [
        migrations.RenameModel(old_name="SoftwareProduct", new_name="Project_Software"),
        migrations.RenameModel(old_name="HardwareProduct", new_name="Project_Hardware"),
        migrations.RenameModel(old_name="MechanicalProduct", new_name="Project_Mechanical"),
        migrations.RenameModel(old_name="SimulationProduct", new_name="Project_Simulation"),
        migrations.RenameModel(old_name="ScienceProduct", new_name="Project_Science"),
        migrations.RenameModel(old_name="CraftProduct", new_name="Project_Craft"),
        migrations.AlterModelOptions(
            name="project_software",
            options={
                "ordering": ["-timestamp"],
                "verbose_name": "Project Software",
                "verbose_name_plural": "Project Software",
            },
        ),
        migrations.AlterModelOptions(
            name="project_hardware",
            options={
                "ordering": ["-timestamp"],
                "verbose_name": "Project Hardware",
                "verbose_name_plural": "Project Hardware",
            },
        ),
        migrations.AlterModelOptions(
            name="project_mechanical",
            options={
                "ordering": ["-timestamp"],
                "verbose_name": "Project Mechanical",
                "verbose_name_plural": "Project Mechanical",
            },
        ),
        migrations.AlterModelOptions(
            name="project_simulation",
            options={
                "ordering": ["-timestamp"],
                "verbose_name": "Project Simulation",
                "verbose_name_plural": "Project Simulation",
            },
        ),
        migrations.AlterModelOptions(
            name="project_science",
            options={
                "ordering": ["-timestamp"],
                "verbose_name": "Project Science",
                "verbose_name_plural": "Project Science",
            },
        ),
        migrations.AlterModelOptions(
            name="project_craft",
            options={
                "ordering": ["-timestamp"],
                "verbose_name": "Project Craft",
                "verbose_name_plural": "Project Craft",
            },
        ),
    ]
