import re


def _valid_qq(qq: str) -> str:
    qq = qq.strip()
    if not re.fullmatch(r"[1-9]\d{5,12}", qq):
        raise ValueError
    return qq
