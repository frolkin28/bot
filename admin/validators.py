from models import session, Admin
from re import fullmatch, compile


def check_admin(message):
    admin = session.query(Admin).filter(
        Admin.telegram_id == message.from_user.id).first()
    if admin:
        return True
    else:
        return False


def check_phone(message):
    pattern = compile(r'\+380\d{9}')
    phone = pattern.fullmatch(message)
    if phone:
        return True
    else:
        return False
