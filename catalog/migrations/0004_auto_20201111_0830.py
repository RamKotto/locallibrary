# Generated by Django 3.1.1 on 2020-11-11 05:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0003_book_language'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['last_name'], 'verbose_name': 'Автор', 'verbose_name_plural': 'Авторы'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'verbose_name': 'Жанр', 'verbose_name_plural': 'Жанры'},
        ),
        migrations.AddField(
            model_name='bookinstance',
            name='borrower',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='book',
            name='language',
            field=models.ForeignKey(help_text='Select language', null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.language'),
        ),
    ]
