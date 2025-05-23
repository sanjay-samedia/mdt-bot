# Generated by Django 5.2 on 2025-05-16 12:59

import apps.bot.models
import django.contrib.postgres.fields
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=256, unique=True)),
                ('name', models.CharField(max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='BotInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('requested_visits', models.PositiveIntegerField(help_text='Number of visits requested')),
                ('visits_sent', models.PositiveIntegerField(default=0, help_text='Number of visits actually sent')),
                ('successful_visits', models.PositiveIntegerField(default=0, help_text='Number of visits successful sent')),
                ('start_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('min_stay_time', models.PositiveIntegerField(default=0, help_text='Minimum stay time during a visit in seconds.', validators=[django.core.validators.MinValueValidator(0)])),
                ('max_stay_time', models.PositiveIntegerField(default=0, help_text='Maximum stay time during a visit in seconds.', validators=[django.core.validators.MinValueValidator(0)])),
                ('status', models.CharField(choices=apps.bot.models.BotStatus.choices, default='STOPPED', max_length=20)),
                ('success_rate', models.CharField(max_length=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('task_ids', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=36), blank=True, default=list, size=None)),
                ('bot_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bot_instances', to='accounts.botuser')),
                ('website', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bot_instances', to='bot.website')),
            ],
        ),
        migrations.CreateModel(
            name='TaskLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.CharField(max_length=36)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('bot_instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_logs', to='bot.botinstance')),
            ],
        ),
        migrations.AddIndex(
            model_name='botinstance',
            index=models.Index(fields=['bot_user', 'status'], name='bot_botinst_bot_use_f77eca_idx'),
        ),
    ]
