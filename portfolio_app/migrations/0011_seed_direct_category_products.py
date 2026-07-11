from django.db import migrations


CATEGORIES = {
    "photography": {
        "name": "Photography",
        "description": "Showcasing visual stories through portrait, travel, and lifestyle photography.",
        "order": 2,
        "product_categories": [
            (
                "Black and White",
                "Timeless monochrome moments defined by contrast, texture, and emotion.",
                1,
                [
                    ("Midnight Streets", "Moody urban scenes captured in rich shadow and soft grain.", 1),
                    ("Quiet Faces", "Subtle portraits that emphasize expression over color.", 2),
                ],
            ),
            (
                "Colour",
                "Vivid frames full of atmosphere, warmth, and visual energy.",
                2,
                [
                    ("Golden Hour", "Warm, glowing scenes that celebrate light and movement.", 1),
                    ("Color Stories", "Bold and playful compositions that bring everyday moments to life.", 2),
                ],
            ),
        ],
    },
    "art": {
        "name": "Traditional & Digital Art",
        "description": "Exploring expressive works shaped by traditional techniques and digital innovation.",
        "order": 3,
        "product_categories": [
            (
                "Sceneries",
                "Atmospheric landscapes and immersive views shaped by light, mood, and natural movement.",
                1,
                [
                    ("Golden Horizon", "A soft sunset scene with layered skies and calm, reflective tones.", 1),
                    ("Forest Drift", "Dense woodland imagery blending depth, texture, and quiet atmosphere.", 2),
                ],
            ),
            (
                "Portraits",
                "Expressive character studies focused on emotion, identity, and human presence.",
                2,
                [
                    ("Quiet Expression", "A contemplative portrait with subtle shading and delicate detail.", 1),
                    ("Modern Muse", "Bold lines and softened color create a confident, modern presence.", 2),
                ],
            ),
            (
                "Surreal",
                "Dreamlike visuals and imaginative compositions that push beyond the ordinary.",
                3,
                [
                    ("Dreamscape", "An abstract world of floating forms, cosmic light, and symbolic imagery.", 1),
                    ("Midnight Bloom", "Surreal floral imagery wrapped in shadow, glow, and mysterious motion.", 2),
                ],
            ),
        ],
    },
}


def seed_direct_category_products(apps, schema_editor):
    Category = apps.get_model("portfolio_app", "Category")
    ProductCategory = apps.get_model("portfolio_app", "ProductCategory")
    ProductItem = apps.get_model("portfolio_app", "ProductItem")

    for slug, data in CATEGORIES.items():
        category = Category.objects.filter(slug=slug).first()
        if not category:
            category = Category.objects.filter(name=data["name"]).first()
        if not category:
            category = Category.objects.create(
                slug=slug,
                name=data["name"],
                description=data["description"],
                order=data["order"],
            )
            created = True
        else:
            created = False
        update_fields = []
        if category.slug != slug:
            category.slug = slug
            update_fields.append("slug")
        if not category.description:
            category.description = data["description"]
            update_fields.append("description")
        if created or not category.order:
            category.order = data["order"]
            update_fields.append("order")
        if update_fields:
            category.save(update_fields=update_fields)

        for category_name, category_description, category_order, products in data["product_categories"]:
            product_category, _ = ProductCategory.objects.update_or_create(
                category=category,
                subcategory=None,
                name=category_name,
                defaults={
                    "description": category_description,
                    "order": category_order,
                },
            )
            for product_name, product_description, product_order in products:
                ProductItem.objects.update_or_create(
                    category=product_category,
                    name=product_name,
                    defaults={
                        "description": product_description,
                        "order": product_order,
                    },
                )


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio_app", "0010_remove_productcategory_unique_product_category_per_subcategory_and_more"),
    ]

    operations = [
        migrations.RunPython(seed_direct_category_products, migrations.RunPython.noop),
    ]
