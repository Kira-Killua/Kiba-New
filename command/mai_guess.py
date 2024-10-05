import asyncio

from nonebot import NoneBot

from hoshino.service import priv
from hoshino.typing import CQEvent, MessageSegment

from .. import sv
from ..libraries.maimaidx_music import guess
from ..libraries.maimaidx_music_info import draw_music_info

guess_music_start   = sv.on_fullmatch('猜歌')
guess_music_pic     = sv.on_fullmatch('猜曲绘')
guess_music_reset   = sv.on_fullmatch('重置猜歌')
guess_music_switch  = sv.on_suffix('mai猜歌')


@sv.on_fullmatch('猜歌')
async def guess_music(bot: NoneBot, ev: CQEvent):
    gid = str(ev.group_id)
    if ev.group_id not in guess.config['enable']:
        await bot.finish(ev, '▼ 请注意\n管理员已关闭本群的猜歌功能......若要开启，请输入 "开启mai猜歌" 指令。')
    if gid in guess.Group:
        await bot.finish(ev, '▼ 请注意\n该群已有正在进行的猜歌或猜曲绘，先来参与一下呀？')
    await guess.start(gid)
    await bot.send(ev, '▼ 猜歌\n我将从热门乐曲中选择一首歌，每隔8秒描述它的特征，请输入歌曲的 id 标题 或 别名（需bot支持，无需大小写） 进行猜歌（DX乐谱和标准乐谱视为两首歌）。猜歌时查歌等其他命令依然可用。')
    await asyncio.sleep(4)
    for cycle in range(7):
        if ev.group_id not in guess.config['enable'] or gid not in guess.Group or guess.Group[gid].end:
            break
        if cycle < 6:
            await bot.send(ev, f'▼ 提示 {cycle + 1}/7\n这首歌{guess.Group[gid].options[cycle]}')
            await asyncio.sleep(8)
        else:
            await bot.send(ev, f'''▼ 提示 7/7\n 这首歌封面的一部分是：\n{MessageSegment.image(guess.Group[gid].img)}答案将在30秒后揭晓。''')
            for _ in range(30):
                await asyncio.sleep(1)
                if gid in guess.Group:
                    if ev.group_id not in guess.config['enable'] or guess.Group[gid].end:
                        return
                else:
                    return
            guess.Group[gid].end = True
            answer = f'''▼ 猜歌答案\n答案是：\n{await draw_music_info(guess.Group[gid].music)}'''
            guess.end(gid)
            await bot.send(ev, answer)


@sv.on_fullmatch('猜曲绘')
async def guess_music_pic(bot: NoneBot, ev: CQEvent):
    gid = str(ev.group_id)
    if ev.group_id not in guess.config['enable']:
        await bot.finish(ev, '▼ 请注意\n管理员已关闭本群的猜歌功能......若要开启，请输入 "开启mai猜歌" 指令。')
    if gid in guess.Group:
        await bot.finish(ev, '▼ 请注意\n该群已有正在进行的猜歌或猜曲绘，先来参与一下呀？')
    await guess.startpic(gid)
    await bot.send(ev, f'▼ 猜曲绘\n以下裁切图片是哪首谱面的曲绘：\n{MessageSegment.image(guess.Group[gid].img)}请在30s内输入答案。')
    for _ in range(30):
        await asyncio.sleep(1)
        if gid in guess.Group:
            if ev.group_id not in guess.config['enable'] or guess.Group[gid].end:
                return
        else:
            return
    guess.Group[gid].end = True
    answer = f'''▼ 猜曲绘答案\n答案是：\n{await draw_music_info(guess.Group[gid].music)}'''
    guess.end(gid)
    await bot.send(ev, answer)


@sv.on_message()
async def guess_music_solve(bot: NoneBot, ev: CQEvent):
    gid = str(ev.group_id)
    if gid not in guess.Group:
        return
    ans: str = ev.message.extract_plain_text().strip().lower()
    if ans.lower() in guess.Group[gid].answer:
        guess.Group[gid].end = True
        answer = f'''▼ 答案正确！\n恭喜你猜对了，答案是：\n{await draw_music_info(guess.Group[gid].music)}'''
        guess.end(gid)
        await bot.send(ev, answer, at_sender=True)


@sv.on_fullmatch('重置猜歌')
async def reset_guess(bot: NoneBot, ev: CQEvent):
    gid = str(ev.group_id)
    if not priv.check_priv(ev, priv.ADMIN):
        msg = '▼ 请注意\n仅允许管理员重置。请联系管理员进行重置操作。'
    elif gid in guess.Group:
        msg = '▼ 猜歌状态重置\n已重置该群猜歌'
        guess.end(gid)
    else:
        msg = '▼ 请注意\n该群未处在猜歌状态'
    await bot.send(ev, msg)


@sv.on_suffix('mai猜歌')
async def guess_on_off(bot: NoneBot, ev: CQEvent):
    gid = ev.group_id
    args: str = ev.message.extract_plain_text().strip()
    if not priv.check_priv(ev, priv.ADMIN):
        msg = '▼ 请注意\n仅允许管理员进行操作，请联系管理员。'
    elif args == '开启':
        msg = await guess.on(gid)
    elif args == '关闭':
        msg = await guess.off(gid)
    else:
        msg = '▼ 请注意\n指令错误，请检查指令。'
    await bot.send(ev, msg, at_sender=True)