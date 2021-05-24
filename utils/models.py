from datetime import datetime

from peewee import AutoField, BooleanField, DateTimeField, Model, ModelSelect

from database import db_instance


class BaseModel(Model):
    id = AutoField()
    available = BooleanField(default=True)
    creation_date = DateTimeField(default=datetime.now)

    @classmethod
    def select_available(cls) -> ModelSelect:
        """Select only available.

        Returns:
            ModelSelect: Items list.
        """
        return cls.select().where(cls.available == True)

    class Meta:
        database = db_instance
