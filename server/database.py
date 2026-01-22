# JSON/SQLITE para usuarios y relaciones
import json
import os
from typing import Dict, Optional

class UserDataBase:
    def __init__(self, db_file: str = "users.json"):
        self.db_file = db_file
        self.data = self._load_data()

    def _load_data(self) -> Dict:
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as f:
                return json.load(f)
        return {"users": {}}
    
    def _save_data(self):
        with open(self.db_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def add_user(self, username: str, password_hash: str, name: str, photo: str = ""):
        if username in self.data["users"]:
            return False
        self.data["users"][username] = {
            "name": name,
            "photo": photo,
            "password_hash": password_hash,
            "friends": []
        }
        self._save_data()
        return True
    
    def get_user(self, username: str) -> Optional[Dict]:
        return self.data["users"].get(username)
    
    def add_friend(self, user1: str, user2: str):
        if user1 in self.data["users"] and user2 in self.data["users"]:
            if user2 not in self.data["users"][user1]["friends"]:
                self.data["users"][user1]["friends"].append(user2)
            
            if user1 not in self.data["users"][user2]["friends"]:
                self.data["users"][user2]["friends"].append(user1)
            self._save_data()
            return True
        
        return False
    
    def remove_friend(self, user1: str, user2: str):
        if user1 in self.data["users"] and user2 in self.data["users"]:
            if user2 in self.data["users"][user1]["friends"]:
                self.data["users"][user1]["friends"].remove(user2)
            if user1 in self.data["users"][user2]["friends"]:
                self.data["users"][user2]["friends"].remove(user1)
            self._save_data()
            return True
        return False