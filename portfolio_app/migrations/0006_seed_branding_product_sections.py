from django.db import migrations


SECTIONS = [
    (
        "Products",
        "Custom-designed branding elements for products and services.",
        1,
        [
            ("Shampoo bottle", "Custom label design for a natural haircare product.", 1),
            (
                "Niacinamide Serum",
                "Custom packaging design for a skincare product with a modern, clean aesthetic.",
                2,
            ),
        ],
    ),
    (
        "Logos",
        "Distinctive logo designs that capture the essence and values of a brand.",
        2,
        [
            ("Brand Logo 1", "A minimalist logo design featuring clean lines and a modern font.", 1),
            (
                "Brand Logo 2",
                "A bold, abstract logo design that conveys innovation and creativity.",
                2,
            ),
        ],
    ),
    (
        "Business Cards",
        "Custom-designed business cards that reflect the personality and values of a brand.",
        3,
        [
            (
                "Business Card 1",
                "A minimalist business card design with a clean layout and modern typography.",
                1,
            ),
            (
                "Business Card 2",
                "A bold, abstract business card design that conveys innovation and creativity.",
                2,
            ),
        ],
    ),
]


def seed_branding_product_sections(apps, schema_editor):
    SubCategory = apps.get_model("portfolio_app", "SubCategory")
    ProductSection = apps.get_model("portfolio_app", "ProductSection")
    ProductItem = apps.get_model("portfolio_app", "ProductItem")

    branding = SubCategory.objects.filter(slug="branding", category__slug="graphic-design").first()
    if not branding:
        return

    for section_name, section_description, section_order, products in SECTIONS:
        section, _ = ProductSection.objects.update_or_create(
            subcategory=branding,
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
        ("portfolio_app", "0005_productsection_productitem"),
    ]

    operations = [
        migrations.RunPython(seed_branding_product_sections, migrations.RunPython.noop),
    ]
