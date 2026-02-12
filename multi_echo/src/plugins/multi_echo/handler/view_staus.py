from nonebot import on_command, get_bots
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.rule import to_me
from nonebot_plugin_orm import async_scoped_session
from sqlalchemy import select

from .permission import ADMIN_OR_SUPER_ADMIN
from ..model.follow import Follow
from ..model.follow_switch import FollowSwitch
from ..model.group import Group

view_status = on_command("查看状态", rule=to_me(), aliases={"查看跟随状态"}, permission=ADMIN_OR_SUPER_ADMIN,
                         block=True)
view_whitelist_group = on_command("查看当前添加群", rule=to_me(), permission=ADMIN_OR_SUPER_ADMIN, block=True)


@view_status.handle()
async def handler_view_status(event: GroupMessageEvent, session: async_scoped_session):
    num = len(get_bots())

    result = await session.execute(select(Follow))
    follows = result.scalars().all()
    total = len(follows)

    if not follows:
        detail = "无"
    else:
        follow_map: dict[str, list[str]] = {}
        for item in follows:
            follow_map.setdefault(item.bot_id, []).append(item.user_id)

        parts: list[str] = []
        for bot_id, user_ids in follow_map.items():
            user_list = "，".join(sorted(set(user_ids)))
            parts.append(f"{bot_id}: {user_list}")

        detail = "；".join(parts)

    # 计算本群是否启用跟随（总开关开启 且 本群在白名单中）
    total_switch = await session.get(FollowSwitch, 1)
    total_enabled = bool(total_switch and total_switch.enabled)
    res = await session.execute(
        select(Group).where(
            Group.bot_qq == str(event.self_id),
            Group.platform_id == event.group_id
        )
    )
    in_whitelist = bool(res.scalar_one_or_none())
    group_status = "开启跟随" if (total_enabled and in_whitelist) else "关闭跟随"

    await view_status.finish(
        f"当前在线账号数：{num}\n"
        f"账号跟随详情：{detail}\n"
        f"跟随规则总数：{total}\n"
        f"本群已{group_status}"
    )


@view_whitelist_group.handle()
async def handler_view_whitelist_group(session: async_scoped_session):
    result = await session.execute(select(Group).order_by(Group.platform_id))
    obj = result.scalars().all()

    group = "；".join(str(item.platform_id) for item in obj)

    await view_whitelist_group.finish(f"当前添加群：{group}")
