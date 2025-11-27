from django.db import models
from core_utils.utils.generics.generic_models import CoreGenericModel
import uuid
from user_config.user_auth.models import UserModel

# Create your models here.

class BlackListTokenModel(CoreGenericModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column="BLACK_LIST_TOKEN_ID"
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='BlackListTokenModel_user',
        db_column="USER_ID"
    )

    token = models.TextField(
        db_column="JWT_TOKEN"
    )

    is_login = models.BooleanField(
        default=False,
        db_column="IS_LOGIN"
    )

    is_delete = models.BooleanField(
        default=False,
        db_column="IS_DELETE"
    )



    