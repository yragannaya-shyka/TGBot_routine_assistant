
from fuzzywuzzy import process

faq_data = {
    "Выйти в отпуск":"Чтобы выйти в отпуск вам необходимо заполнить соответствующий документ",
    "Выйти на больничный":"Чтобы выйти на болничный вам необходимо иметь при себе больничный лист",
    "Вопрос 3":"Ответ 3",
    "Вопрос 4":"Ответ 4",
    "Вопрос 5":"Ответ 5",
    "Вопрос 6":"Ответ 6",
    "Вопрос 7":"Ответ 7",
    "Вопрос 8":"Ответ 8",
    "Вопрос 9":"Ответ 9",
    "Вопрос 10":"Ответ 10",
    "Вопрос 11":"Ответ 11",
    "Вопрос 12":"Ответ 12",
    "Вопрос 13":"Ответ 13",

}

QUESTION_PER_PAGE = 4

def get_questions_page(page):
    start = (page - 1) * QUESTION_PER_PAGE
    end = start + QUESTION_PER_PAGE
    return list(faq_data.keys())[start:end]

def find_closest_question(user_input):
    questions = list(faq_data.keys())
    closest_match = process.extractOne(user_input, questions)
    return closest_match[0] if closest_match[1] > 70 else None
