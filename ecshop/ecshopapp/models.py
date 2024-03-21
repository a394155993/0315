from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User,BaseUserManager, AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from mdeditor.fields import MDTextField




class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, user_name, user_email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not user_name:
            raise ValueError("The given username must be set")
        user_email = self.normalize_email(user_email)
        user = self.model(user_name=user_name, user_email=user_email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, user_name, user_email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(user_name, user_email, password, **extra_fields)

    def create_superuser(self, user_name, user_email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(user_name, user_email, password, **extra_fields)


class MyUser(AbstractBaseUser):
    username_validator = UnicodeUsernameValidator()
    user_name = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
        verbose_name='ユーザー名',
    )
    user_email = models.EmailField(
        verbose_name='メールアドレス',
        max_length=255,
        unique=True,
        editable=True
    )
    user_nickname = models.CharField(
        max_length=150,
        verbose_name='会社名',
        default=''
    )
    user_point = models.IntegerField(verbose_name='ポイント', default=0, editable=True)
    user_joined = models.DateTimeField(verbose_name='登録時間', default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(verbose_name='管理権限', default=False)

    objects = MyUserManager()
    EMAIL_FIELD = "user_email"
    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['user_email']

    def get_full_name(self):
        # The user is identified by their email address
        return self.user_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.user_name

    def __str__(self):  # __unicode__ on Python 2
        return self.user_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Email this user."""
        send_mail(subject, message, from_email, [self.user_email], **kwargs)

    class Meta:
        db_table = 'ecshop_user_member_list'
        verbose_name = "会員情報"
        verbose_name_plural = "users_member"
        abstract = True

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

class User_Member(MyUser):
    """
    Users within the Django authentication system are represented by this
    model.

    Username and password are required. Other fields are optional.
    """

    class Meta(MyUser.Meta):
        swappable = "AUTH_USER_MODEL"   



class Goods(models.Model):
    """Goods Table"""
    status_choices = (
        (0, "offline"),
        (1, "online"),
    )

    name = models.CharField(max_length=30, verbose_name="商品名")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="商品価格")
    stock = models.IntegerField(default=1, verbose_name="商品在庫")
    goods_type = models.CharField(max_length=30, verbose_name="商品タイプ")
    publishings = models.CharField(max_length=30, verbose_name="商品メーカー") 
    sales = models.IntegerField(default=0, verbose_name="商品売上")
    add_datetime = models.DateTimeField(default=timezone.now, verbose_name="入荷時間")
    status = models.SmallIntegerField(choices=status_choices, default=1, verbose_name="商品ステータス")
    image = models.ImageField(upload_to='goods', verbose_name='商品画像')
    content = MDTextField(verbose_name='商品詳細', default=None)

    class Meta:
        db_table = "ecshop_Goods"
        verbose_name = "商品表"
        verbose_name_plural = "商品表"

class UserAddresses(models.Model):
    """UserAddresses Table"""
    user = models.ForeignKey(User_Member, verbose_name='ユーザー', on_delete=models.CASCADE)
    receiver = models.CharField(max_length=26, verbose_name='会社名')
    addr = models.CharField(max_length=256, verbose_name='お届け先')
    zip_code = models.CharField(max_length=15, null=True, verbose_name='郵便番号')
    phone = models.CharField(max_length=26, verbose_name='電話番号')
    is_default = models.BooleanField(default=False, verbose_name='デフォルト')

    def __str__(self):
        return '会社名: %s,\n お届け先: %s,\n 電話番号: %s' % (self.receiver, self.addr, self.phone)

    class Meta:
        db_table = 'ecshop_user_address'
        verbose_name = '住所'
        verbose_name_plural = verbose_name

