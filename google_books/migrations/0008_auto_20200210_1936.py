# Generated by Django 3.0.3 on 2020-02-10 19:36

from django.db import migrations, models
import google_books.models


class Migration(migrations.Migration):

    dependencies = [
        ('google_books', '0007_auto_20200210_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='publishedDay',
            field=models.IntegerField(null=True, validators=[google_books.models.validate_day]),
        ),
        migrations.AlterField(
            model_name='book',
            name='publishedMonth',
            field=models.IntegerField(null=True, validators=[google_books.models.validate_month]),
        ),
        migrations.AlterField(
            model_name='book',
            name='publishedYear',
            field=models.IntegerField(null=True, validators=[google_books.models.validate_year]),
        ),
    ]