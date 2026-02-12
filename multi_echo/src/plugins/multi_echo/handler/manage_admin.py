from arclet.alconna import CommandMeta
from nonebot.adapters.onebot.v11 import Message, Bot
from nonebot_plugin_alconna import on_alconna, Alconna, Args, Match
from nonebot_plugin_orm import async_scoped_session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from .permission import SUPER_ADMIN
from .utils import _valid_qq
from ..model.admin import Admin

add_admin = on_alconna(
    Alconna("添加主人", Args["qq?", str], meta=CommandMeta(compact=True)),
    response_self=True,
    permission=SUPER_ADMIN,
    block=True
)
del_admin = on_alconna(
    Alconna("删除主人", Args["qq?", str], meta=CommandMeta(compact=True)),
    response_self=True,
    permission=SUPER_ADMIN,
    block=True
)


@add_admin.handle()
async def handler_add_admin(
        bot: Bot,
        session: async_scoped_session,
        qq: Match[str]
):
    try:
        admin = _valid_qq(Message(qq.result))
    except ValueError:
        await add_admin.finish("QQ号不合法")
        return

    try:
        session.add(Admin(bot_qq=bot.self_id, admin_qq=admin))
        await session.commit()
        await add_admin.finish(f"已设置主人：{admin}")

    except IntegrityError:
        await session.rollback()
        await add_admin.finish(f"已设置主人：{admin}")


@del_admin.handle()
async def handler_del_admin(
        bot: Bot,
        session: async_scoped_session,
        qq: Match[str]
):
    try:
        admin = _valid_qq(Message(qq.result))
    except ValueError:
        await add_admin.finish("QQ号不合法")
        return

    try:
        stmt = (
            select(Admin)
            .where(
                Admin.bot_qq == bot.self_id,
                Admin.admin_qq == admin
            )
        )
        result = await session.execute(stmt)
        obj = result.scalar_one_or_none()

        if obj is not None:
            await session.delete(obj)
            await session.commit()

        await del_admin.finish("已取消设置该主人")

    except SQLAlchemyError:
        await session.rollback()
        await del_admin.finish("数据库错误，取消失败")
