# Generated by Django 4.0.4 on 2022-05-23 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chargemix', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='type',
            field=models.CharField(choices=[('furnace_mat', 'furnace material'), ('ladle_mat', 'ladle material'), ('additive', 'additive'), ('nodularization_mat', 'nodularization material')], default='furnace_mat', max_length=50),
        ),
    ]
