from django.db import models,transaction
from core_utils.region_data.models import CityModel, CountryModel, StateModel
import uuid
from user_config.accounts.enums import UserRoleEnum
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.apps import apps
from core_utils.utils.generics.generic_models import CoreGenericModel
# Create your models here.


class UserRoleModel(CoreGenericModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        db_column="USER_ROLE_ID"
    )

    title = models.CharField(
        max_length=100,
        null= True,
        blank=True,
        db_column="TITLE",
    )

    role = models.CharField(
        max_length=50,
        choices=UserRoleEnum.choices(),
        db_column="ROLE"
    )


class CustomUserManager(BaseUserManager):
    """
    Object Manager for UserModel
    """

    def create_user(
        self,email : str, password : str , **extra_fields
    ):
        """
        This is a manager method to create a user
        """
        with transaction.atomic():
            if not email:
                raise ValueError("Email is required")
            
            user : AbstractBaseUser = self.model(email=email, **extra_fields)

            if password :
                user.set_password(password)
            user.save(using=self._db)
            
            user_detail_model = apps.get_model("UserDetailModel_user")

            user_detail_model.objects.create(user=user)
        
        return user
    
    def create_superuser(self , email :str , password : str , **extra_fields):
        """
        This is a manager method to create a superuser
        """
        extra_fields :dict = {
            "is_superuser": True,
            "is_active": True,
            "is_staff": True,
        }

        return self.create_user(email=email,password=password,**extra_fields)



class UserModel(AbstractBaseUser,PermissionsMixin,CoreGenericModel):
    id = models.UUIDField(
        unique=True,
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='USER_ID'
    )

    username = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_column='USERNAME'
    )

    first_name = models.CharField(
        max_length=50,
        db_column="FIRST_NAME"
    )

    last_name = models.CharField(
        max_length=50,
        db_column="LAST_NAME"
    )

    email = models.EmailField(
        unique=True,
        max_length=100,
        db_column="EMAIL"
    )

    phone_number = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        db_column="PHONE_NUMBER"
    )

    user_role = models.ForeignKey(
        UserRoleModel,
        on_delete=models.CASCADE,
        related_name='UserModel_user_role',
        db_column="USER_ROLE_ID"
    )

    is_active = models.BooleanField(
        default=True,
        db_column="IS_ACTIVE"
    )

    is_staff = models.BooleanField(
        default=False,
        db_column="IS_STAFF"
    )

    is_superuser = models.BooleanField(
        default=False,
        db_column="IS_SUPERUSER"
    )

    USERNAME_FIELD ='email'
    
    objects = CustomUserManager()


class UserDetailModel(CoreGenericModel):
    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        related_name='UserDetailModel_user',
        unique=True,
        db_column="USER_DETAIL_ID"
    )

    profile_photo = models.URLField(
        max_length=100,
        null=True,
        blank=True,
        db_column="PROFILE_PHOTO"
    )

    address = models.CharField(
        max_length=255,
        db_column="ADDRESS"
    )

    city = models.ForeignKey(
        CityModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='UserDetailModel_city',
        db_column="CITY_ID"
    )

    state = models.ForeignKey(
        StateModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='UserDetailModel_state',
        db_column="STATE_ID"
    )

    country = models.ForeignKey(
        CountryModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='UserDetailModel_country',
        db_column="COUNTRY_ID"
    )

    postal_code = models.CharField(
        max_length=10,
        db_column="POSTAL_CODE"
    )
    
    emergency_contact_number = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        db_column="EMERGENCY_CONTACT_NUMBER"
    )

