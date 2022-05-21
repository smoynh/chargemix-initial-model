# Generated by Django 4.0.4 on 2022-05-19 06:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chargemix',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='')),
                ('furnace_size', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tapping_time', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tapping_temp', models.DecimalField(decimal_places=2, max_digits=10)),
                ('rate_per_unit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_elec_model', models.BooleanField(default=False)),
                ('use_elem_recov_rate', models.BooleanField(default=True)),
                ('fesimg_qty', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ChargemixProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_curr_qty', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product_final_qty', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product_min_qty', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product_max_qty', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product_qty_roundoff', models.IntegerField()),
                ('metal_recov_rate', models.DecimalField(decimal_places=2, max_digits=4)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='ChargemixProductElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('element', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Element',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('symbol', models.CharField(max_length=30)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('has_nodu', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('type', models.CharField(choices=[('furnace mat', 'furnace_material'), ('inoculant', 'inoculant'), ('additive', 'additive'), ('nodularization_mat', 'nodularization_material')], default='furnace_material', max_length=50)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddConstraint(
            model_name='product',
            constraint=models.CheckConstraint(check=models.Q(('price__gte', 1)), name='price_gte_1'),
        ),
        migrations.AddField(
            model_name='chargemixproductelement',
            name='chargemix_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chargemix_product', to='newc.chargemixproduct'),
        ),
        migrations.AddField(
            model_name='chargemixproduct',
            name='chargemix',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chargemix', to='newc.chargemix'),
        ),
        migrations.AddField(
            model_name='chargemixproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='newc.product'),
        ),
        migrations.AddField(
            model_name='chargemix',
            name='grade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grade', to='newc.grade'),
        ),
        migrations.AddConstraint(
            model_name='chargemixproduct',
            constraint=models.CheckConstraint(check=models.Q(('metal_recov_rate__lte', 100)), name='metal_recov_rate_lte_100'),
        ),
        migrations.AddConstraint(
            model_name='chargemixproduct',
            constraint=models.CheckConstraint(check=models.Q(('product_qty_roundoff__lte', 10)), name='product_qty_roundoff_lte_10'),
        ),
    ]