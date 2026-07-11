from django.db import migrations


GRAPHIC_DESIGN_DESCRIPTION = (
    "Professional graphic design services including logo design, branding, social media posts, "
    "banners, posters, flyers, brochures, business cards, UI graphics, and other creative visual "
    "solutions for businesses and individuals."
)

SUBCATEGORIES = [
    (
        "Branding",
        "branding",
        "Identity systems, product visuals, logos, and polished business materials.",
        1,
    ),
    (
        "Editorial Layouts",
        "editorial-layouts",
        "Thoughtful print and digital layouts for eBooks, books, and storytelling pieces.",
        2,
    ),
    (
        "Social Campaigns",
        "social-campaigns",
        "Visual campaigns built for banners, templates, and social ad content.",
        3,
    ),
]


def seed_graphic_design_subcategories(apps, schema_editor):
    Category = apps.get_model("portfolio_app", "Category")
    SubCategory = apps.get_model("portfolio_app", "SubCategory")

    graphic_design, created = Category.objects.get_or_create(
        slug="graphic-design",
        defaults={
            "name": "Graphic Design",
            "description": GRAPHIC_DESIGN_DESCRIPTION,
            "order": 1,
        },
    )
    if not created and not graphic_design.description:
        graphic_design.description = GRAPHIC_DESIGN_DESCRIPTION
        graphic_design.save(update_fields=["description"])

    for name, slug, description, order in SUBCATEGORIES:
        SubCategory.objects.update_or_create(
            slug=slug,
            defaults={
                "category": graphic_design,
                "name": name,
                "description": description,
                "order": order,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio_app", "0003_subcategory"),
    ]

    operations = [
        migrations.RunPython(seed_graphic_design_subcategories, migrations.RunPython.noop),
    ]
