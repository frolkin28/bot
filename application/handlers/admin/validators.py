'''Local validators for handlers'''

import re

from application.services import AdminService
from application import dp


async def check_admin(message):
    service = AdminService()
    admin = service.get_by_tg_id(message.from_user.id)
    if admin:
        return True
    else:
        return False
