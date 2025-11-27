from core.settings import CUSTOM_APPS
from typing import List

class GetCustomApps:
    custom_apps : List = CUSTOM_APPS

    def refactor_apps(self,app_name : str, app : List):
        """
        Extracts and appends the final app name from a potentially nested app structure.

        If the app name is a sub-app (e.g., "user_config.user_auth"),
        it extracts only the final part ("user_auth") and appends it to the list.
        Otherwise, it appends the app name as is.

        Args:
            app_names (str): The app name, which may be a sub-app in a dotted path.
            app (list): The list to which the extracted app name is appended.
        """
        if "." in app_name :
            app_label = app_name.split(".")[-1]
            app.append(app_label)
        else:
            app.append(app_name)

    def refactor_command(self,custom_apps : List[str]):
        """
        Processes a list of custom apps and extracts only the final app names.

        This ensures that `makemigrations` is run only for the relevant Django apps.

        Args:
            custom_apps (list): List of full app names (may include sub-apps).

        Returns:
            list: A list of extracted app names.
        """
        app : List = []
        for app_name in custom_apps :
            self.refactor_apps(app_name=app_name,app=app)
        return app
            


