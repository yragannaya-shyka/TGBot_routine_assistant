from config import B24_WH
import requests


API_METHOD = "disk.folder.getchildren"

url = f"{B24_WH}{API_METHOD}"

FOLDER_IDS = {"Тест проекный архив":(367992,
                                     ["Проект 1", "Файл 1.docx", "Файл 2.docx"],
                                     "https://fsk-r.bitrix24.ru/docs/path/%D0%A4%D0%A1%D0%9A%20%D0%A0%D0%B5%D0%B3%D0%B8%D0%BE%D0%BD/02.%20%D0%9F%D0%BE%D0%B4%D1%80%D0%B0%D0%B7%D0%B4%D0%B5%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F/02.08.%20%D0%94%D0%B5%D0%BF%D0%B0%D1%80%D1%82%D0%B0%D0%BC%D0%B5%D0%BD%D1%82%20%D1%80%D0%B0%D0%B7%D0%B2%D0%B8%D1%82%D0%B8%D1%8F/%D0%94%D0%BB%D1%8F%20%D1%82%D0%B5%D1%81%D1%82%D0%BE%D0%B2%20%D0%91%D0%B8%D1%82%D1%80%D0%B8%D1%8124/%D0%A2%D0%B5%D1%81%D1%82%20%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%BD%D1%8B%D0%B9%20%D0%B0%D1%80%D1%85%D0%B8%D0%B2/")}



def get_folder_content(folerd_id):

    params = {
        'id': folerd_id
    }

    response = requests.post(url, json=params)

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


def get_disk_content_report(folders=FOLDER_IDS):
    disk_content = []
    for folder in folders:
        id, temple_folder, url = folders[folder]
        disk_content.append(f"[{folder}]({url})")
        id, temple_folder, _ = folders[folder]
        folder_content = get_folder_content(id)
        for temple_file in temple_folder:
            if temple_file in folder_content:
                disk_content.append(f"{temple_file} ✅")
            else:
                disk_content.append(f"{temple_file} ❌")
    return '\n'.join(disk_content)
