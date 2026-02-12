import re

from nonebot.adapters.onebot.v11 import Message


def _valid_qq(qq: Message) -> str:
    qq = qq.extract_plain_text().strip()
    if not re.fullmatch(r"[1-9]\d{5,12}", qq):
        raise ValueError
    return qq
