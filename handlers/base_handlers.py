from buttons.button_generation_class import ButtonGenerator
from aiogram import types, Dispatcher


async def start_command(message: types.Message):
    """
    Base set of buttons to handle initial user requests such as Register, Home and Help.
    """
    # Creating dict of buttons
    buttons_list = ["/home", "/help", "/registration", "/commands"]
    global main_buttons
    main_buttons = ButtonGenerator(buttons_list, buttons_per_row=2, row_or_column='row')

    await message.reply("Hi there, friend!\nWelcome to Project registration. Don't waste Your time and join us!",
                        reply_markup=main_buttons.get_keyboard())


async def help_command(message: types.Message):
    await message.reply("Customers support contact 24/7\n+380991234567")
    await message.answer('Hope I could help', reply_markup=main_buttons.get_keyboard())


async def list_commands(message: types.Message):
    await message.answer("List of commands available:\n\n"
                         "/start    - Begins a conversation to allow bot to reply\n"
                         "/home     - Your Hub to discover all functionalities\n"
                         "/help     - Relevant information to help with any issues\n"
                         "/commands - List of commands")


# Handlers registration section
def register_base_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start', 'home'])
    dp.register_message_handler(help_command, commands=['help'])
    dp.register_message_handler(list_commands, commands=['commands'])
