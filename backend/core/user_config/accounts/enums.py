from core_utils.utils.enums import EnumChoices


class UserRoleEnum(EnumChoices):
    ADMIN = "ADMIN"
    TENANT = "TENANT"
    MANAGER = "MANAGER"
