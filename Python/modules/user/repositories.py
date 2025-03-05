from typing import Dict, Literal, cast
from database import DatabaseFactory
from modules.user.typings import UserType
from werkzeug.security import check_password_hash
import bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token
ConditionKey = Literal[
    'id',
    'campo1',
    'campo2'
]


class UserRow(UserType):
    pass


class UserRepository:
    def __init__(self, db_factory: DatabaseFactory) -> None:
        self.db_factory = db_factory

    def get_mysql_user(self, json: Dict) -> Dict:
        """
        Query MySQL users based on the provided conditions.

        :param json: Dictionary containing 'email' and 'senha'.
        :return: Access token and refresh token.
        """
        mysql_conn = self.db_factory.get_mysql_connection()

        query = """SELECT id, senha FROM usuario WHERE email = %s"""
        with mysql_conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, [json.get('email')])
            result = cursor.fetchone()

            if result and bcrypt.checkpw(json.get('senha').encode(), result['senha'].encode()):
                user_identity = str(result['id'])  # Converta para string
                access_token = create_access_token(identity=user_identity)
                refresh_token = create_refresh_token(identity=user_identity)
                return access_token, refresh_token

        raise ValueError("Email ou senha inválidos.")

        

    
    def create(self , json: Dict) -> Dict:
        """
        Insere um novo usuário no banco de dados, garantindo que a senha seja armazenada de forma segura.

        :param json: Dicionário contendo os campos e valores do novo usuário.
        :return: Dicionário com os dados inseridos e o ID do usuário.
        """
        if not json:
            raise ValueError("Nenhum dado fornecido para inserção.")

        mysql_conn = self.db_factory.get_mysql_connection()

        # Verifica se a senha foi fornecida e criptografa antes de inserir no banco
        if "senha" in json:
            hashed_password = bcrypt.hashpw(json["senha"].encode(), bcrypt.gensalt())
            json["senha"] = hashed_password  # Armazena como string no banco
        
        columns = list(json.keys())
        values = list(json.values())
        query = f"""INSERT INTO usuario ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(values))})"""

        try:
            with mysql_conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, tuple(values))
                mysql_conn.commit()
                json["id"] = cursor.lastrowid  # Adiciona o ID gerado ao retorno
        except Exception as e:
            mysql_conn.rollback()
            raise RuntimeError(f"Erro ao inserir usuário: {str(e)}")
        finally:
            mysql_conn.close()

        return json