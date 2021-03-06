'''Local validators for handlers'''

from application.services import DriverService


async def check_driver(message):
    driver = DriverService().get_by_tg_id(message.from_user.id)
    if driver:
        return True
    else:
        return False
