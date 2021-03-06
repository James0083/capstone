# Generated by Django 4.0.3 on 2022-06-12 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capstone', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Returntext',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sttAnswer', models.CharField(max_length=20, null=True, verbose_name='stt_text')),
            ],
        ),
        migrations.CreateModel(
            name='RightWrong',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=10, null=True, verbose_name='정답')),
            ],
        ),
        migrations.AlterField(
            model_name='document',
            name='title',
            field=models.CharField(max_length=64, null=True, verbose_name='첨부파일명'),
        ),
    ]
