# Generated by Django 4.0.4 on 2022-05-20 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newc', '0009_alter_product_type_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='element',
            name='newc_elemen_name_f6d4f9_idx',
        ),
        migrations.RemoveIndex(
            model_name='element',
            name='newc_elemen_symbol_da96b0_idx',
        ),
        migrations.AlterField(
            model_name='element',
            name='symbol',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['name'], name='newc_produc_name_a056ee_idx'),
        ),
    ]
