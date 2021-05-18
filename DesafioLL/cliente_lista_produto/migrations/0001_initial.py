# Generated by Django 3.2.3 on 2021-05-18 00:11

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=200)),
                ('email', models.EmailField(default='', max_length=200)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('deleted', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_product', models.UUIDField()),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('id_client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cliente_lista_produto.client')),
            ],
        ),
    ]
