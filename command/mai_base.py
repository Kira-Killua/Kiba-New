import random
from re import Match

from nonebot import NoneBot
from PIL import Image

from hoshino.service import sucmd
from hoshino.typing import CommandSession, CQEvent, MessageSegment

from .. import BOTNAME, Root, log, sv
from ..libraries.image import image_to_base64
from ..libraries.maimaidx_api_data import maiApi
from ..libraries.maimaidx_error import UserDisabledQueryError, UserNotFoundError
from ..libraries.maimaidx_model import UserInfo
from ..libraries.maimaidx_music import mai
from ..libraries.maimaidx_music_info import draw_music_info
from ..libraries.maimaidx_player_score import rating_ranking_data
from ..libraries.tool import hash

update_data         = sucmd('updatedata', aliases=('更新maimai数据'))
maimaidxhelp        = sv.on_fullmatch(['帮助maimaiDX', '帮助maimaidx'])
maimaidxrepo        = sv.on_fullmatch(['项目地址maimaiDX', '项目地址maimaidx'])
mai_today           = sv.on_prefix(['今日mai', '今日舞萌', '今日运势'])
mai_what            = sv.on_rex(r'.*mai.*什么(.+)?')
random_song         = sv.on_rex(r'^[来随给]个((?:dx|sd|标准))?([绿黄红紫白]?)([0-9]+\+?)$')
rating_ranking      = sv.on_prefix(['查看排名', '查看排行'])
data_update_daily   = sv.scheduled_job('cron', hour='4')


@update_data
async def _(session: CommandSession):
    await mai.get_music()
    await mai.get_music_alias()
    await session.send('▼ 更新完成\n舞萌数据更新完成！')


@maimaidxhelp
async def _(bot: NoneBot, ev: CQEvent):
    await bot.send(ev, MessageSegment.image(image_to_base64(Image.open((Root / 'maimaidxhelp.png')))), at_sender=True)


@maimaidxrepo
async def _(bot: NoneBot, ev: CQEvent):
    await bot.send(ev, f'关于KibaBot New，采用的基础项目为 Yuri-YuzuChaN 的 maimaiDX 项目。\n其Repo是：https://github.com/Yuri-YuzuChaN/maimaiDX', at_sender=True)

    
@mai_today
async def _(bot: NoneBot, ev: CQEvent):
    wm_list = ['拼机', '推分', '越级', '下埋', '夜勤', '练底力', '练手法', '打旧框', '干饭', '抓绝赞', '收歌']
    uid = ev.user_id
    h = hash(uid)
    rp = h % 100
    wm_value = []
    for i in range(11):
        wm_value.append(h & 3)
        h >>= 2
    msg = f'▼ 今日运势 Basic\n人品值：{rp}\n'
    for i in range(11):
        if wm_value[i] == 3:
            msg += f'宜 {wm_list[i]}\n'
        elif wm_value[i] == 0:
            msg += f'忌 {wm_list[i]}\n'
    music = mai.total_list[h % len(mai.total_list)]
    ds = '/'.join([str(_) for _ in music.ds])
    msg += f'========\n今日推荐：\n'
    msg += f'🎵 {music.id} \n {music.title}'
    msg += MessageSegment.image(image_to_base64(Image.open(await maiApi.download_music_pictrue(music.id))))
    msg += ds
    await bot.send(ev, msg, at_sender=True)


@mai_what
async def _(bot: NoneBot, ev: CQEvent):
    match: Match[str] = ev['match']
    music = mai.total_list.random()
    user = None
    if (point := match.group(1)) and ('推分' in point or '上分' in point or '加分' in point):
        try:
            obj = await maiApi.query_user('player', qqid=ev.user_id)
            user = UserInfo(**obj)
            r = random.randint(0, 1)
            _ra = 0
            ignore = []
            if r == 0:
                if sd := user.charts.sd:
                    ignore = [m.song_id for m in sd if m.achievements < 100.5]
                    _ra = sd[-1].ra
            else:
                if dx := user.charts.dx:
                    ignore = [m.song_id for m in dx if m.achievements < 100.5]
                    _ra = dx[-1].ra
            if _ra != 0:
                ds = round(_ra / 22.4, 1)
                musiclist = mai.total_list.filter(ds=(ds, ds + 1))
                for _m in musiclist:
                    if int(_m.id) in ignore:
                        musiclist.remove(_m)
                music = musiclist.random()
        except UserNotFoundError:
            pass
        except UserDisabledQueryError:
            pass
    await bot.send(ev, await draw_music_info(music, ev.user_id, user))


@random_song
async def _(bot: NoneBot, ev: CQEvent):
    try:
        match: Match[str] = ev['match']
        diff = match.group(1)
        if diff == 'dx':
            tp = ['DX']
        elif diff == 'sd' or diff == '标准':
            tp = ['SD']
        else:
            tp = ['SD', 'DX']
        level = match.group(3)
        if match.group(2) == '':
            music_data = mai.total_list.filter(level=level, type=tp)
        else:
            music_data = mai.total_list.filter(level=level, diff=['绿黄红紫白'.index(match.group(2))], type=tp)
        if len(music_data) == 0:
            msg = '▼ 请注意\n没有这样的乐曲哦。检查一下啦。'
        else:
            msg = await draw_music_info(music_data.random(), ev.user_id)
        await bot.send(ev, msg, at_sender=True)
    except:
        await bot.send(ev, '▼ 请注意\n随机命令错误，请检查语法......', at_sender=True)
        
        
@rating_ranking
async def _(bot: NoneBot, ev: CQEvent):
    args: str = ev.message.extract_plain_text().strip()
    page = 1
    name = ''
    if args.isdigit():
        page = int(args)
    else:
        name = args.lower()
    
    data = await rating_ranking_data(name, page)
    await bot.send(ev, data, at_sender=True)


@data_update_daily
async def _():
    await mai.get_music()
    mai.guess()
    log.info('舞萌数据更新完毕！')
