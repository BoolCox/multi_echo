from nonebot_plugin_orm import Model
from sqlalchemy import String, Column, Integer, UniqueConstraint


class Follow(Model):
    __tablename__ = "follows"

    id = Column(Integer, primary_key=True)

    bot_id = Column(String)
    user_id = Column(String)

    # bot_id 和 user_id 这对组合不能重复
    __table_args__ = (
        UniqueConstraint("bot_id", "user_id"),
    )
