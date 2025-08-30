from pyrogram import Client
from pyrogram.errors import RPCError

from app.utils.helper import get_user_balance, format_user_reference
from app.utils.logger import error
from data.config import config, t


async def send_message(app: Client, message: str) -> None:
    if not config.CHANNEL_ID:
        return

    try:
        await app.send_message(config.CHANNEL_ID, message, disable_web_page_preview=True)
    except RPCError as ex:
        error(f'Failed to send notification: {str(ex)}')


async def send_notification(app: Client, gift_id: int, **kwargs) -> None:
    total_gifts = kwargs.get('total_gifts', 1)

    supply_text = ""
    if 'total_amount' in kwargs and kwargs['total_amount'] > 0:
        supply_text = f" | {t('telegram.available')}: {kwargs.get('total_amount')}"

    message_types = {
        'peer_id_error': lambda: t("telegram.peer_id_error"),
        'error_message': lambda: t("telegram.error_message", error=kwargs.get('error_message')),
        'balance_error': lambda: t("telegram.balance_error", gift_id=gift_id,
                                   gift_price=kwargs.get('gift_price', 0),
                                   current_balance=kwargs.get('current_balance', 0)),
        'range_error': lambda: t("telegram.range_error", gift_id=gift_id,
                                 price=kwargs.get('gift_price'),
                                 supply=kwargs.get('total_amount'),
                                 supply_text=supply_text),
        'success_message': lambda: t("telegram.success_message", current=kwargs.get('current_gift'), total=total_gifts,
                                     gift_id=gift_id, recipient='') +
                                   format_user_reference(kwargs.get('user_id'), kwargs.get('username'))
    }

    for key, value in kwargs.items():
        if value and key in message_types:
            await send_message(app, message_types[key]().strip())
            return


async def send_start_message(client: Client) -> None:
    balance = await get_user_balance(client)
    ranges_text = "\n".join([
        f"• {r['min_price']}-{r['max_price']} ⭐ (supply ≤ {r['supply_limit']}) x{r['quantity']}"
        for r in config.GIFT_RANGES
    ])

    message = t("telegram.start_message",
                language=config.language_display,
                locale=config.LANGUAGE,
                balance=balance,
                ranges=ranges_text)
    await send_message(client, message)


async def send_summary_message(app: Client, sold_out_count: int = 0,
                               non_limited_count: int = 0, non_upgradable_count: int = 0) -> None:
    if not config.CHANNEL_ID:
        return

    skip_types = {
        'sold_out_item': sold_out_count,
        'non_limited_item': non_limited_count,
        'non_upgradable_item': non_upgradable_count
    }

    summary_parts = [
        t(f"telegram.{skip_type}", count=count)
        for skip_type, count in skip_types.items()
        if count > 0
    ]

    if summary_parts:
        message = t("telegram.skip_summary_header") + "\n" + "\n".join(summary_parts)
        await send_message(app, message)
