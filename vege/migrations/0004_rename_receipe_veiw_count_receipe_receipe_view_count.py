# Generated by Django 4.2.7 on 2023-11-12 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vege', '0003_receipe_receipe_veiw_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='receipe',
            old_name='receipe_veiw_count',
            new_name='receipe_view_count',
        ),
    ]
