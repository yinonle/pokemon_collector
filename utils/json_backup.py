import json
import os
from typing import Any, Dict, List
from scheme.config import settings

class JsonBackupFile:
    def __init__(self, file_path: str = settings.JSON_FILE_PATH):
        self.file_path = file_path

    def load_backup(self) -> Dict[str, Any]:
        if not os.path.exists(self.file_path):
            return {}
        
        with open(self.file_path, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except Exception as e:
                raise e
            
    def save_pokemon_batch(self, pokemon_list: List[Dict[str,Any]]) -> None:
        data = self.load_backup()
        for pokemon in pokemon_list:
            serial_num = pokemon["serial_number"]
            if serial_num is not None:
                format_key = str(serial_num).zfill(3)
                data[format_key] = pokemon

        with open(self.file_path, "w", encoding = "utf-8") as file:
            json.dump(data, file, indent = 4, ensure_ascii = False)

        


    