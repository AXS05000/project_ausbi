# Generated by Django 4.2.3 on 2023-07-23 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='nome',
            field=models.CharField(choices=[('RC', 'Receitas'), ('GF', 'Gastos Fixos'), ('GV', 'Gastos Variáveis'), ('I', 'Investimentos')], max_length=2),
        ),
    ]