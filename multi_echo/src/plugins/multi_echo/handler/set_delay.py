from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, GroupMessageEvent
from nonebot.params import CommandArg
from nonebot.rule import to_me
from nonebot_plugin_orm import async_scoped_session
from sqlalchemy import select

from .permission import ADMIN_OR_SUPER_ADMIN
from ..model.delay import Delay

set_delay = on_command("设置跟随延迟", rule=to_me(), permission=ADMIN_OR_SUPER_ADMIN, block=True)


@set_delay.handle()
async def handler_set_delay(event: GroupMessageEvent, session: async_scoped_session, args: Message = CommandArg()):
    arg = args.extract_plain_text().strip()
    if not arg.isdigit():
        await set_delay.finish("请输入0~30000之间的整数（毫秒）")
    delay = int(arg)
    if not (0 <= delay <= 30000):
        await set_delay.finish("延迟必须在0~30000毫秒之间")

    bot_id = str(event.self_id)

    # 查询现有记录
    res = await session.execute(select(Delay).where(Delay.bot_qq == bot_id))
    obj = res.scalar_one_or_none()
    if obj:
        obj.delay = delay
    else:
        obj = Delay(bot_qq=bot_id, delay=delay)
        session.add(obj)

    await session.commit()
    await set_delay.finish(f"已将本账号的跟随延迟设置为 {delay} 毫秒")
