# Generated by Django 4.2.3 on 2023-07-24 08:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "ecommerce",
            "0004_order_alter_product_image_alter_product_thumbnail_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="zip_code",
            field=models.CharField(max_length=9),
        ),
    ]
