import re
from textwrap import dedent

from nonebot import NoneBot

from hoshino.typing import CQEvent, MessageSegment

from .. import sv
from ..libraries.image import image_to_base64, text_to_image
from ..libraries.maimai_best_50 import generate
from ..libraries.maimaidx_music import mai
from ..libraries.maimaidx_music_info import music_play_data
from ..libraries.maimaidx_player_score import music_global_data

best50  = sv.on_prefix(['b50', 'B50'])
minfo   = sv.on_prefix(['minfo', 'Minfo', 'MINFO', 'info', 'Info', 'INFO'])
ginfo   = sv.on_prefix(['ginfo', 'Ginfo', 'GINFO'])
score   = sv.on_prefix(['分数线'])


@best50
async def _(bot: NoneBot, ev: CQEvent):
    qqid = ev.user_id
    username: str = ev.message.extract_plain_text().strip()
    await bot.send(ev, "▼ Best 50 Generating\n正在根据水鱼数据生成 Best，请耐心等待我的回复~！一般这需要1分钟。请注意游玩数据仅供参考喔。", at_sender=True)
    for i in ev.message:
        if i.type == 'at' and i.data['qq'] != 'all':
            qqid = int(i.data['qq'])
    await bot.send(ev, await generate(qqid, username), at_sender=True)
    
    
@minfo
async def _(bot: NoneBot, ev: CQEvent):
    qqid = ev.user_id
    args: str = ev.message.extract_plain_text().strip().lower()
    for i in ev.message:
        if i.type == 'at' and i.data['qq'] != 'all':
            qqid = int(i.data['qq'])
    if not args:
        await bot.finish(ev, '▼ 请注意\n请输入曲目ID或曲名。', at_sender=True)

    if mai.total_list.by_id(args):
        songs = args
    elif by_t := mai.total_list.by_title(args):
        songs = by_t.id
    else:
        alias = mai.total_alias_list.by_alias(args)
        if not alias:
            await bot.finish(ev, '▼ 请注意\n我没有找到曲目。', at_sender=True)
        elif len(alias) != 1:
            msg = f'▼ 曲名相同\n找到相同别名的曲目，请使用以下ID查询：\n'
            for songs in alias:
                msg += f'{songs.SongID}：{songs.Name}\n'
            await bot.finish(ev, msg.strip(), at_sender=True)
        else:
            songs = str(alias[0].SongID)
    pic = await music_play_data(qqid, songs)
    await bot.send(ev, pic, at_sender=True)


@ginfo
async def _(bot: NoneBot, ev: CQEvent):
    args: str = ev.message.extract_plain_text().strip().lower()
    if not args:
        await bot.finish(ev, '▼ 请注意\n请输入曲目ID或曲名。', at_sender=True)
    if args[0] not in '绿黄红紫白':
        level_index = 3
    else:
        level_index = '绿黄红紫白'.index(args[0])
        args = args[1:].strip()
        if not args:
            await bot.finish(ev, '▼ 请注意\n请输入曲目ID或曲名。', at_sender=True)
    if mai.total_list.by_id(args):
        id = args
    elif by_t := mai.total_list.by_title(args):
        id = by_t.id
    else:
        alias = mai.total_alias_list.by_alias(args)
        if not alias:
            await bot.finish(ev, '▼ 请注意\n我没有找到曲目。', at_sender=True)
        elif len(alias) != 1:
            msg = f'▼ 曲名相同\n找到相同别名的曲目，请使用以下ID查询：\n'
            for songs in alias:
                msg += f'{songs.SongID}：{songs.Name}\n'
            await bot.finish(ev, msg.strip(), at_sender=True)
        else:
            id = str(alias[0].SongID)
    music = mai.total_list.by_id(id)
    if not music.stats:
        await bot.finish(ev, '▼ 请注意\n该乐曲还没有统计信息', at_sender=True)
    if len(music.ds) == 4 and level_index == 4:
        await bot.finish(ev, '▼ 请注意\n该乐曲没有这个等级', at_sender=True)
    if not music.stats[level_index]:
        await bot.finish(ev, '▼ 请注意\n该等级没有统计信息', at_sender=True)
    stats = music.stats[level_index]
    info = dedent(f'''\▼ 谱面游玩情况
            游玩次数：{round(stats.cnt)}
            拟合难度：{stats.fit_diff:.2f}
            平均达成率：{stats.avg:.2f}%
            平均 DX 分数：{stats.avg_dx:.1f}
            谱面成绩标准差：{stats.std_dev:.2f}''')
    await bot.send(ev, await music_global_data(music, level_index) + info, at_sender=True)
    
    
