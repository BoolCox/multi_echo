from nonebot_plugin_orm import Model
from sqlalchemy import String, Column, Integer


class Delay(Model):
    __tablename__ = "delays"

    id = Column(Integer, primary_key=True)

    bot_qq = Column(String, unique=True, index=True)
    delay = Column(Integer, default=0)
