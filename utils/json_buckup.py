import json
import os
from typing import Any, Dict
from scheme.config import Settings

class JsonBackupHandler:
    def __init__(self, file_path: str = Settings.JSON_FILE_PATH):
        self.file_path = file_path

    def load_backup(self) -> Dict[str, Any]:
        if not os.path.exists(self.file_path):
            return {}
        
        with open(self.file_path, "r", "utf-8") as file:
            try:
                return json.load(file)
            except Exception as e:
                raise e
            
    def 
    