import configparser
import sys
from pathlib import Path
from typing import List, Union, Dict

from app.utils.localization import localization
from app.utils.logger import error


class Config:
    def __init__(self):
        self.parser = configparser.ConfigParser()
        self._load_config()
        self._setup_paths()
        self._setup_properties()
        self._validate()
        localization.set_locale(self.LANGUAGE)

    def _load_config(self) -> None:
        config_file = Path('config.ini')
        if not config_file.exists():
            error("Configuration file 'config.ini' not found!")
            sys.exit(1)
        self.parser.read(config_file, encoding='utf-8')

    def _setup_paths(self) -> None:
        base_dir = Path(__file__).parent
        self.SESSION = str(base_dir.parent / "data/account")
        self.DATA_FILEPATH = base_dir / "json/history.json"

    def _setup_properties(self) -> None:
        self.API_ID = self.parser.getint('Telegram', 'API_ID', fallback=0)
        self.API_HASH = self.parser.get('Telegram', 'API_HASH', fallback='')
        self.PHONE_NUMBER = self.parser.get('Telegram', 'PHONE_NUMBER', fallback='')
        self.CHANNEL_ID = self._parse_channel_id()

        self.INTERVAL = self.parser.getfloat('Bot', 'INTERVAL', fallback=15.0)
        self.LANGUAGE = self.parser.get('Bot', 'LANGUAGE', fallback='EN').lower()

        self.USER_ID = self._parse_recipients()
        self.GIFT_RANGES = self._parse_gift_ranges()
        self.PURCHASE_NON_LIMITED_GIFTS = self.parser.getboolean('Gifts', 'PURCHASE_NON_LIMITED_GIFTS', fallback=False)
        self.PURCHASE_ONLY_UPGRADABLE_GIFTS = self.parser.getboolean('Gifts', 'PURCHASE_ONLY_UPGRADABLE_GIFTS',
                                                                     fallback=False)
        self.PRIORITIZE_LOW_SUPPLY = self.parser.getboolean('Gifts', 'PRIORITIZE_LOW_SUPPLY', fallback=False)

    def _parse_channel_id(self) -> Union[int, str, None]:
        channel_value = self.parser.get('Telegram', 'CHANNEL_ID', fallback='').strip()

        channel_validators = {
            'empty_or_default': lambda val: not val or val == '-100',
            'username_with_at': lambda val: val.startswith('@'),
            'numeric_id': lambda val: val.isdigit(),
            'username_without_at': lambda val: val and not val.startswith('@') and not val.isdigit()
        }

        channel_handlers = {
            'empty_or_default': lambda: None,
            'username_with_at': lambda: channel_value,
            'numeric_id': lambda: int(channel_value) if int(channel_value) != 0 else None,
            'username_without_at': lambda: f"@{channel_value}"
        }

        for validator_key, validator_func in channel_validators.items():
            if validator_func(channel_value):
                try:
                    return channel_handlers[validator_key]()
                except (ValueError, TypeError):
                    return None

        return None

    def _parse_recipients(self) -> List[Union[int, str]]:
        raw_ids = self.parser.get('Gifts', 'USER_ID', fallback='').split(',')
        recipients = []

        for user_id in raw_ids:
            user_id = user_id.strip()
            if not user_id:
                continue

            recipient_processors = {
                'username_with_at': {
                    'condition': lambda uid: uid.startswith('@'),
                    'handler': lambda uid: uid[1:]
                },
                'numeric_id': {
                    'condition': lambda uid: uid.isdigit(),
                    'handler': lambda uid: int(uid)
                },
                'username_without_at': {
                    'condition': lambda uid: not uid.startswith('@') and not uid.isdigit(),
                    'handler': lambda uid: uid
                }
            }

            for processor in recipient_processors.values():
                if processor['condition'](user_id):
                    try:
                        recipients.append(processor['handler'](user_id))
                    except ValueError:
                        recipients.append(user_id)
                    break

        return recipients

    def _parse_gift_ranges(self) -> List[Dict[str, int]]:
        ranges_str = self.parser.get('Gifts', 'GIFT_RANGES', fallback='')
        ranges = []

        for range_item in ranges_str.split(','):
            range_item = range_item.strip()
            if not range_item:
                continue

            try:
                price_part, rest = range_item.split(':')
                supply_part, quantity_part = rest.strip().split(' x ')

                min_price, max_price = map(int, price_part.strip().split('-'))
                supply_limit = int(supply_part.strip())
                quantity = int(quantity_part.strip())

                ranges.append({
                    'min_price': min_price,
                    'max_price': max_price,
                    'supply_limit': supply_limit,
                    'quantity': quantity
                })
            except (ValueError, IndexError):
                error(f"Invalid gift range format: {range_item}")
                continue

        return ranges

    def get_matching_range(self, price: int, total_amount: int) -> tuple[bool, int]:
        for range_config in self.GIFT_RANGES:
            if (range_config['min_price'] <= price <= range_config['max_price'] and
                    total_amount <= range_config['supply_limit']):
                return True, range_config['quantity']
        return False, 0

    def _validate(self) -> None:
        validation_checks = {
            "Telegram > API_ID": self.API_ID == 0,
            "Telegram > API_HASH": not self.API_HASH,
            "Telegram > PHONE_NUMBER": not self.PHONE_NUMBER,
            "Gifts > USER_ID": not self.USER_ID,
            "Gifts > GIFT_RANGES": not self.GIFT_RANGES,
        }

        invalid_fields = [field for field, is_invalid in validation_checks.items() if is_invalid]
        if invalid_fields:
            error_msg = localization.translate("errors.missing_config").format(
                '\n'.join(f'- {field}' for field in invalid_fields))
            error(error_msg)
            sys.exit(1)

    @property
    def language_display(self) -> str:
        return localization.get_display_name(self.LANGUAGE)

    @property
    def language_code(self) -> str:
        return localization.get_language_code(self.LANGUAGE)


config = Config()
t = localization.translate
get_language_display = localization.get_display_name
get_language_code = localization.get_language_code
get_all_translations = localization.load_all_translations
