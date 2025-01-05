# Generated by Django 5.1.2 on 2025-01-02 14:33

import se_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("se_app", "0006_alter_customer_name_alter_product_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="name",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(
                decimal_places=3,
                max_digits=50,
                validators=[se_app.models.validate_positive],
            ),
        ),
    ]
