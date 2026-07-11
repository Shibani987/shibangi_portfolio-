from django.db import migrations
from django.utils.text import slugify


def unique_slug(SubCategory, base_slug):
    slug = base_slug
    counter = 2
    while SubCategory.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug


def move_direct_product_categories(apps, schema_editor):
    Category = apps.get_model("portfolio_app", "Category")
    SubCategory = apps.get_model("portfolio_app", "SubCategory")
    ProductCategory = apps.get_model("portfolio_app", "ProductCategory")

    for category in Category.objects.all():
        direct_groups = ProductCategory.objects.filter(category=category, subcategory__isnull=True)
        if not direct_groups.exists():
            continue

        subcategory = SubCategory.objects.filter(category=category).order_by("order", "name").first()
        if not subcategory:
            base_slug = slugify(f"{category.slug or category.name}-featured-work")
            subcategory = SubCategory.objects.create(
                category=category,
                name="Featured Work",
                slug=unique_slug(SubCategory, base_slug),
                description=category.description,
                order=0,
            )

        direct_groups.update(subcategory=subcategory, category=None)


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio_app", "0019_siteprofile_cv_url"),
    ]

    operations = [
        migrations.RunPython(move_direct_product_categories, migrations.RunPython.noop),
    ]
