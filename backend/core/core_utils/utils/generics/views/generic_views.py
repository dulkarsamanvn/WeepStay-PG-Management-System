from core_utils.utils.generics.views.queryset import CoreGenericQueryset
from django.db.models.query import QuerySet
from django.db.models import Model
from rest_framework.request import Request
from rest_framework.serializers import Serializer
from typing import List,Dict
from backend.core.core_utils.utils.generics.views.queryset import CoreGenericQuerysetInstance
from backend.core.core_utils.utils.generics.views.process_view import CoreGenericProcessDataAPIView



class CoreGenericListAPIView(CoreGenericQueryset):
    """
    Generic GET API for returning a paginated queryset of model instances.

    This class expects a valid queryset and a serializer class.
    It handles pagination and returns serialized data accordingly.
    """

    queryset : QuerySet[Model]

    def list(self,request: Request, *args: List, **kwargs: Dict):
        """
        GET handler for listing model instances in a paginated format.

        Returns:
            - Paginated response with serialized model data.
        Raises:
            - Any error is caught and passed to the custom exception handler.
        """
        try :
            # ? Get paginated queryset from CoreGenericQueryset
            paginated_queryset : QuerySet[Model] = self.get_paginate_queryset()

            # ? Prepare context for serializer (can include request/user/etc.)
            context = self.set_context_data()

            #? serialize data
            serializer : Serializer = self.get_serializer(
                paginated_queryset,
                context = context,
                many=True
            )

            #? return paginated response with serializer data
            return self.get_paginated_response(serializer.data)
        
        except Exception as e :
            #? custom exception handler
            return self.custom_handle_exception(e=e)


class CoreGenericGetAPIView(CoreGenericQueryset,CoreGenericQuerysetInstance):
    """
    Generic GET API for returning one or more model instances based on the `many` flag.

    Attributes:
        many (bool):
            - True: Returns a queryset (list of objects).
            - False: Returns a single model instance.
    """
    queryset : QuerySet[Model]
    many : bool = True

    def get(self,request: Request, *args: List, **kwargs: Dict) :
        """
        GET handler for retrieving data using a serializer.

        Returns:
            - List or single object based on the `many` flag.
        """
        try :
            #? fetch queryset or single object
            if self.many :
                queryset : QuerySet[Model] = self.get_queryset()
            else :
                queryset : Model = self.get_object()
            
            # ? Prepare context for serializer (can include request/user/etc.)
            context = self.set_context_data()

            #? serialize data
            serializer : Serializer = self.get_serializer(
                queryset,
                context=context,
                many = self.many
            )

            return self.success_response(validated_data=serializer.data)
        except Exception as e :
            #? custom exception handler
            return self.custom_handle_exception(e=e)


class CoreGenericGetDataFromSerializerAPIView(CoreGenericProcessDataAPIView) :
    """
    GET API that executes business logic within a serializer.

    Use this when data needs to be calculated/processed via serializer logic
    (using `validate()` and `create()`) which are return inside handlers,
    rather than direct DB reads.
    """

    def get(self,request: Request, *args: List, **kwargs: Dict):
        """
        GET handler that routes logic through `handle_request()`
        which invokes validation and creation logic in the serializer.
        """
        return self.get_custom_response()


class CoreGenericPostAPIView(CoreGenericProcessDataAPIView) :
    """
    Generic POST API that processes input through a serializer.

    Useful when the logic resides inside the serializer’s `validate()`
    and `create()` methods which are return inside handlers.
    """
    def post(self,request: Request, *args: List, **kwargs: Dict) :
        """
        POST handler that passes request data through serializer logic.
        """
        return self.handle_request()


class CoreGenericCreateAPIView(CoreGenericProcessDataAPIView) :
    """
    View for executing create logic that is not necessarily tied to POST.

    Can be called internally or used for business logic simulations.
    """
    def create(self,request: Request, *args: List, **kwargs: Dict):
        """
        Handler for executing creation logic through a serializer.
        """
        return self.handle_request()


class CoreGenericListCreateAPIView(CoreGenericCreateAPIView,CoreGenericListAPIView):
    """
    Combines list and create views into a single view class.

    Supports:
        - GET: Paginated listing of model data
        - CREATE: Serializer-based object creation
    """

class CoreGenericPutAPIView(CoreGenericProcessDataAPIView) :
    """
    Generic PUT API to process update requests through custom logic.

    Ideal when you need validation and transformation before updating.
    """
    def put(self,request: Request, *args: List, **kwargs: Dict) :
        """
        PUT handler for updating data via serializer logic.
        """
        return self.handle_request()

class CoreGenericDeleteAPIView(CoreGenericProcessDataAPIView) :
    """
    Generic DELETE API to handle deletion logic through serializers.

    Use this when business rules are involved in deletion,
    such as soft deletes, cascading checks, etc.
    """

    def delete(self,request: Request, *args: List, **kwargs: Dict) :
        """
        DELETE handler that delegates logic to serializer.
        """
        return self.handle_request()
     









