# Generated by Django 4.2.11 on 2024-03-21 03:25

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import ecshopapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User_Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('user_name', models.CharField(max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='ユーザー名')),
                ('user_email', models.EmailField(max_length=255, unique=True, verbose_name='メールアドレス')),
                ('user_nickname', models.CharField(default='', max_length=150, verbose_name='会社名')),
                ('user_point', models.IntegerField(default=0, verbose_name='ポイント')),
                ('user_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='登録時間')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False, verbose_name='管理権限')),
            ],
            options={
                'verbose_name': '会員情報',
                'verbose_name_plural': 'users_member',
                'db_table': 'ecshop_user_member_list',
                'abstract': False,
                'swappable': 'AUTH_USER_MODEL',
            },
            managers=[
                ('objects', ecshopapp.models.MyUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='商品名')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='商品価格')),
                ('stock', models.IntegerField(default=1, verbose_name='商品在庫')),
                ('goods_type', models.CharField(max_length=30, verbose_name='商品タイプ')),
                ('publishings', models.CharField(max_length=30, verbose_name='商品メーカー')),
                ('sales', models.IntegerField(default=0, verbose_name='商品売上')),
                ('add_datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='入荷時間')),
                ('status', models.SmallIntegerField(choices=[(0, 'offline'), (1, 'online')], default=1, verbose_name='商品ステータス')),
                ('image', models.ImageField(upload_to='goods', verbose_name='商品画像')),
            ],
            options={
                'verbose_name': '商品表',
                'verbose_name_plural': '商品表',
                'db_table': 'ecshop_Goods',
            },
        ),
        migrations.CreateModel(
            name='UserAddresses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiver', models.CharField(max_length=26, verbose_name='会社名')),
                ('addr', models.CharField(max_length=256, verbose_name='お届け先')),
                ('zip_code', models.CharField(max_length=15, null=True, verbose_name='郵便番号')),
                ('phone', models.CharField(max_length=26, verbose_name='電話番号')),
                ('is_default', models.BooleanField(default=False, verbose_name='デフォルト')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
            options={
                'verbose_name': '住所',
                'verbose_name_plural': '住所',
                'db_table': 'ecshop_user_address',
            },
        ),
    ]