# Generated by Django 4.2.3 on 2023-07-23 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0002_alter_categoria_nome'),
    ]

    operations = [
        migrations.AddField(
            model_name='transacao',
            name='descricao',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
