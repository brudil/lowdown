from rolepermissions.roles import AbstractUserRole


class Editor(AbstractUserRole):
    available_permissions = {
        'can_finalize_content': True,
        'can_publish': True,
        'can_save_any': True,
    }


class Writer(AbstractUserRole):
    available_permissions = {
        'can_save_watching': True,
    }
