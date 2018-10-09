from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.conf import settings
from sautiYangu.models import Category


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
        user.user_role = kwargs['user_role']
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self._create_user(email, password, is_superuser=True, is_staff=True, is_active=True)
        user.user_role = kwargs['user_role']
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    """
        This is the user database table, it is called custom user because
        it is customised from django default User model
    """
    # user role choices
    normal_user = 'U'
    institute_user = 'I'
    user_choices = [
        (normal_user, 'User'),
        (institute_user, 'Institute')
    ]

    email = models.EmailField(unique=True)
    user_role = models.CharField(max_length=1, choices=user_choices, default=normal_user, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)
    activation_key = models.IntegerField(blank=True, default=1)
    activation_key_expirity = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_role', ]

    class Meta:
        indexes = [
            models.Index(fields=['user_role']),
            models.Index(fields=['email']),
        ]

    objects = CustomManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

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
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    profile_picture = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
    bio = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(default=timezone.now)
    geder = models.CharField(max_length=1, default=Male, choices=gender_choices)

    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['date_of_birth']),
        ]

    objects = models.Manager()  # can be removed

    def __str__(self):
        return self.user.get_full_name()

    def get_full_name(self):
        return self.first_name + " " + self.last_name


class InstituteProfile(models.Model):
    """
        This is basicaly same as User profile, it holds Taasisi profile info, 
        use it same way as you use UserProfile
    """
    institute = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, default=1, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    cover_image = models.ImageField()
    bio = models.CharField(max_length=255)
    services = models.TextField()
    location = models.CharField(max_length=255)

    objects = models.Manager()

    REQUIRED_FIELDS = ['name',]

    class Meta:
        indexes = [
            models.Index(fields=['institute']),
        ]

    def __str__(self):
        return self.bio

    def get_full_name(self):
        return self.name


class UserFollow(models.Model):
    following = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="following_user", db_index=True)
    followed = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField(default=timezone.now)

    objects = models.Manager()

    def __str__(self):
        return self.following.get_full_name()

