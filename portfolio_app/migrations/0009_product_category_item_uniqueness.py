from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio_app", "0008_rename_productsection_productcategory"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="productcategory",
            constraint=models.UniqueConstraint(
                fields=("subcategory", "name"),
                name="unique_product_category_per_subcategory",
            ),
        ),
        migrations.AddConstraint(
            model_name="productitem",
            constraint=models.UniqueConstraint(
                fields=("category", "name"),
                name="unique_product_item_per_category",
            ),
        ),
    ]
