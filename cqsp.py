# -*- coding: utf-8 -*-
import asyncio
import os
import requests
import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import GroupMessage, Message

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_group_at_message_create(self, message: GroupMessage):
     if "随机视频" in message.content:
       url = "http://www.wudada.online/Api/ScSp"  # 更新为你的API请求URL
       response = requests.get(url)
       data = response.json()
       try:
        data = response.json()
        if data["code"] == "200":
            file_url = data["data"]  # 获取从API返回的URL
            uploadMedia = await message._api.post_group_file(
            group_openid=message.group_openid, 
            file_type=2, # 文件类型要对应上，具体支持的类型见方法说明
            url=file_url # 文件Url
            )
            # 资源上传后，会得到Media，用于发送消息
            await message._api.post_group_message(
            group_openid=message.group_openid,
            msg_type=7,  # 7表示富媒体类型
            msg_id=message.id, 
            media=uploadMedia
            )
        else :
            messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_id=message.id,
                content=f"\n请求超时{e}")
       except Exception as e:
        _log.error(f"处理消息时出现异常：{e}")
        await message._api.post_group_message(
        group_openid=message.group_openid,
        msg_id=message.id,
        content=f"\ntx服务器：“上传资源失败！”：\n{e}")
if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], secret=test_config["secret"])