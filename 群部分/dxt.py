# -*- coding: utf-8 -*-
import psutil
import datetime
import asyncio
import os
import botpy
import time
from botpy import logging
from botpy.message import Message
from botpy.types.message import Embed
from botpy.ext.cog_yaml import read
from botpy.message import GroupMessage, Message

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()
class MyClient(botpy.Client):
        #这里是频道@机器人发送指令
    async def on_at_message_create(self, message: Message):
      if "系统" in message.content:
        # 获取 CPU 使用率
        cpu_percent = psutil.cpu_percent(interval=1)

        # 获取内存使用情况
        memory_info = psutil.virtual_memory()
        memory_percent = memory_info.percent
        memory_used = memory_info.used
        memory_total = memory_info.total

        # 获取交换空间使用情况
        swap_info = psutil.swap_memory()
        swap_percent = swap_info.percent
        swap_used = swap_info.used
        swap_total = swap_info.total
        
        # 获取系统运行时间
        uptime_seconds = int(time.time() - psutil.boot_time())
        uptime_readable = datetime.timedelta(seconds=uptime_seconds)

        # 打印获取的数据
        response = (
            f"CPU 使用率: {cpu_percent}%\n"
            f"内存使用率: {memory_percent}%\n"
            f"交换空间使用率: {swap_percent}%\n"
            f"系统运行时间: {uptime_readable}"
        )
        # 回复获取的系统信息
        await message.reply(content=response)
        
        #下面是群聊端
    async def on_group_at_message_create(self, message: GroupMessage):
      if "系统" in message.content or "状态" in message.content:
        # 获取 CPU 使用率
        cpu_percent = psutil.cpu_percent(interval=1)

        # 获取内存使用情况
        memory_info = psutil.virtual_memory()
        memory_percent = memory_info.percent
        memory_used = memory_info.used
        memory_total = memory_info.total

        # 获取交换空间使用情况
        swap_info = psutil.swap_memory()
        swap_percent = swap_info.percent
        swap_used = swap_info.used
        swap_total = swap_info.total
        
        # 获取系统运行时间
        uptime_seconds = int(time.time() - psutil.boot_time())
        uptime_readable = datetime.timedelta(seconds=uptime_seconds)

        # 打印获取的数据
        response = (
            f"CPU 使用率: {cpu_percent}%\n"
            f"内存使用率: {memory_percent}%\n"
            f"交换空间使用率: {swap_percent}%\n"
            f"系统运行时间: {uptime_readable}"
        )
        # 回复获取的系统信息
        messageResult = await message._api.post_group_message(
        group_openid=message.group_openid,
        msg_type=0, 
        msg_id=message.id,
        content=response)
if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_guild_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents.default()
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], secret=test_config["secret"])