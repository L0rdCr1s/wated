from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from time import strftime, gmtime
from django.utils import timezone
from django.conf import settings


class CustomManager(BaseUserManager):
    """
        Database table manager for users table, used to create new users and store them into
        the custom users table
    """

    def _create_user(self, email=None, password=None, is_superuser=False, is_staff=False, is_active=False):

        # validate email and password
        # raise value error if email and password are not given
        if email is None:
            raise ValueError("users must have an email")
        if password is None:
            raise ValueError("users must have a password")

        user = self.model(
            email=self.normalize_email(email),
            is_superuser=is_superuser,
            is_staff=is_staff,
            is_active=is_active,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **kwargs):
        user = self._create_user(email, password, is_staff=False, is_superuser=False, is_active=False)
        user.first_name = kwargs['first_name']
        user.last_name = kwargs['last_name']
        user.date_joined = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        user.last_login = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self._create_user(email, password, is_superuser=True, is_staff=True, is_active=True)
        user.first_name = kwargs['first_name']
        user.last_name = kwargs['last_name']
        user.date_joined = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        user.last_login = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    """
        This is the user database table, it is called custom user because
        it is customised from django default User model
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    is_active = models.BooleanField(default=False)  # can use the account
    is_staff = models.BooleanField(default=False)  # has modrate priviledges
    is_superuser = models.BooleanField(default=False)  # has all priviledges
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', ]

    class Meta:
        indexes = [
            models.Index(fields=['first_name']),
            models.Index(fields=['last_name']),
        ]

    objects = CustomManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.last_name

    def get_username(self):
        return self.email

    @staticmethod
    def has_perm(obj=None):
        return True

    @staticmethod
    def has_module_perms(app_label):
        return True


class UserProfile(models.Model):
    """
        This is the userprofile table, it is separated from customuser (User)
        table because it can frequently be modified without disturbing the user table,
        it holds all the details about the users profile
    """

    # gender choices for the users
    Female = 'F'
    Male = 'M'
    gender_choices = [(Female, 'F'), (Male, 'M')]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activation_key = models.IntegerField(blank=True)  # to activate user account
    activation_key_expirity = models.DateTimeField()
    profile_picture = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
    bio = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(default=timezone.now)
    geder = models.CharField(max_length=1, default=Male, choices=gender_choices)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['date_of_birth']),
        ]

    objects = models.Manager()  # can be removed

    def __str__(self):
        return self.user.get_full_name()


class Category(models.Model):
    """
        This is categories table, it holds all sectors the site is devided to,
        be carefull when editing this as it has many relations with other tables
    """
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class TaasisiManager(BaseUserManager):
    """
        This is the Taasisi manager as how the CustomUserManager is,
        creates new Taasisi and save them to the database as Taasisi table is designed,
        use it the same way you use CustomManager
    """

    def _create_user(self, email=None, password=None, is_superuser=False, is_staff=False, is_active=False):
        if email is None:
            raise ValueError("users must have an email")
        if password is None:
            raise ValueError("users must have a password")

        user = self.model(
            email=self.normalize_email(email),
            is_superuser=is_superuser,
            is_staff=is_staff,
            is_active=is_active,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **kwargs):
        user = self._create_user(email, password, is_staff=False, is_superuser=False, is_active=False)
        user.name = kwargs['name']
        user.date_joined = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        user.last_login = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        user.save(using=self._db)
        return user


class Taasisi(AbstractBaseUser):
    """
        This is basically the CustomUSer table but it is used to store
        Taasisi, use it the same way you use CustomUser
    """
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', ]

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['email']),
        ]

    objects = TaasisiManager()

    def __str__(self):
        return self.name

    def get_short_name(self):
        return self.name

    @staticmethod
    def has_perm(obj=None):
        return True

    @staticmethod
    def has_module_perms(app_label):
        return True


class TaasisiProfile(models.Model):
    """
        This is basicaly same as User profile, it holds Taasisi profile info,
        use it same way as you use UserProfile
    """
    category = models.ForeignKey(Category, default=1, on_delete=models.CASCADE)
    taasisi = models.OneToOneField(Taasisi, on_delete=models.CASCADE)
    cover_image = models.ImageField()
    bio = models.CharField(max_length=600)
    services = models.TextField()
    location = models.CharField(max_length=255)

    class Meta:
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['taasisi']),
            models.Index(fields=['services'])
        ]

    def __str__(self):
        return self.bio
