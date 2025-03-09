from tortoise import Tortoise, fields
from tortoise.models import Model

DB_NAME = "database.db"

class User(Model):
    user_id = fields.BigIntField(pk=True)
    full_name = fields.CharField(max_length=255)

    class Meta:
        table = "users"

async def init_db():
    await Tortoise.init(
        db_url=f'sqlite://{DB_NAME}',
        modules={'models': ['database']},
    )
    await Tortoise.generate_schemas()

async def get_all_users():
    return await User.all().values_list("user_id", flat=True)

async def add_user(user_id: int, full_name: str):
    await User.get_or_create(user_id=user_id, full_name=full_name)

async def close_db():
    await Tortoise.close_connections()
