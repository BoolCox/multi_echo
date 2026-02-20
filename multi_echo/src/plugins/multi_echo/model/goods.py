from nonebot_plugin_orm import Model
from sqlalchemy import Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column


class Goods(Model):
    """商品目录表"""
    __tablename__ = "goods"

    id: Mapped[int] = mapped_column(primary_key=True)
    bot_qq: Mapped[str] = mapped_column(String(64), comment="Bot QQ号")
    code: Mapped[str] = mapped_column(String(64), comment="商品代号")
    max_price: Mapped[int] = mapped_column(Integer, comment="费用上限")
    min_price: Mapped[int] = mapped_column(Integer, default=0, comment="费用下限")
    is_onepack: Mapped[bool] = mapped_column(default=False, comment="是否一包杀")

    __table_args__ = (
        UniqueConstraint("bot_qq", "code", "is_onepack", name="uq_goods_bot_qq_code_onepack"),
    )
