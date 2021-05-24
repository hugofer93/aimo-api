from typing import List, Optional

from bcrypt import checkpw, gensalt, hashpw
from peewee import CharField, ForeignKeyField, Model, ModelSelect, TextField

from database import db_instance
from utils.models import BaseModel


class User(BaseModel):
    username = CharField(45, unique=True)
    password = CharField(128)

    def save(self, force_insert: bool = False,
             only: Optional[List[str]] = None) -> None:
        """Modify the default behavior for hashing the password."""
        if not self._pk:
            self.set_password(self.password)
        return super().save(force_insert=force_insert, only=only)

    def set_password(self, raw_password: str) -> None:
        """hash user password.

        Args:
            raw_password (str): User password
        """
        hashed_password = hashpw(raw_password.encode('utf-8'),
                                 gensalt(rounds=12))
        raw_hashed_password = hashed_password.decode('utf-8')
        self.password = raw_hashed_password

    def check_password(self, raw_password: str) -> bool:
        """Check user password with hash.

        Args:
            raw_password (str): User password.

        Returns:
            bool: If is successful.
        """
        try:
            is_correct = checkpw(raw_password.encode('utf-8'),
                                 self.password.encode('utf-8'))
        except ValueError as error:
            is_correct = False
        return is_correct

    @classmethod
    def get_user(cls, username: str) -> Model:
        """Get user from database.

        Args:
            username (str): Username.

        Raises:
            JSONResponseNotFound: If user doesn't exist.

        Returns:
            UserModel: User instance.
        """
        try:
            user_list = cls.select_available()
            user = user_list.where(cls.username == username).get()
        except cls.DoesNotExist as error:
            user = None
        return user

    def __str__(self) -> str:
        return self.username


# Create User model.
db_instance.create_tables([User, ])


class Note(BaseModel):
    name = CharField(60)
    text = TextField()
    user = ForeignKeyField(User, backref='notes')

    @classmethod
    def get_user_notes(cls, user: User) -> ModelSelect:
        """Get the user's note list.

        Args:
            user (User): User instance.

        Returns:
            ModelSelect: User's note list.
        """
        user_notes = cls.select_available().where(cls.user == user.id)
        return user_notes

    def __str__(self) -> str:
        return self.name


# Create Note model.
db_instance.create_tables([Note, ])
