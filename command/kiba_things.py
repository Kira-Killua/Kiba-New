from asyncio import CancelledError
from ctypes.wintypes import MSG
import re
from re import Match
import random
from nonebot import NoneBot
from .. import sv
from hoshino.service import sucmd
from hoshino.typing import CommandSession, CQEvent, MessageSegment, NoticeSession
from ..libraries.tool import random_uniform

    

kibahelp = sv.on_prefix(['kibathings', 'mykiba'])
select_things       = sv.on_prefix(['帮我选', 'select'])
eat_normal       = sv.on_prefix(['今天吃什么'])
eat_cx       = sv.on_prefix(['抽象吃什么'])
eat_thank       = sv.on_prefix(['吃什么作者'])
eat_all       = sv.on_prefix(['吃什么全览'])
poke = sv.on_notice('notify.poke')
rolling       = sv.on_prefix(['轮盘', 'roll'])
than = sv.on_prefix(['比大小', 'than'])

eatlist_cx=["绝赞烧烤","有蒸羊羔、蒸熊掌、蒸鹿尾儿、烧花鸭、烧雏鸡、烧子鹅，卤猪、卤鸭、酱鸡、腊肉、松花、小肚儿、晾肉、香肠儿，什锦苏盘儿、熏鸡白肚儿、清蒸八宝猪、江米酿鸭子，罐儿野鸡、罐儿鹌鹑、卤什件儿、卤子鹅、山鸡、兔脯、菜蟒、银鱼、清蒸哈士蟆！烩腰丝、烩鸭腰、烩鸭条、清蒸鸭丝儿。黄心管儿，焖白鳝、焖黄鳝、豆豉鲶鱼、锅烧鲤鱼、锅烧鲶鱼、清蒸甲鱼、抓炒鲤鱼、抓炒对虾、软炸里脊、软炸鸡！什锦套肠儿、麻酥油卷儿、卤煮寒鸦儿，熘鲜蘑、熘鱼脯、熘鱼肚、熘鱼骨、熘鱼片儿、醋熘肉片儿！烩三鲜儿、烩白蘑、烩全饤儿、烩鸽子蛋、炒虾仁儿、烩虾仁儿、烩腰花儿、烩海参、炒蹄筋儿、锅烧海参、锅烧白菜、炸开耳、炒田鸡，还有桂花翅子、清蒸翅子、炒飞禽、炸什件儿、清蒸江瑶柱。糖熘芡实米，拌鸡丝、拌肚丝、什锦豆腐、什锦丁儿，糟鸭、糟蟹、糟鱼、糟熘鱼片、熘蟹肉、炒蟹肉、清拌蟹肉，蒸南瓜、酿倭瓜、炒丝瓜、酿冬瓜、焖鸡掌儿、焖鸭掌儿、焖笋、烩茭白，茄干晒炉肉、鸭羹、蟹肉羹、三鲜木樨汤！还有红丸子、白丸子、熘丸子、炸丸子、南煎丸子、苜蓿丸子、三鲜丸子、四喜丸子、鲜虾丸子、鱼脯丸子、饹炸丸子、豆腐丸子、汆丸子！一品肉、樱桃肉、马牙肉、红焖肉、黄焖肉、坛子肉。烀肉、扣肉、松肉、罐儿肉、烧肉、大肉、白肉、酱豆腐肉！红肘子、白肘子、水晶肘子、蜜蜡肘子、酱豆腐肘子、扒肘子！炖羊肉、烧羊肉、烤羊肉、煨羊肉、涮羊肉、五香羊肉、爆羊肉，汆三样儿、爆三样儿、烩银丝、烩散丹、熘白杂碎、三鲜鱼翅、栗子鸡、煎汆活鲤鱼、板鸭、筒子鸡！","24分交互","凑豆腐配腐掳，美食界中的博主。不管是腥还是臭，到我嘴里就是肉。奥利给，干了兄弟们！","吃我一拳","昏睡红茶","水馒头","会员制餐厅","星星","迪拉熊刺身","奥利给","苍月","滴蜡熊","touch","星星","绝赞","生嗑源石","真理医生的粉笔头","92号汽油","dio的小面包","小孩火锅","极犽鞭汤"]
eatlist_normal = ["手擀面","锅包肉","烤串","炒粉","炒饭","汉堡","炸鸡","关东煮","牛肉饭","煲仔饭","蛋糕","章鱼小丸子","食堂","烤肉拌饭","烤面筋","锅包又","饭包","香辣鸡腿堡","麻辣烫","鲜肉馄饨","小笼包","猪肘饭","卤肉饭","辣子鸡","手撕鸡","鸭腿饭","煎饼果子","酱肘子","辣子鸡盖饭","KFC蜜汁全鸡","关东煮","可乐鸡翅","炒河粉","自选盒饭","鹅饭儿","五爷拌面","米村拌饭","阿卜杜烤肉","隐厨","米村拌饭","辣条","川香麻辣面","蛋炒饭","螺蛳粉","萨莉亚","必胜客","麦当劳","肯德基","汉堡王","德克士","必胜客","DQ","蜜雪冰城","老菜坊","法式焗蜗牛","🍟薯条","炒米粉","饭团","麦麦脆汁鸡","回锅肉","饺砸","奶油号角","千层面","拿破仑蛋糕","歌剧院蛋糕"]

