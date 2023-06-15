# Generated by Django 4.2 on 2023-06-14 11:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, null=True)),
                ('text', models.TextField(null=True)),
                ('attachment', models.BinaryField(blank=True, editable=True, null=True)),
                ('attachment_type', models.CharField(blank=True, max_length=150, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('by_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AnnouncementCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('TK', 'Tank'), ('HL', 'Heal'), ('DD', 'Damage Dealer'), ('TD', 'Treader'), ('GM', 'GuuldMaster'), ('QG', 'Quest Giver'), ('SM', 'Smith'), ('TN', 'Tanner'), ('PM', 'Poison Master'), ('SM', 'Spell Master')], max_length=2, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AnnouncementSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='announcement.announcementcategory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AnnouncementResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TimeField(null=True)),
                ('is_taken', models.BooleanField(null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('announcement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='announcement.announcement')),
                ('by_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='responce', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='announcement',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='anouncement', to='announcement.announcementcategory'),
        ),
    ]
