# Generated by Django 2.2.8 on 2020-02-18 23:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('amount', models.PositiveIntegerField()),
                ('is_paid', models.BooleanField(default=False)),
                ('payment_id', models.PositiveIntegerField(null=True, unique=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.Cart')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