@score
async def _(bot: NoneBot, ev: CQEvent):
    args: str = ev.message.extract_plain_text().strip()
    pro = args.split()
    if len(pro) == 1 and pro[0] == '帮助':
        msg = dedent('''此功能为查找某首歌分数线设计。
                    命令格式：分数线 <难度+歌曲id> <分数线>
                    例如：分数线 紫799 100
                    命令将返回分数线允许的 TAP GREAT 容错以及 BREAK 50落等价的 TAP GREAT 数。
                    以下为 TAP GREAT 的对应表：
                    GREAT/GOOD/MISS
                    TAP\t1/2.5/5
                    HOLD\t2/5/10
                    SLIDE\t3/7.5/15
                    TOUCH\t1/2.5/5
                    BREAK\t5/12.5/25(外加200落)''')
        await bot.send(ev, MessageSegment.image(image_to_base64(text_to_image(msg))), at_sender=True)
    else:
        try:
            result = re.search(r'([绿黄红紫白])\s?([0-9]+)', args)
            level_labels = ['绿', '黄', '红', '紫', '白']
            level_labels2 = ['Basic', 'Advanced', 'Expert', 'Master', 'Re:MASTER']
            level_index = level_labels.index(result.group(1))
            chart_id = result.group(2)
            line = float(pro[-1])
            music = mai.total_list.by_id(chart_id)
            chart = music.charts[level_index]
            tap = int(chart.notes.tap)
            slide = int(chart.notes.slide)
            hold = int(chart.notes.hold)
            touch = int(chart.notes.touch) if len(chart.notes) == 5 else 0
            brk = int(chart.notes.brk)
            total_score = tap * 500 + slide * 1500 + hold * 1000 + touch * 500 + brk * 2500
            break_bonus = 0.01 / brk
            break_50_reduce = total_score * break_bonus / 4
            reduce = 101 - line
            if reduce <= 0 or reduce >= 101:
                raise ValueError
            msg = f'''▾ 分数线
设置的达成率为{line}%，其 Note 损失参照如下:
----------------------
此表格遵循的格式为:
类型 | ACHV.损失/个 | 最多损失数
----------------------
Great 评价:
Tap & Touch | {10000 / total_score:.4f}% | {(total_score * reduce / 10000):.2f}
Hold | {(10000 / total_score)* 2:.4f}% | {((total_score * reduce / 10000)/ 2):.2f}
Slide | {(10000 / total_score)* 3:.4f}% | {((total_score * reduce / 10000)/ 3):.2f}
Good 评价:
Tap & Touch | {(10000 / total_score)* 2.5:.4f}% | {((total_score * reduce / 10000)/ 2.5):.2f}
Hold | {(10000 / total_score)* 5:.4f}% | {((total_score * reduce / 10000)/ 5):.2f}
Slide | {(10000 / total_score)* 7.5:.4f}% | {((total_score * reduce / 10000)/ 7.5):.2f}
Miss 评价:
Tap & Touch | {(10000 / total_score)*5:.4f}% | {((total_score * reduce / 10000)/5):.2f}
Hold | {(10000 / total_score)* 10:.4f}% | {((total_score * reduce / 10000)/ 10):.2f}
Slide | {(10000 / total_score)* 15:.4f}% | {((total_score * reduce / 10000)/ 15):.2f}

Break 各评价损失:
注意: Break 的 Great 与 Perfect 评价都有细分等级，此表格的 Break Great 不做细分，仅为大约数供您参考。
本谱面每个 Break Perfect 2600 的达成率是 {((10000 / total_score) * 25 + (break_50_reduce / total_score * 100)* 4):.4f}%,谱面共 {brk} 个 Break，其占总体达成率的 {(((10000 / total_score) * 25 + (break_50_reduce / total_score * 100)* 4)* brk):.4f}%。
----------------------
此表格遵循的格式为:
类型 | ACHV.损失/个 | Tap Great 等价数
----------------------
Perfect 2550 | {break_50_reduce / total_score * 100:.4f}% | {(break_50_reduce / 100):.3f}
Perfect 2500 | {(break_50_reduce / total_score * 100)* 2:.4f}% | {(break_50_reduce / 100)* 2:.3f}
Great | ≈{((10000 / total_score) * 5 + (break_50_reduce / total_score * 100)* 4):.4f}% | ≈{5 + (break_50_reduce / 100)* 4:.3f}
Good | {((10000 / total_score) * 12.5 + (break_50_reduce / total_score * 100)* 4):.4f}% | {12.5 + (break_50_reduce / 100)* 4:.3f}
Miss | {((10000 / total_score) * 25 + (break_50_reduce / total_score * 100)* 4):.4f}% | {25 + (break_50_reduce / 100)* 4:.3f}'''
            await bot.send(ev, msg, at_sender=True)
        except Exception as e:
            await bot.send(ev, f'▼ 请注意\n格式错误，输入“分数线 帮助”以查看帮助信息。Exception:{e}', at_sender=True)