# Generated by Django 3.2 on 2022-04-26 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='title',
            new_name='product_category',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='product_id',
            new_name='brand_name',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='original_price',
            new_name='price',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='category',
            new_name='product_category',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='highlights',
            new_name='product_description',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='title',
            new_name='product_name',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='avg_rating',
            new_name='rating',
        ),
    ]
