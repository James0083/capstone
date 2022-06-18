# Generated by Django 4.0.3 on 2022-06-14 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capstone', '0007_alter_rightwrong_lipnetresult_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Notice',
        ),
        migrations.DeleteModel(
            name='Returntext',
        ),
        migrations.AddField(
            model_name='rightwrong',
            name='LipNetAnswer',
            field=models.CharField(max_length=20, null=True, verbose_name='독순결과'),
        ),
        migrations.AddField(
            model_name='rightwrong',
            name='sttAnswer',
            field=models.CharField(max_length=20, null=True, verbose_name='stt결과'),
        ),
        migrations.AlterField(
            model_name='rightwrong',
            name='LipNetResult',
            field=models.CharField(max_length=64, null=True, verbose_name='독순비교결과'),
        ),
        migrations.AlterField(
            model_name='rightwrong',
            name='sttResult',
            field=models.CharField(max_length=64, null=True, verbose_name='stt비교결과'),
        ),
    ]