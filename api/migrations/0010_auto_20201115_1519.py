# Generated by Django 3.0.8 on 2020-11-15 08:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20201101_0050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurantimagefile',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='restaurant_images', to='api.Restaurant'),
        ),
    ]