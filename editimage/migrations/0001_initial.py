# Generated by Django 5.0.7 on 2024-10-09 14:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EditImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_image', models.ImageField(upload_to='original_images/')),
                ('edited_image', models.ImageField(blank=True, null=True, upload_to='edited_images/')),
                ('prompt', models.TextField(blank=True, null=True)),
                ('steps', models.IntegerField(default=50)),
                ('cfg_scale', models.FloatField(default=7.0)),
                ('denoising_strength', models.FloatField(default=0.75)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
