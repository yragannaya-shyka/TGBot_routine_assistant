class ActionCanceled(Exception):
    pass

def handle_errors(func):
    def wrapper(message, bot, *args, **kwargs):
        try:
            return func(message, bot, *args, **kwargs)
        except ActionCanceled as e:
            bot.send_message(message.chat.id, f"{str(e)}")
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")
    return wrapper

def handle_action_cancel(func):
    def wrapper(message, bot, *args, **kwargs):
        if message.text in ("/cancel", "Отмена"):
            raise ActionCanceled("Действие отменено")
        return func(message, bot, *args, **kwargs)
    return wrapper
