# Generated by Django 2.2.1 on 2019-07-30 11:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('helpline', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(verbose_name='시간')),
                ('txHash', models.CharField(max_length=64, verbose_name='TxHash')),
                ('user', models.CharField(max_length=10, verbose_name='user')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='helpline.Report', verbose_name='신고서')),
            ],
        ),
    ]
