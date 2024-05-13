from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# from
# from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    profile_image = models.ImageField(
        verbose_name='Картинка профиля',
        upload_to="photos/%Y/%m/%d",
        blank=True,
        null=True,
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата рождения"
    )

    def __str__(self) -> str:
        return f'Профиль {self.user.username}'


# class UserAccountManager(BaseUserManager):
#     use_in_migrations = True

#     def _create_user(self, username, password, **extra_fields):
#         if not username:
#             raise ValueError('Username must be provided')
#         if not password:
#             raise ValueError('Password must be provided')

#         # email = self.normalize_email(email)

#         user = self.model(username=username, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_user(self, email=None, password=None, **extra_fields):
#         return self._create_user(email, password, **extra_fields)

#     def create_superuser(self, email, password, **extra_fields):
#         extra_fields['is_stuff'] = True
#         extra_fields['is_superuser'] = True
#         return self._create_user(email, password, **extra_fields)


# class User(AbstractBaseUser, PermissionsMixin):
#     REQUIRED_FIELDS = []
#     USERNAME_FIELD = 'email'
