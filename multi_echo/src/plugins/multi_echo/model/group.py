from nonebot_plugin_orm import Model
from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column


class Group(Model):
    """群白名单表"""
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    bot_qq: Mapped[str] = mapped_column(String(64), comment="Bot QQ账号")
    platform_id: Mapped[str] = mapped_column(String(64), comment="QQ群号")

    __table_args__ = (
        UniqueConstraint("bot_qq", "platform_id", name="uq_group_bot_qq_platform_id"),
    )
