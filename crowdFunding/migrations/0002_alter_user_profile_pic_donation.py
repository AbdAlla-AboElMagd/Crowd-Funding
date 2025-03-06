# Generated by Django 5.1.6 on 2025-03-06 03:54

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crowdFunding', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(1)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donations', to='crowdFunding.project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
