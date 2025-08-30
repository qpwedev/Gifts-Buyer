import asyncio
from typing import Dict, Any

from pyrogram import Client

from app.notifications import send_notification
from app.purchase import buy_gift
from app.utils.logger import warn
from data.config import config, t


class GiftFilter:
    @staticmethod
    async def is_eligible(gift_data: Dict[str, Any]) -> tuple[bool, Dict[str, Any]]:
        gift_price = gift_data.get("price", 0)
        is_limited = gift_data.get("is_limited", False)
        is_sold_out = gift_data.get("is_sold_out", False)
        is_upgradable = "upgrade_price" in gift_data
        total_amount = gift_data.get("total_amount", 0) if is_limited else 0

        validation_rules = {
            'sold_out': {
                'condition': is_sold_out,
                'return_data': {}
            },
            'non_limited': {
                'condition': not is_limited and not config.PURCHASE_NON_LIMITED_GIFTS,
                'return_data': {}
            },
            'non_upgradable': {
                'condition': config.PURCHASE_ONLY_UPGRADABLE_GIFTS and not is_upgradable,
                'return_data': {}
            }
        }

        for rule in validation_rules.values():
            if rule['condition']:
                return False, rule['return_data']

        range_matched, quantity = config.get_matching_range(gift_price, total_amount)
        # if not range_matched:
        #     return False, {
        #         "range_error": True,
        #         "gift_price": gift_price,
        #         "total_amount": total_amount
        #     }

        return True, {"quantity": quantity}


async def new_callback(app: Client, gift_data: Dict[str, Any]) -> None:
    gift_id = gift_data.get("id")
    is_eligible, notification_kwargs = await GiftFilter.is_eligible(gift_data)

    if not is_eligible:
        if notification_kwargs:
            await send_notification(app, gift_id, **notification_kwargs)
        return

    quantity = notification_kwargs.get("quantity", 1)

    for user_id in config.USER_ID:
        try:
            await buy_gift(app, user_id, gift_id, quantity)
        except Exception as ex:
            warn(t("console.purchase_error", gift_id=gift_id, chat_id=user_id))
            await send_notification(app, gift_id, error_message=str(ex))
        await asyncio.sleep(0.5)
