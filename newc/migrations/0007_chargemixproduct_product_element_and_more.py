# Generated by Django 4.0.4 on 2022-05-20 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newc', '0006_alter_product_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='chargemixproduct',
            name='product_element',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='chargemixproduct',
            name='product_qty_roundoff',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.DeleteModel(
            name='ChargemixProductElement',
        ),
    ]