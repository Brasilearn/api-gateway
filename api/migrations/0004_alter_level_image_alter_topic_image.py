# Generated by Django 4.2.13 on 2024-06-19 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_userprofile_alter_userskills_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='level',
            name='image',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='topic',
            name='image',
            field=models.TextField(blank=True, null=True),
        ),
    ]
