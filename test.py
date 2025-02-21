from config import B24_WH
import requests


API_METHOD = "disk.folder.getchildren"

url = f"{B24_WH}{API_METHOD}"

FOLDER_IDS = {"Тест проекный архив":(367992, ["Проект 1", "Файл 1.docx", "Файл 2.docx"])}



def get_disk_content_report(folders: dict):
    disk_content = []
    for folder in folders:
        disk_content.append(folder)
        # print(f"Название папки - {folder}")
        # print(folders[folder])
        id, temple_folder = folders[folder]
        # print(id)
        folder_content = get_folder_content(id)
        # print(folder_content)
        for temple_file in temple_folder:
            if temple_file in folder_content:
                disk_content.append(f"{temple_file} ✅")
            else:
                disk_content.append(f"{temple_file} ❌")
    return '\n'.join(disk_content)
# def get_disk_content(folders: dict):
#     disk_content = []
#     for folder in folders:
#         disk_content.append(folder)
#         id, *content_temple = folders[folder]
#         folder_content = get_folder_content(id)
#         print(content_temple)
#         for temple_folder in content_temple:
#             if temple_folder in folder_content:
#                 disk_content.append(f"{temple_folder} - есть")
#             else:
#                 disk_content.append(f"{temple_folder} - нет")
#     print(disk_content)

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


# print(B24_WH)
print(get_disk_content_report(FOLDER_IDS))
