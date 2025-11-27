from typing import Dict,Any,Optional
from django.db.models.query import QuerySet
from django.db.models import Model 
from rest_framework.response import Response
from rest_framework import status

class CoreGenericUtils:
    # -----------
    # ? Class Attributes
    # -----------

    toast_message_value : str = ""
    queryset : QuerySet 

    success_message : Dict[str,str] = {
        "POST" : "Successfully Created",
        "PUT" : "Successfully Updated",
        "DELETE" : "Successfully Deleted"
    }

    exception_message : str = "Internal Server Error"

    # -------------------------------
    # Request Utilities
    # -------------------------------

    def get_params(self):
        """
        Retrieves query parameters from the request object.

        Returns:
            Dict: A dictionary of query parameters.
        """
        try:
            params = dict(self.request.query_params)
        except :
            params = self.request.query_params
        
        return params
    
    def get_queryset(self) -> QuerySet[Model]:
        """
        Returns the active queryset (default: `.all()`).

        Returns:
            QuerySet[Model]: A Django queryset.
        """
        return self.queryset.all()

    def get_success_message(self) -> Optional[Any] :
        """
        Returns the default success message for the current HTTP method.

        Returns:
            Optional[str]: A success message or None if not mapped.
        """
        return self.success_message.get(self.request.method)


    def set_context_data(self) -> Dict :
        """
        Returns:
            Dict: Context containing the request, logger, and view kwargs.
        """
        context = {
            "request" : self.request,
            # "logger" : self.get_logger(),
            **self.kwargs
        }

        return context
    
    # ----------------------
    # ? Response Helpers
    # ----------------------

    def validation_response(self,validated_data : Dict) -> Response:
        """
        Returns a standardized validation error response.

        Args:
            validated_data (Dict): Must include 'error_message'.

        Returns:
            Response: DRF Response with error message and optional field errors.
        """
        return Response(
           {
                "message" : validated_data["error_message"],
                "field_errors" : validated_data.get("field_errors")
           },
           status=status.HTTP_400_BAD_REQUEST
        )
    
    def success_response(self,validated_data) -> Response:
        """
        Returns a standardized success response.

        Args:
            validated_data (Union[List, Dict]): Data payload to return.

        Returns:
            Response: DRF Response with a success message and results.
        """
        success_message : str = self.set_dynamic_toast_message(validated_data=validated_data)
        return Response(
            {
                "message" : success_message ,
                "results" : validated_data
            }
        )
    
    def custom_handle_exception(self , e : Exception) -> Response :
        """
        Handles exceptions consistently:
            - Returns a standardized error response

        Args:
            e (Exception): The raised exception.

        Returns:
            Response: DRF Response with error payload and HTTP 400.
        """ 
        return Response(
            {
                "message" : self.exception_message,
                "error" : str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
        )


    # -----------------------------
    # ? Toast Message Utilities
    # -----------------------------

    def get_toast_message_value(self) -> str :
        """
        Get the current toast message value.

        Returns:
            str: The toast message value.
        """

        return self.toast_message_value
    
    def set_toast_message_value(self,value : str) :
        """
        Set a custom toast message value.

        Args:
            value (str): Custom message string.
        """

        self.toast_message_value = value
    
    def set_dynamic_toast_message(self,validated_data : Dict) -> str :
        """
        Constructs and applies a dynamic toast message based on:
            - The current HTTP method (POST/PUT/DELETE)
            - The pre-set `toast_message_value` if available.

        Args:
            validated_data (Dict): The payload data.

        Returns:
            str: The final toast message used in the response.
        """

        success_message : str = self.get_success_message()

        payload : Dict[str,Any] = self.request.data

        if isinstance(success_message,str) :
            success_message : str = self.toast_message_value + "" + success_message
        
        success_message : str = success_message.strip().capitalize()

        return success_message 
    



