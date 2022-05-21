# Generated by Django 4.0.4 on 2022-05-20 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newc', '0008_chargemix_newc_charge_created_69d0fa_idx_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='type',
            field=models.CharField(choices=[('furnace_mat', 'furnace material'), ('inoculant', 'inoculant'), ('additive', 'additive'), ('nodularization_mat', 'nodularization material')], default='furnace_material', max_length=50),
        ),
        migrations.AddIndex(
            model_name='chargemix',
            index=models.Index(fields=['name'], name='newc_charge_name_29596d_idx'),
        ),
    ]
