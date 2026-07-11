from django.db import migrations


SECTIONS_BY_SUBCATEGORY = {
    "editorial-layouts": [
        (
            "E-Book Cover",
            "Compelling book cover designs that capture the essence and tone of the narrative.",
            1,
            [
                (
                    "Mountain Echo",
                    "A dramatic cover design featuring a majestic mountain range under a vibrant sunset.",
                    1,
                ),
                (
                    "Alone",
                    "A contemplative cover design with subtle textures and a serene, introspective mood.",
                    2,
                ),
            ],
        ),
        (
            "Book Covers",
            "Engaging book cover designs that reflect the genre and narrative of the content.",
            2,
            [
                (
                    "Quiet Expression",
                    "A subtle and introspective cover design that captures the essence of the narrative.",
                    1,
                ),
                (
                    "Modern Muse",
                    "A bold and contemporary cover design that embodies the spirit of modernity and creativity.",
                    2,
                ),
            ],
        ),
        (
            "Magazine Layouts",
            "Dynamic magazine layouts that balance visual appeal with readability and content flow.",
            3,
            [
                (
                    "Fashion Forward",
                    "A sleek and stylish magazine layout that highlights fashion trends and photography.",
                    1,
                ),
                (
                    "Nightlife Chronicles",
                    "A vibrant and energetic magazine layout that captures the essence of nightlife culture.",
                    2,
                ),
            ],
        ),
    ],
    "social-campaigns": [
        (
            "Campaign Strategy",
            "High-impact visuals and messaging designed for attention, storytelling, and conversion.",
            1,
            [
                (
                    "Launch Moment",
                    "Bold campaign visuals that balance product presence with confident brand storytelling.",
                    1,
                ),
                (
                    "Trend Response",
                    "Creative concepts designed for fast-moving social engagement and audience recall.",
                    2,
                ),
            ],
        ),
    ],
}


def seed_remaining_graphic_design_sections(apps, schema_editor):
    SubCategory = apps.get_model("portfolio_app", "SubCategory")
    ProductSection = apps.get_model("portfolio_app", "ProductSection")
    ProductItem = apps.get_model("portfolio_app", "ProductItem")

    for subcategory_slug, sections in SECTIONS_BY_SUBCATEGORY.items():
        subcategory = SubCategory.objects.filter(
            slug=subcategory_slug,
            category__slug="graphic-design",
        ).first()
        if not subcategory:
            continue

        for section_name, section_description, section_order, products in sections:
            section, _ = ProductSection.objects.update_or_create(
                subcategory=subcategory,
                name=section_name,
                defaults={
                    "description": section_description,
                    "order": section_order,
                },
            )
            for product_name, product_description, product_order in products:
                ProductItem.objects.update_or_create(
                    section=section,
                    name=product_name,
                    defaults={
                        "description": product_description,
                        "order": product_order,
                    },
                )


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio_app", "0006_seed_branding_product_sections"),
    ]

    operations = [
        migrations.RunPython(seed_remaining_graphic_design_sections, migrations.RunPython.noop),
    ]
