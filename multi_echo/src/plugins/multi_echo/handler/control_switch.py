from nonebot_plugin_orm import async_scoped_session

from ..model.total_switch import TotalSwitch
from ..command import total_switch


@total_switch.handle()
async def handler_total_switch(session: async_scoped_session):
    """处理总开关的命令"""
    obj = await session.get(TotalSwitch, 1)

    if obj is None:
        obj = TotalSwitch(id=1, enabled=True)
        session.add(obj)
        new_status = True
    else:
        obj.enabled = not obj.enabled
        new_status = obj.enabled

    await session.commit()

    await total_switch.finish(
        "已开启总开关" if new_status else "已关闭总开关"
    )
