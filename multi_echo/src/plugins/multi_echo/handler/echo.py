import asyncio

from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot_plugin_orm import async_scoped_session
from sqlalchemy import select

from ..command import echo
from ..model.delay import Delay
from ..model.follow import Follow
from ..model.follow_switch import FollowSwitch
from ..model.group import Group


async def is_group_registered(event: GroupMessageEvent, session: async_scoped_session) -> bool:
    group = event.group_id
    result = await session.execute(
        select(Group)
        .where(
            Group.bot_qq == str(event.self_id),
            Group.platform_id == group
        )
    )
    obj = result.scalar_one_or_none()
    return bool(obj)


@echo.handle()
async def handler_echo(event: GroupMessageEvent, session: async_scoped_session):
    # 总开关和白名单校验
    result = await session.get(FollowSwitch, 1)
    if result is None or not result.enabled or not await is_group_registered(event, session):
        return

    # 如果消息不是以@人开头，返回
    # 如果消息是@机器人，则没有@消息段，因此 type=text 也会返回
    if event.message[0].type != "at":
        return

    # 当@后的内容不为纯数字，返回
    text = event.message[1].data.get("text").strip()
    if not text.isdigit():
        return

    # 如果不符合跟随规则，返回
    bot_id = event.self_id
    user_id = event.get_user_id()
    result = await session.execute(
        select(Follow).where(
            Follow.bot_id == bot_id,
            Follow.user_id == user_id
        )
    )
    obj = result.scalar_one_or_none()
    if not obj:
        return

    # 从数据库读取当前机器人的延迟
    res = await session.execute(
        select(Delay)
        .where(
            Delay.bot_qq == bot_id
        )
    )
    delay_obj = res.scalar_one_or_none()
    delay_ms = delay_obj.delay if delay_obj else 0
    if delay_ms and delay_ms > 0:
        await asyncio.sleep(delay_ms / 1000)

    await echo.send(event.get_message())
