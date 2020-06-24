from models import Admin, Driver


def check_driver(message):
    driver = Driver.query.filter(
        Driver.telegram_id == message.from_user.id).first()
    if driver:
        return True
    else:
        return False
