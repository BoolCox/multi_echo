# from nonebot import get_plugin_config
from nonebot import require
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import add_global_extension
from nonebot_plugin_alconna.builtins.extensions.onebot11 import MessageSentExtension

from .config import EchoConfig
from .handler.control_switch import follow_switch
from .handler.echo import echo
from .handler.manage_admin import add_admin
from .handler.set_delay import set_delay
from .handler.switch_group import add_group
from .handler.user_follow_command import follow_user
from .handler.view_staus import view_status, handler_view_whitelist_group
from .model.admin import Admin
from .model.follow import Follow
from .model.follow_switch import FollowSwitch
from .model.group import Group

require("nonebot_plugin_orm")
require("nonebot_plugin_alconna")
add_global_extension(MessageSentExtension())

__plugin_meta__ = PluginMetadata(
    name="multi_echo",
    description="用多个账号复读指定用户的消息",
    usage="",
    config=EchoConfig,
)

# config = get_plugin_config(EchoConfig)
