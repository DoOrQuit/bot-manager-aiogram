import asyncio
import re

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from utils import parse_date

from google_calendar.my_calendar import Calendar


calendar = Calendar("34d26d5fc687a92669649f6988b8ce852006f604a82e154ef055c991bbb24e49@group.calendar.google.com")


class EventBooking(StatesGroup):

    """ Booking a session to service master """

    date = State()
    time = State()


async def book_event(message: types.Message):
    await message.reply("Sure. Let me book a service session for You")
    await asyncio.sleep(1)
    await message.answer("NOTE:\nYou can STOP the process of registration. Just send me message 'stop' or 'cancel'")
    await asyncio.sleep(3)
    await EventBooking.date.set()
    await message.answer("Please, enter date You like to be booked for. "
                         "Date format includes 'month-day'. For example '06-25'.")


async def set_date(message: types.Message, state: FSMContext):
    date_pattern = r'^\d{2}-\d{2}$'

    async with state.proxy() as data:

        data['date'] = message.text
        # Validates a date provided
        if re.match(date_pattern, data["date"]):
            await EventBooking.next()
            await message.answer("Give me a second to check for available slots for this date")
            await asyncio.sleep(3)
            data['available_slots'] = calendar.get_event_hours(date=data['date'], available=True)
            await message.answer(f"The time slots available:\n {data['available_slots']}")
            await message.answer("Please, send me a time You like to book in format 24h format. For example: '14:00'")
        else:
            await message.answer("Date provided doesn't match with a pattern given."
                                 "Please provide date in numeric format of 'month-date'. "
                                 "For example '06-25'.")

            await EventBooking.date.set()


async def set_time(message: types.Message, state: FSMContext):

    time_pattern = r'^([01]\d|2[0-3]):[0-5]\d$'

    async with state.proxy() as data:
        data['time'] = message.text
        # Validates a date provided
        if re.match(time_pattern, data["time"]):
            if data['time'] in data['available_slots']:
                calendar.add_event("Customer", "Beauty tune up", date=data['date'], time=data['time'])
                await state.finish()
                await message.answer("Your session was booked successfully.")
                await asyncio.sleep(1)
                await message.answer(f"We are happy to meet You at {parse_date(data['date'])}, {data['time']}\n"
                                     f"Have a nice day!")
            else:
                await EventBooking.time.set()
                await message.answer("We are sorry but time is already occupied. Please, enter choose another time.")
        else:
            await EventBooking.time.set()
            await message.answer("Time provided doesn't match with a pattern given."
                                 "Please provide time in format like '14:00'")


def register_event_booking_handlers(dp: Dispatcher):
    dp.register_message_handler(book_event, commands=['book_event'], state=None)
    dp.register_message_handler(set_date, state=EventBooking.date)
    dp.register_message_handler(set_time, state=EventBooking.time)
