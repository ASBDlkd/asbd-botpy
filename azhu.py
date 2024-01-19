import asyncio
import os
import re
import botpy
import requests
import json
import yaml
import urllib.parse
from lunardate import LunarDate
from PIL import ImageDraw
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
from io import BytesIO
from botpy import logging
from botpy.message import DirectMessage
from botpy.message import Message,BotAPI
from botpy.types.message import Ark, ArkKv
from botpy.ext.cog_yaml import read
from botpy.types.message import Embed, EmbedField
from botpy.message import GroupMessage, Message

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))
config = yaml.load(open('config.yaml', encoding="utf-8").read(), Loader=yaml.FullLoader)

#以上需要安装各种依赖

_log = logging.get_logger()
class MyClient(botpy.Client):
#以下是频道@机器人发送指令    
    async def on_at_message_create(self, message: Message):
    
          #查QQ头像功能                      
        if re.search(r'查头像\s*(.*)', message.content)  :#定义完全匹配指令 @机器人 查头像（QQ号）
            # 获取提到@机器人的用户ID
            user_id = message.author.id
            # 下面提取用户@机器人 指令 内容，提取其中的内容部分
            tiqu = re.search(r'查头像\s*(.*)', message.content).group(1).strip()
            #定义新的URL（把提取的QQ融合在下面URL里）
            api_url = f"https://q.qlogo.cn/headimg_dl?dst_uin={urllib.parse.quote(tiqu)}&spec=640&img_type=jpg"
            #爬取头像并保存到本地，命名为user.jpg
            headers ={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
            }
            r = requests.get(api_url,headers=headers)
            f = open("user.jpg",'wb')
            f.write(r.content)
            f.close()
            #@用户 发送本地图片user.jpg
            await message.reply(content=f"<@{user_id}> 叮叮叮~！你的qq头像查询已送达~",
                                file_image="user.jpg")
                                
            #头像合成指令需要本地图片zan.jpg作为背景
        elif "赞" in message.content:
            url = message.author.avatar
            response = requests.get(url)
            avatar_image = Image.open(BytesIO(response.content))

            # 本地背景图片
            background_image = Image.open("zan.jpg")

            # 将头像调整为60x60的大小
            avatar_image = avatar_image.resize((80, 80))

            # 创建一个新的图片，作为最终的叠加结果
            result_image = Image.new("RGBA", background_image.size, (255, 255, 255, 0))

            # 将背景图片复制到结果图片
            result_image.paste(background_image, (0, 0))
            # 计算头像在左下角的位置（假设留有n像素的间距）
            avatar_position = (50, result_image.size[1] - avatar_image.size[1] - 50)
            # 创建一个圆形的蒙版
            mask = Image.new("L", (80, 80), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, 80, 80), fill=255)
            # 将头像图片应用圆形蒙版
            avatar_image = ImageOps.fit(avatar_image, mask.size, method=0, bleed=0.0, centering=(0.5, 0.5))
            result_image.paste(avatar_image, avatar_position, mask=mask)
            # 显示或保存最终的结果
            result_image.show()
            result_image.save("result_image.png")
            user_id = message.author.id
            #发送本地图片
            await message.reply(content=f"<@{user_id}>叮叮叮~！",
                                file_image="result_image.png")
                                
            #爬取api里的json数据并且发送示例
        elif "搞笑文案" in message.content or "笑一笑" in message.content:
            url = "https://zj.v.api.aa1.cn/api/wenan-gaoxiao/?type=json"
            try:
                response = requests.get(url)
                response.raise_for_status()  # 检查请求是否成功
                res = json.loads(response.text)
                qinggan = res["msg"]
                await message.reply(content=qinggan)
            except requests.exceptions.RequestException as e:
                reply_message = "抱歉，巴迪对搞笑文案请求上限暂时无法获取，请明天再试。"
                await message.reply(content=reply_message)

        #以下是发送embed消息模板示例：
        elif "太空乐人" in message.content:
            embed = {
                "title": "你喜欢吃西瓜吗",
                "prompt": "太空乐人",
                "thumbnail": {
                     "url": message.author.avatar       #获取用户URL
                     },
                "fields": [
                    {
                        "name": "恭喜你发现了隐藏彩蛋🎉"
                    },
                    {
                        "name": "   "
                    },
                    {
                        "name": "西瓜："
                    },
                    {
                        "name": "它还富含水分和营养，对身体健康有益。"
                    },
                    {
                        "name": "许多人都喜欢它的甜美和清凉口感呢！太空乐人也喜欢吃吗？"
                    },
                    ]
                    }
            #发送被动embed消息模板方法
            await message.reply(embed=embed)
            
        #官方案例发送频道个人头像
        elif "我的头像" in message.content:
          await message.reply(image=message.author.avatar)
          
        #发送壁纸api示例
        elif "二次元" in message.content:
          image_url= "https://t.mwm.moe/pc"#"这里填图片api的URL"
          headers ={
          'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
          }
          #下载到本地
          r = requests.get(image_url,headers=headers)
          f = open("3.jpg",'wb')
          f.write(r.content)
          f.close()
          #@用户，发送给用户
          user_id = message.author.id
          await message.reply(content=f"<@{user_id}> 叮叮叮~！你的二次元图片已送达~",
                                file_image="3.jpg")
                                
        #这里是发送ark示例
        elif "百变图" in message.content:
          payload: Ark = Ark(
             template_id=37,
             kv=[
                 ArkKv(key="#METATITLE#", value="百变图"),
                 ArkKv(key="#PROMPT#", value="百变图自动刷新"),
                 ArkKv(key="#TITLE#", value="标题"),
                 ArkKv(key="#METACOVER#", value=""),#这里是一个图片URL，但是需要URL加白
             ],
             )
             #发送被动ark示例
          await message.reply(ark=payload)
          
        #在某个频道存在的权限
        elif "存在的权限" in message.content:
          apis = await self.api.get_permissions(message.guild_id)
          for api in apis:
             _log.info("api: %s" % api["desc"] + ", status: %d" % api["auth_status"])
         #获取频道信息
        elif "频道信息" in message.content:
            guild = await self.api.get_guild(guild_id=message.guild_id)
            guild_info = (
                f"频道id: {guild['id']}\n"
                f"频道名称: {guild['name']}\n"
                f"频道成员数量: {guild['member_count']}\n"
                f"频道最大容量: {guild['max_members']}\n"
                f"频道描述: {guild['description']}"
            )
            await self.api.post_message(channel_id=message.channel_id, content=guild_info, msg_id=message.event_id)
            
           #消息模板embed发送示例
        elif "指令" in message.content or "菜单" in message.content or "功能" in message.content:
            embed = {
                "title": "菜单",
                "prompt": "菜单&指令&功能",
                "thumbnail": {
                     "url": message.author.avatar
                     },
                "fields": [
                    {
                        "name": "叮叮叮~！你好哇！(❤️ ω ❤️)"
                    },
                    {
                        "name": "当前指令有："
                    },
                    {
                        "name": "巴迪正在努力迭代更新中……"
                    }
                    ]
                    }
            await message.reply(embed=embed)

    #以下是频道私信机器人相关代码
    async def on_direct_message_create(self, message: DirectMessage):
    
      if "搞笑文案" in message.content or "笑一笑" in message.content:
            url = "https://zj.v.api.aa1.cn/api/wenan-gaoxiao/?type=json"
            try:
                response = requests.get(url)
                response.raise_for_status()  # 检查请求是否成功
                res = json.loads(response.text)
                qinggan = res["msg"]
                await message.reply(content=qinggan)
            except requests.exceptions.RequestException as e:
                reply_message = "抱歉，巴迪对搞笑文案请求上限暂时无法获取，请明天再试。"
                await message.reply(content=reply_message)

      elif "我的头像" in message.content:
         await message.reply(image=message.author.avatar)

      elif "二次元" in message.content:
          image_url= "https://t.mwm.moe/pc"
          headers ={
          'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
          }
          r = requests.get(image_url,headers=headers)
          f = open("3.jpg",'wb')
          f.write(r.content)
          f.close()
          await message.reply(content=f"叮叮叮~！你的二次元图片已送达~",
          file_image="3.jpg")
        
        #私信端发送ark37
      elif "百变图" in message.content:
          payload: Ark = Ark(
             template_id=37,
             kv=[
                 ArkKv(key="#METATITLE#", value="百变图"),
                 ArkKv(key="#PROMPT#", value="百变图自动刷新"),
                 ArkKv(key="#TITLE#", value="标题"),
                 ArkKv(key="#METACOVER#", value=""),#这里依旧需要已加白的图片URL
             ],
             )
          #await self.api.post_message(channel_id=message.channel_id, ark=payload,)
          await message.reply(ark=payload)
          
          #频道私信端embed消息模板
      elif "指令" in message.content or "菜单" in message.content or "功能" in message.content:
              embed = {
                "title": "菜单",
                "prompt": "菜单&指令&功能",
                "thumbnail": {
                     "url": message.author.avatar
                     },
                "fields": [
                    {
                        "name": "叮叮叮~！你好哇！(❤️ ω ❤️)"
                    },
                    {
                        "name": "当前指令有："
                    },
                    },
                    {
                        "name": "巴迪正在努力迭代更新中……"
                    }
                    ]
                    }
              #await self.api.post_message(channel_id=message.channel_id, embed=embed)
              await message.reply(embed=embed)

              
              
    #以下是群聊@机器人发送指令代码（目前个人开发者除了参赛选手是没有监听群事件的权限的）
    #注意如果没有监听权限要删掉 群 监听部分所有代码！！
    async def on_group_at_message_create(self, message: GroupMessage):

        if re.search(r'查头像\s*(.*)', message.content):
            # 提取投稿内容
            tiqu = re.search(r'查头像\s*(.*)', message.content).group(1).strip()
            # 发送回复消息，提到用户并表示投稿成功，并显示提取的投稿内容
            file_url = f"https://q.qlogo.cn/headimg_dl?dst_uin={urllib.parse.quote(tiqu)}&spec=640&img_type=jpg"
            upload_media = await message._api.post_group_file(
            group_openid=message.group_openid,
            file_type=1,  # 文件类型要对应上，具体支持的类型见方法说明
            url=file_url # 文件Url
            )
            # 发送富媒体消息
            await message._api.post_group_message(
            group_openid=message.group_openid,
            msg_type=7, #7表示富媒体类型
            msg_id=message.id,
            media=upload_media
            )
          #群端发送代api代码
        elif "搞笑文案" in message.content or "笑一笑" in message.content:
            url = "https://zj.v.api.aa1.cn/api/wenan-gaoxiao/?type=json"
            try:
                response = requests.get(url)
                response.raise_for_status()  # 检查请求是否成功
                res = json.loads(response.text)
                qinggan = res["msg"]
                messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0, 
                msg_id=message.id,
                content=qinggan)
            except requests.exceptions.RequestException as e:
                reply_message = "抱歉，巴迪对搞笑文案请求上限暂时无法获取，请明天再试。"
                messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0, 
                msg_id=message.id,
                content=reply_message)
            #群端发送ark37（需要有发送ark权限 如果没请删掉此部分代码）
        elif "百变图" in message.content:
            payload: Ark = Ark(
                template_id=37,
                kv=[
                    ArkKv(key="#METATITLE#", value="百变图"),
                    ArkKv(key="#PROMPT#", value="百变图每次进入刷新"),
                    ArkKv(key="#METACOVER#", value="https://api.lyiqk.cn/purelady?cdd6a546"),
                    ],
                    )
            messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=3, 
                msg_id=message.id,
                ark=payload)                
                
                #群端发送图片需要上传富文本资源，暂不介绍
        elif "菜单" in message.content or "功能" in message.content or "指令" in message.content:
            messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_id=message.id,
                content=f"\n叮叮叮~！ \n你好哇！(❤️ ω ❤️) \n当前指令有：\n搜图\n查头像(输入QQ号)\n百变图\n搞笑文案or笑一笑\n毒鸡汤or心灵鸡汤\n励志文案\n每日一言\n情感一言or伤感文案\n随机视频\n系统状态\n巴迪正在努力迭代更新中……")
                #上面菜单部分可自定义，只是示例
                
     #假如没有群权限，记得修改下面监听通道详细见官方文档
if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_guild_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents.default()
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], secret=test_config["secret"])