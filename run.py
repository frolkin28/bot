from application import bot
from driver.handlers import *
from admin.driver_handlers import *
from admin.admin_handlers import *
from customer.handlers import *


if __name__ == '__main__':
    bot.enable_save_next_step_handlers(delay=2)
    bot.load_next_step_handlers()
    bot.polling(none_stop=True)
