# Generated by Django 3.0.3 on 2020-02-10 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('google_books', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='names',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='author',
            name='surname',
        ),
    ]
