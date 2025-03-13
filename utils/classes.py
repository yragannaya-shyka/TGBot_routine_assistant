import requests
from config import B24_WH
from dataclasses import dataclass
from keyboards.keyboards import create_keyboard

@dataclass
class ArchFolder:
    name: str
    id: int
    url: str


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

        # self.folders = {"Тест проекный архив": 367992,
        #                 "Для тестов": 220014}

        self.folders = {"Горшкова 24":(ArchFolder(name="ППТ", id=183132,
                                                  url="https://fsk-r.bitrix24.ru/bitrix/tools/disk/focus.php?folderId=183132&action=openFolderList&ncc=1"),
                                       ArchFolder(name="ГПЗУ", id=37719,
                                                  url="https://fsk-r.bitrix24.ru/bitrix/tools/disk/focus.php?folderId=37719&action=openFolderList&ncc=1"),
                                       ArchFolder(name="РНС", id=37877,
                                                  url="https://fsk-r.bitrix24.ru/bitrix/tools/disk/focus.php?folderId=37877&action=openFolderList&ncc=1"),
                                       ArchFolder(name="Экспертиза",
                                                  id=37749, url="https://fsk-r.bitrix24.ru/bitrix/tools/disk/focus.php?folderId=37749&action=openFolderList&ncc=1"),
                                       ArchFolder(name="РВЭ", id=37881,
                                                  url="https://fsk-r.bitrix24.ru/bitrix/tools/disk/focus.php?folderId=37881&action=openFolderList&ncc=1")),
                        "Крылово 10":(ArchFolder(name="ППТ", id=183128,
                                                 url="https://fsk-r.bitrix24.ru/bitrix/tools/disk/focus.php?folderId=183128&action=openFolderList&ncc=1"),
                                      ArchFolder(name="ГПЗУ", id=38073,
                                                 url="https://fsk-r.bitrix24.ru/bitrix/tools/disk/focus.php?folderId=38073&action=openFolderList&ncc=1"),
                                      ArchFolder(name="РНС", id=38231,
                                                 url="https://fsk-r.bitrix24.ru/bitrix/tools/disk/focus.php?folderId=38231&action=openFolderList&ncc=1"),
                                      ArchFolder(name="Экспертиза", id=38103,
                                                 url="https://fsk-r.bitrix24.ru/bitrix/tools/disk/focus.php?folderId=38103&action=openFolderList&ncc=1"),
                                      ArchFolder(name="РВЭ", id=38235,
                                                 url="https://fsk-r.bitrix24.ru/bitrix/tools/disk/focus.php?folderId=38235&action=openFolderList&ncc=1"))
                        }

# "Подготовить отчет по папкам":self.get_disk_content_report(),
        self.options = {
                        "Содержимое папок на данный момент": self.get_folders_content(self.folders)}

    def get_folder_content_by_id(self, folder_id):

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
                    item_name = item.get("NAME", "unnamed")
                    folder_content.append(f"{item_name}")
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
            folder_content = self.get_folder_content_by_id(id)
            for temple_file in temple_folder:
                if temple_file in folder_content:
                    disk_content.append(f"{temple_file} ✅")
                else:
                    disk_content.append(f"{temple_file} ❌")
        return '\n'.join(disk_content)

    def get_folders_content(self, folders: dict):
        folders_content = []
        for name, content in folders.items():
            folders_content.append(f"Проект: {name}")
            for folder in content:
                folders_content.append(f"Папка: {folder.name}")
                folders_content.append(self.get_folder_content_by_id(folder.id))
                folders_content.append(" ")
        return '\n'.join(folders_content)


    def get_project_folders_content(self, project: str):
        folders_content = []
        for folder in self.folders[project]:
            folders_content.append(f"Папка: [{folder.name}]({folder.url})")
            folders_content.append(self.get_folder_content_by_id(folder.id))
            folders_content.append(" ")
        return '\n'.join(folders_content)


    def get_projects_list(self):
        return list(self.folders.keys())

    def get_project_keyboard(self):
        return create_keyboard(i for i in self.folders)

