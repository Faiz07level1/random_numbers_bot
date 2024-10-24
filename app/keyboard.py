from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButtonPollType, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from app.database.models import Game_len, Story
keyboard_1 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Давай сыграем",)]], resize_keyboard=True, one_time_keyboard=True)

# buttons = [KeyboardButton(text=f'Кнопка {i}') for i in range(1, 10)]
    

# # Составляем список списков для будущей клавиатуры
# keyboard: list[list[KeyboardButton]] = [
#     [buttons[0]],
#     buttons[1:3],
#     buttons[3:6],
#     buttons[6:8],
#     [buttons[8]]
# ]

button: list[KeyboardButton] = [
    KeyboardButton(text=f'{i}') for i in range(1, 101)]

# # Генерируем список с кнопками
# buttons_2: list[KeyboardButton] = [
#     KeyboardButton(text=f'{i}') for i in range(31, 61)]
# buttons=[]

# keyboard = []
# for i in range(1, 101):
#     buttons.append(KeyboardButton(text=str(i)))
#     if not i % 12:
#         keyboard.append(buttons)
#         buttons = []
#     if i == 100:
#         keyboard.append(buttons)
#         buttons = []
my_keyboard = ReplyKeyboardBuilder()

# my_keyboard.row(*button)

my_keyboard.add(*[KeyboardButton(text=F"{i}") for i in range(1, 101)])
# my_keyboard.adjust(1, 3, 10, repeat=True)


kb_builder = ReplyKeyboardBuilder()

# Создаем кнопки
contact_btn = KeyboardButton(
    text='Отправить телефон',
    request_contact=True
)
geo_btn = KeyboardButton(
    text='Отправить геолокацию',
    request_location=True
)
poll_btn = KeyboardButton(
    text='Создать опрос/викторину',
    request_poll=KeyboardButtonPollType()
)

# Добавляем кнопки в билдер
kb_builder.row(contact_btn, geo_btn, poll_btn, width=1)

# Создаем объект клавиатуры
keyboard: ReplyKeyboardMarkup = kb_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=True
)
exchange_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="обмен на кристалы 💎", callback_data="exchange_crystals")],
                                                           [InlineKeyboardButton(text="обмен на кубки 🏆", callback_data="exchange_wins")],
                                                             [InlineKeyboardButton(text="отмена", callback_data="cancel")]])

async def story_keyboard(products, games) -> InlineKeyboardMarkup:
    arr = []
    kb_builder = InlineKeyboardBuilder()
    products_arr = list()
    print(games.all_stickers.find(",") > -1)
    for p in products:
        if not games.all_stickers or games.all_stickers.find(",") ==-1:
            if p.sticker_name != games.all_stickers:
                print(p.sticker_name)
                products_arr.append(p)
        if games.all_stickers.find(",") > -1:
            print(games.all_stickers, p.sticker_name)    
            if (p.sticker_name not in games.all_stickers.split(",")):
                products_arr.append(p)
    print("|")
    for p in products_arr:
        arr.append(InlineKeyboardButton(text=F"{p.sticker} - {p.sticker_price}🤑", callback_data=F"product_{p.sticker_name}"))
    kb_builder.row(*arr, width=2)
    return kb_builder.as_markup()


async def user_sticker(products, all_stickers):
    arr = []
    kb_builder = InlineKeyboardBuilder()
    
    products_arr = list()
    for p in products:
          
        if (p.sticker_name in all_stickers.split(",")):
                products_arr.append(p)
    for p in products_arr:
        arr.append(InlineKeyboardButton(text=F"{p.sticker}", callback_data=F"user_sticker_{p.sticker_name}"))
    kb_builder.row(*arr, width=2)
    return kb_builder.as_markup()



rate_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="ставка", callback_data="rate"),
                                                        InlineKeyboardButton(text="отмена", callback_data="cancel")]])

exchange_keyboard_ok = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="обмен", callback_data="exchange_ok"),
                                                        InlineKeyboardButton(text="отмена", callback_data="cancel")]])

my_inline_button = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🗿", callback_data="rock"),
                                                          InlineKeyboardButton(text="✂️", callback_data="scissors"),
                                                          InlineKeyboardButton(text="📃", callback_data="paper")]])
# # Составляем список списков для будущей клавиатуры
# keyboard: list[list[KeyboardButton]] = [buttons_1,
#                                         buttons_2]

# # Создаем объект клавиатуры, добавляя в него список списков с кнопками
# my_keyboard = ReplyKeyboardMarkup(
#     keyboard=keyboard,
#     resize_keyboard=True
# )


# url_button_1 = InlineKeyboardButton(
#     text='Курс "Телеграм-боты на Python и AIOgram"',
#     url='https://stepik.org/120924'
# )
# url_button_2 = InlineKeyboardButton(
#     text='Документация Telegram Bot API',
#     url='https://core.telegram.org/bots/api'
# )
# # url_button_3 = InlineKeyboardButton(
# #     text='Ссылка на Максима',
# #     url='tg://user?id=6119385873'
# # )

# url_button_3 = InlineKeyboardButton(
#     text="Ссылка на канал",
#     url="tg://resolve?domain=umnie_roditeli"
# )

# Создаем объект инлайн-клавиатуры
# keyboard_url = InlineKeyboardMarkup(
#     inline_keyboard=[[url_button_1],
#                      [url_button_2],
#                      [url_button_3]]
# )

