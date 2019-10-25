# Generated by Django 2.2.6 on 2019-10-15 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20191013_0922'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='review_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='img',
            field=models.ImageField(upload_to='books_images'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='release_date',
            field=models.DateField(null=True),
        ),
    ]
