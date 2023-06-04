import asyncio
import re
import aiohttp
from aiogram import types

from bot_config import bot


class NewCustomer:

    """ Customer model. Represents a new user (customer) which sends as a POST request to backend API and creates
        a new customer account on a remote server"""

    def __init__(self, message: types.Message, email=None, password=None):
        self.email = email
        self.password = password
        self.user_id = message.from_user.id
        self.loop = asyncio.get_event_loop()

    async def get_additional_data(self) -> dict | None:

        """ Retrieves data from current user (if available) :
                * telegram_id;
                * username;
                * first_name;
                * last_name;
        """
        if self.user_id is not None:
            user = await bot.get_chat(self.user_id)
            user_data = {
                'telegram_id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
            return user_data
        else:
            return None

    async def create(self, endpoint, **kwargs):

        """ Sends POST request to API endpoint to create a new user. By default, only 'email' and 'password'
        sent (if provided) as minimal requirement to create a new user. Additional data may be provided as kwargs"""

        endpoint = endpoint

        if self.email and self.password:
            user = {
                "email": self.email,
                "password": self.password,
                **kwargs
            }

        else:
            user = {**kwargs}

        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, headers=headers, json=user) as response:
                if response.status == 201:
                    response_data = await response.json()
                    return response_data
                else:
                    return None