@kibahelp
async def _(bot: NoneBot, ev: CQEvent):
    await bot.send(ev, "Kiba 模块帮助:\n帮我选 <选项1> <选项2>...... -> 帮你选择一个选项。有概率不选\n今天/抽象吃什么 -> 展示今天食物菜单 & 抽象菜单\n吃什么作者 -> 显示提供菜谱的所有贡献者\n吃什么全览 -> 提供全部食品 & 抽象类。\n轮盘 <选项1> <选项1占比> <选项2> <选项2占比>...... -> 轮盘帮选。\n比大小 <0-100之间数字> -> 与我随机到的数字比大小！", at_sender=True)
    
@select_things
async def _(bot: NoneBot, ev: CQEvent):
    argv = str(ev.message.extract_plain_text()).strip().split(" ")
    xnmb = random.randint(0,20)
    if len(argv) == 1:
        await bot.send(ev, "▿ 参数不足\n选你🐎。", at_sender=True)
        return
    elif len(argv) is not None:
        if xnmb == 1:
            await bot.send(ev, "▾ 帮选\n选你🐎，自己选去。", at_sender=True)
            return
        elif xnmb == 19:
            await bot.send(ev, "▾ 帮选\n你这选项没一个我中意的，都不选。", at_sender=True)
            return
        elif xnmb == 20:
            await bot.send(ev, "▾ 帮选\n小孩子才做选择，成年人...我都要！", at_sender=True)
            return
        else:
            result = random.randint(0, len(argv) - 1)
            selectresponce = ['天气看着还行','摸了一下自己的尾巴','护目镜掉下去了','圣剑在发光','滴蜡熊的指引','纱露朵小姐的建议']
            await bot.send(ev, f"▾ 帮选\n因为{selectresponce[random.randint(0,5)]}，所以我选 {argv[result]}。", at_sender=True)
            return
    else:
        await bot.send(ev, "▿ 帮选 - 无参数\n选你🐎。", at_sender=True)
        return
    
@eat_normal
async def _(bot: NoneBot, ev: CQEvent):
    breakfast = eatlist_normal[random.randint(0,64)]
    lunch = eatlist_normal[random.randint(0,64)]
    dinner = eatlist_normal[random.randint(0,64)]
    await bot.send(ev, f"▾ 吃什么 2.0\n早餐: {breakfast}\n午餐: {lunch}\n晚餐: {dinner}\n=========\n要寻找其他的吃什么系列指令？\n抽象版：“抽象吃什么”\n全览：“吃什么全览”\n贡献者:“吃什么作者”", at_sender=True)
    
@eat_cx
async def _(bot: NoneBot, ev: CQEvent):
    cx = eatlist_cx[random.randint(0,20)]
    await bot.send(ev, f"▾ 吃什么抽象版 2.0\n您今天的抽象食物是：{cx}", at_sender=True)

@eat_thank
async def _(bot: NoneBot, ev: CQEvent):
    await bot.send(ev, f"▾ 吃什么 2.0 食谱贡献者\n排名不分先后：\nくれる雨ちゃん、Иɒ²Hə、🎵Shiokuya yukine⭐、琦冥血樱、24K纯狼、战术女仆三好、科均菌、zilwitch、天下無双魂音泉、微风wind、YelRivi、Pedigree、_天外飞雪、不是很懂坐忘道、苍月、镭爆、CastWell、Rolan、熊叶、Calf、祭璃、霜影丶Frostwolf、小航、渊琼、Jerry", at_sender=True)
    
@eat_all
async def _(bot: NoneBot, ev: CQEvent):
    await bot.send(ev, f"▾ 吃什么 2.0\n目前收录的正常食谱有:{eatlist_normal}\n 目前收录的抽象食谱有:{eatlist_cx}", at_sender=True)

