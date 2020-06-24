import re

from application.services import AdminService


def check_admin(message):
    service = AdminService()
    admin = service.get_by_tg_id(message.from_user.id)
    if admin:
        return True
    else:
        return False


def check_phone(message):
    pattern = re.compile(r'\+380\d{9}')
    phone = pattern.fullmatch(message)
    if phone:
        return True
    else:
        return False
