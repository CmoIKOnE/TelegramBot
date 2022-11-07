import telebot
import config
import random
import string
import re
 
from telebot import types
'''from sqlighter import *'''

bot = telebot.TeleBot(config.TOKEN)

print("Бот Telegram врублен. by cmkN")

@bot.message_handler(commands=["start"])
def welcome(message):
    #sti = open('stikers/hello.webp', 'rb')
    #bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.from_user.id, "Вас приветствует бот регистрации проекта mcspace.me.")

@bot.message_handler(commands=["connect"])
def connectAccount(message):
	tele_id = message.from_user.id
	if check_tele_id(tele_id):
		bot.send_message(message.from_user.id, "Введите Ваш никнейм на проекте")
		bot.register_next_step_handler(message, checkEmailUser)
	else:
		bot.send_message(message.from_user.id, "К Вашему Telegram-аккаунту уже привязан аккаунт")
login = ''
password = ''
tele_id = ''
login_reg = ''
@bot.message_handler(content_types=["text"])
def start(message):
	tele_id = message.from_user.id
	login_reg = get_login(tele_id)
	if check_tele_id(tele_id):
		if message.text == '/reg':
			bot.send_message(message.from_user.id, "Введите желаемый никнейм.")
			bot.register_next_step_handler(message, get_password)
		else:
			bot.send_message(message.from_user.id, 'Напишите /reg.')
	else: 
		if message.text == '/changepass':
			bot.send_message(message.from_user.id, "Введите желаемый новый пароль.")
			bot.register_next_step_handler(message, get_reset_password)
		else:
			bot.send_message(message.from_user.id, 'Вы зарегистрированы на нашем проекте. Ваш игровой ник - '+login_reg+'. Если хотите сменить пароль, напишите команду - /changepass')

def checkEmailUser(message):
	global login
	login = message.text
	if not check_login(login):
		if not hasAccountTelegram(login):
			bot.send_message(message.from_user.id, 'Введите Ваш текущий email-адрес')
			bot.register_next_step_handler(message, checkPasswordUser)
		else:
			bot.send_message(message.from_user.id, 'Этот аккаунт уже привязан к другому Telegram-аккаунту')
	else:
		bot.send_message(message.from_user.id, 'Аккаунта ' + login + ' не существует')

def checkPasswordUser(message):
	global email
	email = message.text
	if checkEmail(email):
		bot.send_message(message.from_user.id, 'Введите Ваш текущий пароль для подтверждения')
		bot.register_next_step_handler(message, endConnection)
	else:
		bot.send_message(message.from_user.id, 'Аккаунта с таким email-адресом не обнаружено')

def endConnection(message):
	global password
	password = message.text
	if checkUserByData(login, email, password):
		bot.send_message(message.from_user.id, 'Привязываем этот телеграм-аккаунт к аккаунту ' + login)
		if changeAccountType(login, message.from_user.id):
			bot.send_message(message.from_user.id, 'Поздравляем! Вы привязали этот телеграм к аккаунту ' + login)
		else: bot.send_message(message.from_user.id, 'Произошла ошибка со стороны сервера. Сообщите администрации проекта')
	else: bot.send_message(message.from_user.id, 'Проверьте корректность введенных данных')

def get_password(message):
	global login
	login = message.text
	if check_login(login):
		if re.match(r"[a-zA-Z0-9_]{4,16}", login):
			bot.send_message(message.from_user.id, 'Введите желаемый пароль.')
			bot.register_next_step_handler(message, end_reg)
		else:
			bot.send_message(message.from_user.id, 'Никнейм содержит недопустимые символы. Никнейм должен содержать лишь латинские буквы и цифры, и быть длиной от 4 до 16 символов. Используйте заново - /reg.')
	else:
		bot.send_message(message.from_user.id, 'Никнейм уже используется. Используйте заново - /reg.')

def get_reset_password(message):
	global password_new
	password_new = message.text
	tele_id = message.from_user.id
	if re.match(r'[A-Za-z0-9@#$%^&+=]{6,48}', password_new):
		reset_password(password_new, tele_id)
		bot.send_message(message.from_user.id, 'Вы изменили пароль на '+password_new)
	else:
		bot.send_message(message.from_user.id, 'Пароль содержит недопустимые символы. Пароль должен содержать лишь латинский буквы и цифры, и быть длиной от 6 до 48 символов. Используйте заново - /changepass.')

def end_reg(message):
	global password
	password = message.text
	if re.match(r'[A-Za-z0-9@#$%^&+=]{6,48}', password):
		keyboard = types.InlineKeyboardMarkup()
		key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
		key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
		keyboard.add(key_yes)
		keyboard.add(key_no)
		question = 'Ваш игровой ник: '+login+ ' | Ваш пароль: '+password+' | Верно?'
		bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
	else:
		bot.send_message(message.from_user.id, 'Пароль содержит недопустимые символы. Пароль должен содержать лишь латинский буквы и цифры, и быть длиной от 6 до 48 символов. Используйте заново - /reg.')

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    a = telebot.types.ReplyKeyboardRemove()
    keyboard = None
    tele_id = call.from_user.id
    if check_login(login) == False or check_tele_id(tele_id) == False:
    	bot.send_message(call.message.chat.id, 'Регистрация с данного Telegram аккаунта уже была произведена. Ваш игровой ник - '+login, reply_markup=a)
    else:
	    if call.data == "yes": 
	        if add_account(login, password, tele_id) or check_tele_id(tele_id) == True:
	        	bot.send_message(call.message.chat.id, 'Теперь Вы зарегистрированы на проекте MCSpace с помощью Телеграм.', reply_markup=a)
	        else:
	        	bot.send_message(call.message.chat.id, 'Произошла ошибка со стороны сервера.', reply_markup=a)
	    elif call.data == "no":
	        bot.send_message(call.message.chat.id, 'Используйте заново - /reg.', reply_markup=a)
		
# RUN
bot.polling(none_stop=True)