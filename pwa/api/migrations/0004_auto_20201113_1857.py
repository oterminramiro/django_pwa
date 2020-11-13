# Generated by Django 3.1.3 on 2020-11-13 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('key', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='api.taskstatus'),
            preserve_default=False,
        ),
    ]
