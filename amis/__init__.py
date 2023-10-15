"""基于百度amis框架的python pydantic模型封装，
详细文档请看https://aisuda.bce.baidu.com/amis/zh-CN/docs/index
"""
from .base import (
    AmisNode as AmisNode,
    APIResponse as APIResponse,
    BaseAmisModel as BaseAmisModel,
)
from .event import *
from .render import render_as_html as render_as_html