self_id = 3400972434    #这里的id需要自行更改一下！未来会改到从Hoshino处获取。
@poke
async def _(session: NoticeSession):
    value = (session.ctx['target_id'] == int(self_id))
    if value == False:
        return
    r = random.randint(1, 20)
    if r == 2:
        await session.send("* 但是他拒绝了。")
    elif r == 3:
        await session.send("闲的没事的话.....那你再戳戳吧。")
    elif r == 4:
        await session.send("不要再戳了啦，真是的！~")
    elif r == 5:
        await session.send("传送功能启动......带你去一个全是福瑞的地方然后他们追着让你跑起来？开玩笑的。")
    elif r <= 7 and r > 5:
        await session.send("难道要一直戳下去想看我说些什么吗？噫，怎么这么无聊。")
    elif r <= 12 and r > 7:
        await session.send("不可以戳我，唔~！")
    elif r <= 17 and r > 12:
        await session.send(f'福瑞也是有脾气的，不理你了。')
    elif r <= 19 and r > 17:
        await session.send("我灵敏的躲开了~")
    elif r == 1:
        await session.send('不许戳了不许戳了...干什么嘛，你是福瑞控？')
        
@rolling
async def _(bot: NoneBot, ev: CQEvent):
    argv = str(ev.message.extract_plain_text()).strip().split(" ")
    roll = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z AA AB AC AD AE AF AG AH AI AJ AK AL AM AN AO AP AQ AR AS AT AU AV AW AX AY AZ'.split(' ')
    rollnum = 0
    sum = 0
    total = 0
    las = []
    rani = 0
    msg = f'▾ 轮盘'
    if len(argv) % 2 != 0:
        await bot.send(ev, f"▿ 轮盘\n请注意格式：\n轮盘 <选项A> <A占比> <选项B> <B占比>......\n注意：所有选项占比的和必须等于 100。要求占比必须是整数，要不然...骂你嗷。",at_sender=True)
        return
    try:
        for i in range(len(argv)):
            if i % 2 == 0:
                continue
            rollnum += 1
            sum += int(argv[i])
    except Exception as e:
        await bot.send(ev,f"▿ 轮盘\n....您输入的概率确定是整数还是**粗口**的其他语言？\n[Exception Occurred]\n{e}",at_sender=True)
        return
    if sum != 100:
        await bot.send(ev,f"▿ 轮盘\n注意：所有选项占比的和必须等于 100。",at_sender=True)
        return
    else:
        if rollnum > 52:
            await bot.send(ev,f"▿ 轮盘\n注意：您超出了52个选项，不支持过多选项。",at_sender=True)
            return
        else:
            rollnum = 0
        for i in range(len(argv)):
            if i % 2 != 0:
                continue
            msg += f'\n{roll[rollnum]}: {argv[i]}, 占比: {argv[i + 1]}% ({total + 1} -'
            for j in range(int(argv[i + 1])):
                total += 1
            las.append(total)
            msg += f' {total})'
            rollnum += 1
        ran = random.randint(1,100)
        for i in range(len(argv)):
            if i % 2 != 0:
                continue
            if i == 0:
                if ran <= las[rani]:
                    ran_select = i
            else:
                if rani + 1 == len(las) and ran > int(las[rani - 1]):
                    ran_select = i
                else:
                    if ran > int(las[rani - 1]) and ran <= int(las[rani + 1]):
                        ran_select = i
            rani += 1
    msg += f'\n随机数是 {ran}，所以随机到的选项是: {argv[ran_select]}。\n注意：轮盘的算法并不完全公平分配。结果仅用于参考。'
    await bot.send(ev,msg,at_sender=True)

@than
async def _(bot: NoneBot, ev: CQEvent):
    argv = str(ev.message.extract_plain_text()).strip().split(" ")[0]
    try:
        if float(argv)>100 or float(argv)<0:
            await bot.finish(ev, "▿ 比大小\n目前还请在0-100以内作比较啦！（恼）")
        else:
            msg = "▾ 比大小\n"
            if float(argv)==100:
                msg += "嘿，我想，这是要赌我会不会出100吗？那就来试试好了~！\n"
                num = float('%.2f'% random_uniform(99,101))
            elif float(argv)==0:
                msg += "不走程序就想战败！！？不行，给你一个五五开的机会......\n"
                num = float('%.2f'% random_uniform(-1,1))
            else:
                num = float('%.2f'% random_uniform(0,100))
            msg += f"你发的数字是..{argv}。很有趣的数字。那我想到的数字是{num}！"
            if num> float(argv):
                msg += "看起来是我赢了，别灰心，再试试？"
            elif num == float(argv):
                msg += "心有灵犀哈......这局是平局了~！"
            else:
                msg += "哎呀......你赢了！恭喜你啦！"
            await bot.finish(ev, msg)
    except ValueError:
        await bot.finish(ev, f"▿ 比大小\n你输入了什么..?要被玩坏了啊！")