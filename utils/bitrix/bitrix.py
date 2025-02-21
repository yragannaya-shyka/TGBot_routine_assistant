from config import B24_WH, B24_SP_ID
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Category:
    name: str
    value: str

@dataclass
class Command:
    name: str

@dataclass
class Param:
    field: str
    value: Optional[str]
    name: Optional[str]


class BitrixRequest:
    def __init__(self):

        self.categoryes = {
            "access_rights": Category(name="Предоставление прав доступа", value="158"),
            "new_user": Category(name="Добавление нового сотрудника", value="160")
        }

        self.commands = {
            "create_request": Command(name="crm.item.add.json")
        }

        self.params = {
            "title": Param(field="TITLE", value=None, name="Название"),
            "request_category": Param(field="ufCrm_12_1723450334376", value=None, name="Категория заявки"),
            "initiator": Param(field="ufCrm_12_1732527565", value=None, name="Заявитель"),
            "initiator_tg_id": Param(field="ufCrm_12_1736781758613", value=None, name="Телеграм заявителя"),
            "request_id": Param(field="ufCrm_12_1738307039", value=None, name="Номер заявки"),
            "new_user_name": Param(field="ufCrm_12_1736781830742", value=None, name="ФИО нового сотрудника"),
            "new_user_position": Param(field="ufCrm_12_1736781849952", value=None, name="Должность"),
            "new_user_division": Param(field="ufCrm_12_1736781881035", value=None, name="Подразделение"),
            "new_user_supervisor": Param(field="ufCrm_12_1736781897", value=None, name="Руководитель сотрудника"),
            "acces_rights_user": Param(field="ufCrm_12_1737536925", value=None, name="ФИО сотрудника для предоставления доступа"),
            "acces_rights_type": Param(field="ufCrm_12_1737537025432", value=None, name="Тип прав доступа"),
            "acces_rights_object_link": Param(field="ufCrm_12_1737537083844", value=None, name="Ссылка на объект предоставления доступа"),
        }

    def get_clear_params(self) -> dict:
        return {i.field: i.value for i in self.params.values() if i.value is not None}


    def get_data_for_record(self) -> dict:
        return {key:{"field": value.field, "value": value.value, "name": value.name} for key, value in self.params.items() if value.value is not None}

    def create_bitrix_smart_process_element(self, request_categoty) -> str:
        command = self.commands["create_request"].name
        self.params["request_category"].value = self.categoryes[request_categoty].value
        clear_params = self.get_clear_params()
        fields = "&".join([f"fields[{field}]={value}" for field, value in clear_params.items() if value is not None])
        return f"{B24_WH}{command}?entityTypeId={B24_SP_ID}&{fields}"
