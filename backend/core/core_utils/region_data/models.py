from django.db import models
from core_utils.utils.generics.generic_models import CoreGenericModel

# Create your models here.


class CountryModel(CoreGenericModel):
    id = models.BigAutoField(
        primary_key=True,
        db_column="COUNTRY_ID"
    )
    name = models.CharField(
        max_length=100,
        db_column="COUNTRY_NAME"
    )

class StateModel(CoreGenericModel):
    id = models.BigAutoField(
        primary_key=True,
        db_column="STATE_ID"
    )
    name = models.CharField(
        max_length=100,
        db_column="STATE_NAME"
    )
    country = models.ForeignKey(
        CountryModel,
        on_delete=models.CASCADE,
        related_name="StateModel_country"
    )

class CityModel(CoreGenericModel):
    id = models.BigAutoField(
        primary_key=True,
        db_column="CITY_ID"
    )
    name = models.CharField(
        max_length=100,
        db_column="CITY_NAME"
    )
    state = models.ForeignKey(
        StateModel,
        on_delete=models.CASCADE,
        related_name="CityModel_state"
    )
    country = models.ForeignKey(
        CountryModel,
        on_delete=models.CASCADE,
        related_name="CityModel_country"
    )

