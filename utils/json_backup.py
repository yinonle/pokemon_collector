import json
import os
from pathlib import Path
from typing import Any, Dict, List
from config import settings

BASE_DIR = Path(__file__).resolve().parent.parent


class JsonBackupFile:
    def __init__(self, file_path: str = settings.JSON_FILE_PATH):
        self.file_path = BASE_DIR / file_path

    def load_backup(self) -> Dict[str, Any]:
        if not self.file_path.exists() or self.file_path.stat().st_size == 0:
            return {}
        
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}
        except Exception as e:
            raise e
            
    def save_pokemon_to_json(self, pokemon_list: List[Any]) -> None:
        data = {}

        for pokemon in pokemon_list:
            if hasattr(pokemon, "model_dump"):
                p_dict = pokemon.model_dump()
            elif isinstance(pokemon, dict):
                p_dict = pokemon
            else:
                continue

            serial_num = p_dict.get("serial_number") or p_dict.get("p_number")
            
            if serial_num is not None:
                format_key = str(serial_num).zfill(3)
                data[format_key] = p_dict


        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent = 4, ensure_ascii = False)