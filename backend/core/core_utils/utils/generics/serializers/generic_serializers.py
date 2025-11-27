from django.db.models import QuerySet,Model

class CoreGenericGetQuerysetSerializer:
    """
    Provides a base method to retrieve the queryset for serializers.
    """

    def get_queryset(self) -> QuerySet[Model] :
        """
        Retrieves the queryset from the class attribute or model.

        Returns:
            QuerySet[Model]: The queryset for the serializer.

        Raises:
            Exception: If neither queryset nor Meta.model is defined.
        """
        try :
            if hasattr(self,"queryset") and self.queryset is not None :
                return self.queryset.all()
            return self.Meta.model.objects.all()
        except Exception :
            raise Exception("Queryset is not defined for the serializer.")