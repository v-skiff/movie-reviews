# Generated by Django 2.2.6 on 2019-10-21 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='movie',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.Movie'),
        ),
    ]