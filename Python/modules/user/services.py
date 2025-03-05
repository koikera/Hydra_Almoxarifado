from typing import Dict
from modules.user.repositories import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_user(self, json: Dict):
        return self.repository.get_mysql_user(json)
    
    def create(self, json: Dict):
        return self.repository.create(json)