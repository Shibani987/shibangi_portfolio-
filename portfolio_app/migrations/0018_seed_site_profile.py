from django.db import migrations


def seed_site_profile(apps, schema_editor):
    SiteProfile = apps.get_model("portfolio_app", "SiteProfile")
    SiteProfile.objects.get_or_create(name="Shibangi Khan")


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio_app", "0017_siteprofile"),
    ]

    operations = [
        migrations.RunPython(seed_site_profile, migrations.RunPython.noop),
    ]
