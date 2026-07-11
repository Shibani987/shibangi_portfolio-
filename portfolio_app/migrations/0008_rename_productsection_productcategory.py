import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio_app", "0007_seed_remaining_graphic_design_sections"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="ProductSection",
            new_name="ProductCategory",
        ),
        migrations.RenameField(
            model_name="productitem",
            old_name="section",
            new_name="category",
        ),
        migrations.AlterModelOptions(
            name="productcategory",
            options={
                "ordering": ["order", "name"],
                "verbose_name": "Product category",
                "verbose_name_plural": "Product categories",
            },
        ),
        migrations.AlterField(
            model_name="productcategory",
            name="subcategory",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product_categories",
                to="portfolio_app.subcategory",
            ),
        ),
        migrations.AlterField(
            model_name="productitem",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="products",
                to="portfolio_app.productcategory",
            ),
        ),
    ]
