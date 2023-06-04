from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from typing import Optional


class ButtonGenerator:
    """
    Generates a simple buttons' set.
    List to be passed as required argument. Then button creates in chat keyboard with name taken from list.
    Optional arguments:

        resize_keyboard = resizes the keyboard vertically for optimal fit;

        row_or_column = sets the arrangement of a buttons:

            * 'column' - buttons placed in a column format. Each row - one button;
            * 'row' - buttons placed in one row as default. For proper arrangement number of rows to be specified;
            * 'buttons_per_row' - Sets how many buttons nested in a row. Last element in dict - the lowest element.
    """
    def __init__(self, buttons_list: list,
                 resize_keyboard=True,
                 row_or_column='row',
                 buttons_per_row: Optional[int] = None):

        self.resize_keyboard = resize_keyboard
        self.buttons_list = buttons_list
        self.row_or_column = row_or_column
        self.num_rows = buttons_per_row

    def get_keyboard(self):
        keyboard = ReplyKeyboardMarkup(resize_keyboard=self.resize_keyboard)
        match self.row_or_column:
            case 'row':
                if self.num_rows is None:
                    for button_title in self.buttons_list:
                        keyboard.row(KeyboardButton(button_title))
                else:
                    current_row = []
                    for button_title in self.buttons_list:
                        current_row.append(KeyboardButton(button_title))
                        if len(current_row) == self.num_rows:
                            keyboard.row(*current_row)
                            current_row = []

                    if current_row:
                        keyboard.row(*current_row)

            case 'column':
                for button_title in self.buttons_list:
                    keyboard.add(KeyboardButton(button_title))
        return keyboard
