from telebot import types, TeleBot
import requests
from utils.utils import read_load_json_data, bitrix_id_by_name, bitrix_id_by_chat_id, escape_markdown
from utils.bitrix.bitrix import BitrixRequest
from utils.classes import ProjectArchClass, FaqClass
import urllib.parse
from messages import  welcome_message, info_message, help_message, rights_list_message, test_funcs_message
from keyboards.keyboards import create_keyboard, get_cancel_keyboard
from decorators import handle_errors , handle_action_cancel
from config import B24_WH, B24_ADMIN_ID
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

faq = FaqClass()
pa = ProjectArchClass()

state = {
    "status": "null"
}

def new_funcs_handler(message: types.Message, bot: TeleBot):
    keyboard = create_keyboard([types.KeyboardButton("FAQ"),
                                types.KeyboardButton("Проектный архив")])
    bot.send_message(message.chat.id, test_funcs_message, parse_mode="Markdown", reply_markup=keyboard)


def project_arch_handle(message: types.Message, bot: TeleBot):
    state["status"] = "project_arch"
    print(state["status"])
    keyboard = create_keyboard([option for option in pa.options])
    bot.send_message(message.chat.id, "Выберите интересующий вас функионал", parse_mode="Markdown", reply_markup=keyboard)


def hello_handler(message: types.Message, bot: TeleBot):
    bot.send_message(message.chat.id, "Hello test")


def start_handle(message: types.Message, bot: TeleBot):
    keyboard = create_keyboard([types.KeyboardButton("Создать запрос"),
                                types.KeyboardButton("FAQ"),
                                types.KeyboardButton("Проектный архив")])
    bot.send_message(message.chat.id, welcome_message, parse_mode="Markdown", reply_markup=keyboard)


def help_handle(message: types.Message, bot: TeleBot):
    keyboard = create_keyboard([types.KeyboardButton("Задать вопрос разработчику бота")])
    bot.send_message(message.chat.id, help_message, reply_markup=keyboard)


def info_handle(message: types.Message, bot: TeleBot):
    bot.send_message(message.chat.id, info_message)


def request_handle(message: types.Message, bot: TeleBot):
    state["status"] = "request"
    print(state["status"])
    keyboard = create_keyboard([types.KeyboardButton("Подключение нового сотрудника"),
                                types.KeyboardButton("Предоставление прав доступа"),
                                types.KeyboardButton("Отправить уведомление")])
    bot.send_message(message.chat.id, 'Выберите интересующий вас запрос из меню ниже.', reply_markup=keyboard)

def faq_handle(message: types.Message, bot: TeleBot):
    categories = faq.categories
    keyboard = create_keyboard([c for c in categories])
    state["status"] = "faq"
    print(state["status"])
    bot.send_message(message.chat.id, "Выберите интересующий вас вопрос", reply_markup=keyboard)


def handle_request(message: types.Message, bot:TeleBot):
    requests = {
        "Подключение нового сотрудника": (invite_new_user_step_name, "Введите ФИО нового сотрудника"),
        "Предоставление прав доступа": (procces_access_rights_step_name, "Введите ФИО сотрудника, кому необходимо предоставить права доступа."),
        "Отправить уведомление": (procces_notify_step, "Введите текст уведомления"),
    }

    if message.text in requests:
        handler, prompt = requests[message.text]
        msg = bot.send_message(message.chat.id, prompt, reply_markup=get_cancel_keyboard())
        bot.register_next_step_handler(msg, handler, bot=bot)
    else:
        bot.reply_to(message, f"Команды '{message.text}' не существует.")


@handle_errors
@handle_action_cancel
def handle_faq(message: types.Message, bot: TeleBot):
    questions  = faq.categories[message.text]
    keyboard = create_keyboard([q for q in questions])
    bot.send_message(message.chat.id, "Выберите вопрос", parse_mode="Markdown", disable_web_page_preview=True, reply_markup=keyboard)
    # closest_question = find_closest_question(message.text)
    # if closest_question:
    #     bot.send_message(message.chat.id, faq_data[closest_question])
    # else:
    #     bot.send_message(message.chat.id, "Извините, я не нашел ответа на ваш вопрос.")

@handle_errors
@handle_action_cancel
def handle_faq_question(message: types.Message, bot: TeleBot):
    for couple in faq.categories.values():
        if message.text in couple:
            answer = couple[message.text]
            bot.send_message(message.chat.id, answer, parse_mode="Markdown", disable_web_page_preview=True)

@handle_errors
@handle_action_cancel
def handle_project_arch(message: types.Message, bot: TeleBot):
    # text = pa.options[message.text]
    keyboard = pa.get_project_keyboard()
    text = "Выберите проект"
    bot.send_message(message.chat.id, text, reply_markup=keyboard, parse_mode="HTML", disable_web_page_preview=True)


def handle_project_arch_content(message: types.Message, bot: TeleBot):
    text = escape_markdown(pa.get_project_folders_content(message.text))
    bot.send_message(message.chat.id, text=text, parse_mode="Markdown", disable_web_page_preview=True)

def procces_notify_step(message: types.Message, bot: TeleBot):

    try:
        description = message.text
        requests.get(f"{B24_WH}im.notify.personal.add.json?USER_ID={B24_ADMIN_ID}&MESSAGE={description}")
        bot.reply_to(message, f"Уведомление '{description}' отправлено!")
    except Exception as e:
        bot.reply_to(message, "Что-то пошло не так!")


