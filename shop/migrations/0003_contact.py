# Generated by Django 5.1.5 on 2025-02-08 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_product_category_product_image_product_price_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('msgid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(default='', max_length=30)),
                ('phone', models.CharField(default='', max_length=30)),
                ('desc', models.CharField(default='', max_length=500)),
            ],
        ),
    ]
