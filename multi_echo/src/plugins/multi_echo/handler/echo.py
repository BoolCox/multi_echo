import asyncio
import re

from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment
from nonebot_plugin_orm import async_scoped_session
from sqlalchemy import select

from ..command import echo
from ..model.delay import Delay
from ..model.total_switch import TotalSwitch
from ..model.goods import Goods
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
    result = await session.get(TotalSwitch, 1)
    if result is None or not result.enabled or not await is_group_registered(event, session):
        return

    message_text = event.get_message().extract_plain_text().strip()
    match = re.fullmatch(r"收2/([^/]+)/(?P<fee>\d+)(?P<onepack>一包杀)?", message_text)
    reply_fee: int | None = None
    if match:
        code = match.group(1).strip()
        fee = int(match.group("fee"))
        is_onepack = match.group("onepack") is not None
        if not code:
            return
        # 这里不再校验商品编码的格式，允许非数字的代号

        # 校验费用
        result = await session.execute(
            select(Goods)
            .where(
                Goods.bot_qq == str(event.self_id),
                Goods.code == code,
                Goods.is_onepack == is_onepack
            )
        )
        goods = result.scalar_one_or_none()
        if goods is None:
            return
        if fee < goods.min_price or fee > goods.max_price:
            return
        reply_fee = fee

    # 从数据库读取当前机器人的延迟
    bot_id = event.self_id
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

    if reply_fee is not None:
        await echo.send(MessageSegment.at(event.get_user_id()) + str(reply_fee))
        return
