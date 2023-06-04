from aiogram.utils import executor

from bot_config import dp
from handlers import base_handlers, registration_handlers


base_handlers.register_base_handlers(dp)
registration_handlers.register_signup_handlers(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
