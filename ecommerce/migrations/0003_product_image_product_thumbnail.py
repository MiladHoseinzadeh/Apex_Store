# Generated by Django 4.2 on 2023-05-25 20:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ecommerce", "0002_alter_category_options_product"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="uploads"),
        ),
        migrations.AddField(
            model_name="product",
            name="thumbnail",
            field=models.ImageField(blank=True, null=True, upload_to="uploads"),
        ),
    ]
