import requests
from config import B24_WH

class BaseHandlerClass:

    def __init__(self):
        self.B24_WH = B24_WH


class ProjectArchClass(BaseHandlerClass):
    def __init__(self):
        super().__init__()
        self.API_METHOD = "disk.folder.getchildren"
        self.URL = f"{self.B24_WH}{self.API_METHOD}"

        self.data = {"Тест проекный архив":(367992,
                                     ["Проект 1", "Файл 1.docx", "Файл 2.docx"],
                                     "https://fsk-r.bitrix24.ru/docs/path/%D0%A4%D0%A1%D0%9A%20%D0%A0%D0%B5%D0%B3%D0%B8%D0%BE%D0%BD/02.%20%D0%9F%D0%BE%D0%B4%D1%80%D0%B0%D0%B7%D0%B4%D0%B5%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F/02.08.%20%D0%94%D0%B5%D0%BF%D0%B0%D1%80%D1%82%D0%B0%D0%BC%D0%B5%D0%BD%D1%82%20%D1%80%D0%B0%D0%B7%D0%B2%D0%B8%D1%82%D0%B8%D1%8F/%D0%94%D0%BB%D1%8F%20%D1%82%D0%B5%D1%81%D1%82%D0%BE%D0%B2%20%D0%91%D0%B8%D1%82%D1%80%D0%B8%D1%8124/%D0%A2%D0%B5%D1%81%D1%82%20%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%BD%D1%8B%D0%B9%20%D0%B0%D1%80%D1%85%D0%B8%D0%B2/")}
        self.options = {"Подготовить отчет по папкам":self.get_disk_content_report(),
                        "Содержимое папок на данный момент": self.get_folder_content(367992)}

    def get_folder_content(self, folder_id):

        params = {
            'id': folder_id
        }

        response = requests.post(self.URL, json=params)

        if response.status_code == 200:
            data = response.json()
            folder_content = []
            if "error" in data:
                print(f"Ошибка: {data['error_description']}")
            else:
                for item in data['result']:
                    item_type = item.get("TYPE", "unknown")
                    item_name = item.get("NAME", "unnamed")
                    item_id = item.get("ID", "no_id")
                    folder_content.append(f"{item_name}")
                    # folder_content.append(f"{item_type.capitalize()}: {item_name} (ID: {item_id})")
            return "\n".join(folder_content)
        else:
            print(f"Ошибка при выполнении запроса: {response.status_code}")
            print(response.text)

    def get_disk_content_report(self):
        disk_content = []
        for folder in self.data:
            id, temple_folder, url = self.data[folder]
            disk_content.append(f"[{folder}]({url})")
            id, temple_folder, _ = self.data[folder]
            folder_content = self.get_folder_content(id)
            for temple_file in temple_folder:
                if temple_file in folder_content:
                    disk_content.append(f"{temple_file} ✅")
                else:
                    disk_content.append(f"{temple_file} ❌")
        return '\n'.join(disk_content)


class FaqClass(BaseHandlerClass):
    def __init__(self):
        super().__init__()
        self.data = {
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


class RequestClass(BaseHandlerClass):
    pass
