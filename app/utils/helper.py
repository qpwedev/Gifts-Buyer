from typing import Optional, Tuple

from pyrogram import Client


async def get_user_balance(client: Client) -> int:
    try:
        return await client.get_stars_balance()
    except Exception:
        return 0


async def get_recipient_info(app: Client, chat_id: int) -> Tuple[str, str]:
    try:
        user = await app.get_chat(chat_id)
        username = user.username or ""

        recipient_info = (
            f"@{username.strip()}" if username
            else f"{chat_id}" if isinstance(chat_id, int) or str(chat_id).isdigit()
            else f"@{chat_id}"
        )

        return recipient_info, username
    except Exception:
        return str(chat_id), ""


def format_user_reference(user_id: int, username: Optional[str] = None) -> str:
    if username:
        return f"@{username} | <code>{user_id}</code>"

    if isinstance(user_id, int) or (isinstance(user_id, str) and user_id.isdigit()):
        return f'<a href="tg://user?id={user_id}">{user_id}</a>'

    return f"@{user_id}" if isinstance(user_id, str) else str(user_id)