#access_rights procces steps
@handle_errors
@handle_action_cancel
def procces_access_rights_step_name(message: types.Message, bot: TeleBot):
    br = BitrixRequest()

    initiator_tg_id = message.chat.id
    initiator = bitrix_id_by_chat_id(initiator_tg_id)
    br.params["initiator"].value = initiator
    br.params["initiator_tg_id"].value = initiator_tg_id
    name = message.text
    br.params["acces_rights_user"].value = bitrix_id_by_name("users.json", name)
    bot.send_message(message.chat.id, rights_list_message, reply_markup=get_cancel_keyboard())
    bot.register_next_step_handler(message, procces_access_rights_step_rights, bot=bot, br=br)


@handle_errors
@handle_action_cancel
def procces_access_rights_step_rights(message: types.Message, bot: TeleBot, br: BitrixRequest):
    rights = message.text
    br.params["acces_rights_type"].value = rights
    bot.send_message(message.chat.id, "Вставьте ссылку на объект (папка/файл) предоставления прав доступа.", reply_markup=get_cancel_keyboard())
    bot.register_next_step_handler(message, procces_access_rights_step_link, bot=bot, br=br)


@handle_errors
@handle_action_cancel
def procces_access_rights_step_link(message: types.Message, bot: TeleBot, br: BitrixRequest):
    link = message.text
    encoded_description = urllib.parse.unquote(link)
    coded_url = urllib.parse.quote(encoded_description,safe=":/")
    double_coded_url = urllib.parse.quote(coded_url)
    br.params["acces_rights_object_link"].value = double_coded_url
    record_data = br.get_data_for_record()
    request_id = read_load_json_data("users_requests.json", record_data)
    br.params["request_id"].value = request_id
    br.params["title"].value = f"ТГ запрос №{request_id}"
    requests.get(br.create_bitrix_smart_process_element("access_rights"))
    bot.send_message(message.chat.id, f"Ваш запрос №{br.params['request_id'].value} принят в работу. Ожидайте уведомление о выполнении запроса.")



#invite_new_user steps
@handle_errors
@handle_action_cancel
def invite_new_user_step_name(message: types.Message, bot: TeleBot):
    br = BitrixRequest()

    initiator_tg_id = message.chat.id
    initiator = bitrix_id_by_chat_id(initiator_tg_id)
    br.params["initiator"].value = initiator
    br.params["initiator_tg_id"].value = initiator_tg_id


    name = message.text
    br.params["new_user_name"].value = name

    bot.send_message(message.chat.id, "Введите должность нового сотрудника", reply_markup=get_cancel_keyboard())
    bot.register_next_step_handler(message, invite_new_user_step_position, bot=bot, br=br)


@handle_errors
@handle_action_cancel
def invite_new_user_step_position(message: types.Message, bot: TeleBot, br: BitrixRequest):
    position = message.text
    br.params["new_user_position"].value = position
    msg = bot.send_message(message.chat.id, "Введите подразделение нового сотрудника", reply_markup=get_cancel_keyboard())
    bot.register_next_step_handler(msg, invite_new_user_step_division, bot=bot, br=br)



@handle_errors
@handle_action_cancel
def invite_new_user_step_division(message: types.Message, bot: TeleBot, br: BitrixRequest):
    division = message.text
    br.params["new_user_division"].value = division
    msg = bot.send_message(message.chat.id, "Введите ФИО руководителя нового сотрудника", reply_markup=get_cancel_keyboard())
    bot.register_next_step_handler(msg, invite_new_user_step_supervisor, bot=bot, br=br)


@handle_errors
@handle_action_cancel
def invite_new_user_step_supervisor(message: types.Message, bot: TeleBot, br: BitrixRequest):

    supervsor = message.text
    br.params["new_user_supervisor"].value = bitrix_id_by_name("users.json", supervsor)
    record_data = br.get_data_for_record()
    request_id = read_load_json_data("users_requests.json", record_data)
    br.params["request_id"].value = request_id
    br.params["title"].value = f"ТГ запрос №{request_id} - {br.categoryes['new_user'].name}"
    requests.get(br.create_bitrix_smart_process_element("new_user"))
    bot.reply_to(message, f"Ваш запрос №{request_id} принят в работу. Ожидайте уведомление о выполнении запроса.")



HANDLERS = [
    (hello_handler, lambda message: message.text == "Hello"),
    (request_handle, lambda message: message.text == "Создать запрос"),
    (project_arch_handle, lambda message: message.text == "Проектный архив" or message.text.startswith("/prach")),
    (faq_handle, lambda message: message.text == "FAQ" or message.text.startswith("/faq")),
    (request_handle, lambda message: message.text.startswith("/request")),
    (start_handle, lambda message: message.text.startswith("/start")),
    (help_handle, lambda message: message.text.startswith("/help")),
    (info_handle, lambda message: message.text.startswith("/info")),
    (new_funcs_handler, lambda message: message.text.startswith("/tests")),
    (handle_faq_question, lambda message: state["status"] == "faq" and message.text in faq.get_questions()),
    (handle_faq, lambda message: state["status"] == "faq"),
    (handle_project_arch_content, lambda message: state["status"] == "project_arch" and message.text in pa.get_projects_list()),
    (handle_project_arch, lambda message: state["status"] == "project_arch"),
    (handle_request, lambda message: state["status"] == "request")


]

def register_handler(bot: TeleBot):
    for handle, conditition in HANDLERS:
        bot.register_message_handler(handle, func=conditition, pass_bot=True)
