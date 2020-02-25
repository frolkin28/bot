from models import session, Admin


def check_admin(message):
    admin = session.query(Admin).filter(
        Admin.telegram_id == message.from_user.id).first()
    if admin:
        return True
    else:
        return False
