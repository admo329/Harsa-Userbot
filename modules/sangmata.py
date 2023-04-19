# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
• `{i}id`
    Balas Stiker untuk Mendapatkan Id-nya
    Balas Pengguna untuk Mendapatkan Id-nya
    Tanpa Membalas Anda Akan Mendapatkan Id Obrolan

• `{i}sg <reply to a user><username/id>`
    Dapatkan His Name History dari pengguna yang menjawab.
"""
import glob
import io
import os
from asyncio.exceptions import TimeoutError as AsyncTimeout

try:
    import cv2
except ImportError:
    cv2 = None

try:
    from htmlwebshot import WebShot
except ImportError:
    WebShot = None
from telethon.errors.rpcerrorlist import MessageTooLongError, YouBlockedUserError
from telethon.tl.types import (
    ChannelParticipantAdmin,
    ChannelParticipantsBots,
    DocumentAttributeVideo,
)

from Ayra.fns.tools import metadata, translate

from . import (
    HNDLR,
    LOGS,
    AyConfig,
    async_searcher,
    bash,
    check_filename,
    con,
    eor,
    fast_download,
    get_string,
)
from . import humanbytes as hb
from . import inline_mention, is_url_ok, mediainfo, ayra_cmd


@ayra_cmd(
    pattern="id( (.*)|$)",
    manager=True,
)
async def _(event):
    ayra = event
    match = event.pattern_match.group(1).strip()
    if match:
        try:
            ids = await event.client.parse_id(match)
        except Exception as er:
            return await event.eor(str(er))
        return await event.eor(
            f"**Chat ID:**  `{event.chat_id}`\n**User ID:**  `{ids}`"
        )
    data = f"**Current Chat ID:**  `{event.chat_id}`"
    if event.reply_to_msg_id:
        event = await event.get_reply_message()
        data += f"\n**From User ID:**  `{event.sender_id}`"
    if event.media:
        bot_api_file_id = event.file.id
        data += f"\n**Bot API File ID:**  `{bot_api_file_id}`"
    data += f"\n**Msg ID:**  `{event.id}`"
    await ayra.eor(data)


@ayra_cmd(
    pattern="sg( (.*)|$)",
)
async def lastname(steal):
    mat = steal.pattern_match.group(1).strip()
    if not steal.is_reply and not mat:
        return await steal.eor("`Balas Ke Pengguna/Berikan Username atau ID.`")
    if mat:
        try:
            user_id = await steal.client.parse_id(mat)
        except ValueError:
            user_id = mat
    message = await steal.get_reply_message()
    if message:
        user_id = message.sender.id
    chat = "@SangMata_BOT"
    id = f"{user_id}"
    lol = await steal.eor(get_string("com_1"))
    try:
        async with steal.client.conversation(chat) as conv:
            try:
                msg = await conv.send_message(id)
                response = await conv.get_response()
                respond = await conv.get_response()
                responds = await conv.get_response()
            except YouBlockedUserError:
                return await lol.edit("Buka Blokir @SangMata_BOT dan Coba Lagi.")
            if (
                (response and response.text == "No records found")
                or (respond and respond.text == "No records found")
                or (responds and responds.text == "No records found")
            ):
                await lol.edit("No records found for this user")
                await steal.client.delete_messages(conv.chat_id, [msg.id, response.id])
            elif response.text.startswith("🔗"):
                await lol.edit(respond.message)
                await lol.reply(responds.message)
            elif respond.text.startswith("🔗"):
                await lol.edit(response.message)
                await lol.reply(responds.message)
            else:
                await lol.edit(respond.message)
                await lol.reply(response.message)
            await steal.client.delete_messages(
                conv.chat_id,
                [msg.id, responds.id, respond.id, response.id],
            )
    except AsyncTimeout:
        await lol.edit("Error: @SangMata_BOT is not responding!.")