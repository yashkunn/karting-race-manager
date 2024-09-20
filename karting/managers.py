from django.contrib.auth.models import UserManager, AbstractUser


class CustomUserManager(UserManager):

    def create_superuser(
            self,
            username,
            email=None,
            password=None,
            **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        extra_fields["date_of_birth"] = "2000-01-01"

        return self.create_user(username, email, password, **extra_fields)
