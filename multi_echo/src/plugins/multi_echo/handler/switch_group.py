from arclet.alconna import CommandMeta
from nonebot.adapters.onebot.v11 import Message, Bot
from nonebot_plugin_alconna import on_alconna, Alconna, Args, Match
from nonebot_plugin_orm import async_scoped_session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from .permission import ADMIN_OR_SUPER_ADMIN
from .utils import _valid_qq
from ..model.group import Group

add_group = on_alconna(
    Alconna("添加群", Args["qq?", str], meta=CommandMeta(compact=True)),
    response_self=True,
    permission=ADMIN_OR_SUPER_ADMIN,
    block=True
)
del_group = on_alconna(
    Alconna("删除群", Args["qq?", str], meta=CommandMeta(compact=True)),
    response_self=True,
    permission=ADMIN_OR_SUPER_ADMIN,
    block=True
)


@add_group.handle()
async def handler_add_group(bot: Bot, session: async_scoped_session, qq: Match[str]):
    try:
        group = _valid_qq(Message(str(qq.result)))
    except ValueError:
        await add_group.finish("群号不合法")
        return

    try:
        session.add(Group(bot_qq=bot.self_id, platform_id=group))
        await session.commit()
        await add_group.finish(f"已添加群：{group}")

    except IntegrityError:
        await session.rollback()
        await add_group.finish(f"已添加群：{group}")


@del_group.handle()
async def handler_del_group(bot: Bot, session: async_scoped_session, qq: Match[str]):
    try:
        group = _valid_qq(Message(str(qq.result)))
    except ValueError:
        await del_group.finish("群号不合法")
        return

    try:
        result = await session.execute(
            select(Group)
            .where(
                Group.bot_qq == bot.self_id,
                Group.platform_id == group
            )
        )
        obj = result.scalar_one_or_none()

        if obj is not None:
            await session.delete(obj)
            await session.commit()

        await del_group.finish("已取消设置该群")

    except SQLAlchemyError:
        await session.rollback()
        await del_group.finish("数据库错误，取消失败")