class FaqClass(BaseHandlerClass):
    def __init__(self):
        super().__init__()
        self.categories = {
            "Отпуск": {
                "Как подать заявление на отпуск?":"Подайте заявку на ресурсе HR-Link (https://kedo.fsk.ru/ )",
                "Как перенести отпуск?":"Подайте заявку на ресурсе HR-Link (https://kedo.fsk.ru/ ).\nОзнакомьтесь с инструкцией https://fsk-r.bitrix24.ru/knowledge/baza_znaniy/pamyatkasotrudnikupopodgotovkeuotpusku/",
                },
            "Мои документы": {
                "Нужна справка 2НДФЛ":"Подайте заявку на ресурсе HR-Link (https://kedo.fsk.ru/ )",
                "Нужна копия трудовой книжки":"Подайте заявку на ресурсе HR-Link (https://kedo.fsk.ru/ )\nЗаявление на выдачу копии трудовой книжки"
                },
            "Заработная плата": {
                "Какого числа выплачивается зарплата?":"Заработная плата в компании выплачивается 2 раза в месяц: аванс 23 числа и заработная плата 07 числа каждого месяца (если эти даты выпадают на выходные дни, то выплата происходит в ближайший предшествующий рабочий день)"
                },
            "ДМС": {
                "Как получить ДМС":"Подключение к ДМС происходит в течение 10 рабочих дней с момента завершения испытательного срока",
                "Можно ли подключить родственника к своему ДМС":"Можно заключить отдельный договор и оформить ДМС для родственника в страховой компании при условии:\nоформление возможно в течение 2 месяцев с момента завершения испытательного срока;\nДМС для подключаемого родственника Вы оплачиваете самостоятельно;\nк близким родственникам страховая компания относит супругов и детей",
                "У меня другой вопрос по ДМС":"Обратитесь к Руководителю управления персонала Анохиной А.О. (AnohinaAO@fsk.ru )"
                },
            "Удалённый доступ": {
                "Нет подключения к удалённому рабочему столу": "Обратитесь к Руководителю отдела ИТ-инфраструктуры Гасилову Д.С. (GasilovDS@fsk.ru )",
                "Нужно подключить доступ к удалёнке на личном компьютере": "Обратитесь к Руководителю отдела ИТ-инфраструктуры Гасилову Д.С. (GasilovDS@fsk.ru )"
                },
            "Нет доступа": {
                "Нет доступа к ПО":"Обратитесь в техническую поддержку (hd@fsk.ru )",
                "Нет доступа к функционалу БитФинанс":"Обратитесь в техническую поддержку (hd@fsk.ru )",
                "Нет доступа к Академии ФСК":"Обратитесь в техническую поддержку (hd@fsk.ru )",
                "Нет доступа к функционалу ИСУП":"Обратитесь в техническую поддержку (hd@fsk.ru )",
                "Нет доступа к функционалу Битрикс24":"Обратитесь к Ведущему специалисту по автоматизации бизнес-процессов Шинкаренко С.Е (ShinkarenkoSE@fsk.ru )",
                },
            "Командировки": {"Как оформить командировку?":"Ознакомьтесь c инструкцией https://fsk-r.bitrix24.ru/knowledge/baza_znaniy/oformleniekomandirovok/\nЕсли у Вас остались вопросы обратитесь к координатору операционного департамента Макаровой Ю.В. (KorolevaYV@fsk.ru )",
                },
            "Офис": {"Как заказать пропуск в центральном офисе?":"Ознакомьтесь с [инструкцией](https://portal.fsk.ru/upload/medialibrary/1c8/ldbphamuukvvzpwycxbcjuz9rq1pua7o/4_%D0%97%D0%B0%D0%BA%D0%B0%D0%B7%20%D0%BF%D1%80%D0%BE%D0%BF%D1%83%D1%81%D0%BA%D0%B0%20%D0%B8%20%D0%B0%D0%BA%D1%81%D1%81%D0%B5%D1%81%D1%83%D0%B0%D1%80%D0%BE%D0%B2.pdf) на портале ГК ФСК",
                     "Где взять канц.товары?":"Канцелярские товары размещены в канцпоинте (встроенный шкаф рядом с кофе-поинтом).\nЕсли Вы не нашли необходимые канцелярские товары, то обратитесь к Руководителю АХО Виктории Родионовой",
                     "Не  работает  принтер/сканер":"Обратитесь к Руководителю отдела ИТ-инфраструктуры Гасилову Д.С. (GasilovDS@fsk.ru )"
                },
            "Личные данные": {"Как изменить фото на портале https://portal.fsk.ru/ ?":"Ознакомьтесь с инструкцией\nhttps://portal.fsk.ru/news/153043/?sphrase_id=524115",
                              "Мои данные неверно отражаются на портале https://portal.fsk.ru/":"Обратитесь в техническую поддержку (hd@fsk.ru )",
                              "У меня поменялись персональные данные (ФИО, данные паспорта, диплом и т.п.)":"Направьте информацию на e-mail OtdelKA@fsk-lider.ru "}
        }

    def get_questions(self):
         return [key for subdict in self.categories.values() for key in subdict.keys()]


class RequestClass(BaseHandlerClass):
    pass
