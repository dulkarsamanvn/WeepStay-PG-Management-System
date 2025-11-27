from django.db import models
class CoreGenericModel(models.Model):
    core_generic_created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        db_column="CORE_GENERIC_CREATED_AT"
    )

    core_generic_updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        db_column="CORE_GENERIC_UPDATED_AT"
    )

    core_generic_created_by = models.ForeignKey(
        'user_auth.UserDetailModel',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        db_column="CORE_GENERIC_CREATED_BY"
    )
    
    core_generic_updated_by = models.ForeignKey(
        'user_auth.UserDetailModel',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        db_column='CORE_GENERIC_UPDATED_BY'
    )

    class Meta:
        abstract = True
