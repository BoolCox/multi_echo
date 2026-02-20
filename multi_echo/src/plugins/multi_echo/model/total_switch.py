from nonebot_plugin_orm import Model
from sqlalchemy import Boolean, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column


class TotalSwitch(Model):
    """总开关表"""
    __tablename__ = "follow_switches"
    id: Mapped[int] = mapped_column(primary_key=True)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False)

    __table_args__ = (
        CheckConstraint("id = 1", name="ck_feature_switch_singleton"),
    )
