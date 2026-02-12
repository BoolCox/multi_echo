from nonebot import on_command
from nonebot.rule import to_me
from nonebot_plugin_orm import async_scoped_session

from .permission import ADMIN_OR_SUPER_ADMIN
from ..model.follow_switch import FollowSwitch

follow_switch = on_command("切换跟随总开关", rule=to_me(), permission=ADMIN_OR_SUPER_ADMIN, block=True)


@follow_switch.handle()
async def handler_follow_switch(session: async_scoped_session):
    """处理跟随功能总开关的命令"""
    obj = await session.get(FollowSwitch, 1)

    if obj is None:
        obj = FollowSwitch(id=1, enabled=True)
        session.add(obj)
        new_status = True
    else:
        obj.enabled = not obj.enabled
        new_status = obj.enabled

    await session.commit()

    await follow_switch.finish(
        "已开启跟随总开关" if new_status else "已关闭跟随总开关"
    )
