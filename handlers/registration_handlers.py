import asyncio
import re

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


from utils import NewCustomer


REGISTRATION_API_ENDPOINT = "http://127.0.0.1:8000/api/v1/users/"


class UserRegistration(StatesGroup):
    email = State()
    password1 = State()
    password2 = State()


async def register(message: types.Message):
    if message.chat.type == 'private':
        await message.reply("It's gonna be awesome!\n\nBut I definitely need some information from You for "
                            "registration purpose.\nSo let's get to know You better!")
        await asyncio.sleep(1)
        await message.answer("NOTE:\nYou can STOP the process of registration. Just send me message 'stop' or 'cancel'")
        await asyncio.sleep(3)
        await UserRegistration.email.set()
        await message.answer("Tell me an EMAIL You want to use for signing in on a web service?\n\n"
                             "Requirements:\n "
                             "- Any combination of characters, including special characters;\n"
                             "- Must contain at least one '@' symbol;\n"
                             "- It should has a dot (.) symbol followed by a combination of letters or digits"
                             " to complete the address.")
    else:
        await message.answer("Looks like chat is public and Your personal data may be disclosed")


async def cancel_registration(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()

    await message.reply('Registration cancelled. You can start again any time.')


async def get_email(message: types.Message, state: FSMContext):

    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    async with state.proxy() as data:
        data['email'] = message.text
        # Validates an email as per given pattern
        if re.match(email_pattern, data["email"]):
            await UserRegistration.next()
            await message.answer("Cool! Now I can mail You. Don't worry. Just joking!)")
            await asyncio.sleep(0.5)
            await message.answer("Now set a PASSWORD You would like to use on a website. "
                                 "But make sure it is safe enough!\n\n"
                                 "Requirements:\n"
                                 "- Minimum length of 8 characters;\n"
                                 "- At least one digit;\n"
                                 "- Any combination of uppercase, lowercase, and special characters")
        else:
            await message.answer("Email doesn't not match with a pattern given. Please try again.")
            await UserRegistration.email.set()


async def get_pass1(message: types.Message, state: FSMContext):

    password_patter = r'^(?=.*\d)(?=.*[a-zA-Z]).{8,}$'

    async with state.proxy() as data:
        data['password1'] = message.text
        # Validates an email as per given pattern
        if re.match(password_patter, data["password1"]):
            await UserRegistration.next()
            await message.answer("Almost there! Just need to insure You remember which password You set.")
            await asyncio.sleep(0.5)
            await message.answer("Now, please, re-enter Your PASSWORD AGAIN")
            await UserRegistration.password2.set()
        else:
            await message.answer("Password doesn't not match with a pattern given. Please try again.")
            await UserRegistration.password1.set()


async def get_pass2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password2'] = message.text

        if data['password1'] != data['password2']:

            await message.answer("Passwords do not match. Please try again.")
            await UserRegistration.password1.set()

        else:

            async with state.proxy() as clean_data:
                # New customer object creates
                new_user = NewCustomer(message, email=clean_data["email"], password=clean_data["password1"])
                if new_user is not None:
                    # Sends a POST request to server API to create new user (customer) object
                    await new_user.create(REGISTRATION_API_ENDPOINT)
                    await message.answer("User created successfully!")
                else:
                    await message.answer("Failed to create user. Please, contact technical support for help")


def register_signup_handlers(dp: Dispatcher):
    dp.register_message_handler(register, commands=['registration'], state=None)
    dp.register_message_handler(cancel_registration, state='*', commands=['cancel', 'stop'])
    dp.register_message_handler(cancel_registration, lambda message: message.text.lower() == 'cancel' or
                                                                     message.text.lower() == 'stop', state='*')
    dp.register_message_handler(get_email, state=UserRegistration.email)
    dp.register_message_handler(get_pass1, state=UserRegistration.password1)
    dp.register_message_handler(get_pass2, state=UserRegistration.password2)

