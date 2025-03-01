# Generated by Django 5.1.6 on 2025-02-24 15:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0003_rename_content_questionanswers_value_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='survey',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='questions', to='survey.survey'),
        ),
    ]
