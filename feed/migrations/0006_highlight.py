# Generated by Django 3.1.2 on 2020-10-13 20:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feed', '0005_story'),
    ]

    operations = [
        migrations.CreateModel(
            name='Highlight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('highlight_name', models.CharField(max_length=200)),
                ('highlight_pic', models.ImageField(upload_to='media/photos/highlights')),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='highlight_posted_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
