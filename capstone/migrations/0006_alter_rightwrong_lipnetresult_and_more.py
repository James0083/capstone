# Generated by Django 4.0.3 on 2022-06-14 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capstone', '0005_rightwrong_presentword'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rightwrong',
            name='LipNetResult',
            field=models.CharField(max_length=64, null=True, verbose_name='LipNetResult'),
        ),
        migrations.AlterField(
            model_name='rightwrong',
            name='presentWord',
            field=models.CharField(max_length=64, null=True, verbose_name='presentWord'),
        ),
        migrations.AlterField(
            model_name='rightwrong',
            name='sttResult',
            field=models.CharField(max_length=64, null=True, verbose_name='sttResult'),
        ),
    ]
