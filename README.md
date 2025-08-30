# Telegram Gifts Buyer

<img src="https://github.com/user-attachments/assets/a8d750d3-500c-4372-9733-3bbd509643e8" alt="Program Preview" width="100%" />

An automated Telegram userbot that purchases new gifts as they become available in the Telegram store. The bot can
handle both limited and non-limited gifts with flexible configuration options and intelligent prioritization.

> 🌐 [Русская версия документации](README-RU.md)

## 📋 Features

- **Automated Gift Detection**: Continuously monitors for new gifts in the Telegram store
- **Smart Prioritization**: Prioritize gifts with low supply that match your price ranges
- **Unified Range Configuration**: Define price ranges, supply limits, and quantities in one elegant format
- **Multiple Recipients**: Send gifts to one or more users with flexible ID/username support
- **Notification System**: Get updates on purchases through a designated Telegram channel
- **Advanced Filtering**: Choose to buy only limited or upgradable gifts
- **Multi-language Support**: Available in English and Russian

## 🛠️ Installation

### Setup Steps

1. Clone the repository (or download zip):

   ```bash
   git clone https://github.com/qpwedev/Gifts-Buyer.git
   cd Gifts-Buyer
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure the application:
   - Edit the `config.ini` file with your API credentials
   - Set your preferred gift purchasing parameters

## ⚙️ Configuration

Open `config.ini` and configure the following sections:

### Telegram API Settings

```ini
[Telegram]
API_ID = your_api_id              # Get from https://my.telegram.org/apps
API_HASH = your_api_hash          # Get from https://my.telegram.org/apps
PHONE_NUMBER = +1234567890        # Your phone number in international format

# Channel for notifications - supports multiple formats:
CHANNEL_ID = -1001234567890       # Channel ID (numeric) or @usernamw
```

### Bot Behavior

```ini
[Bot]
INTERVAL = 10     # Check interval in seconds (recommended: 5-15)
LANGUAGE = EN     # Interface language (EN or RU)
```

### Gift Preferences

```ini
[Gifts]
# Unified gift ranges with price, supply, and quantity
GIFT_RANGES = 1-1000: 500000 x 1, 1001-5000: 100000 x 2, 5001-10000: 50000 x 3

# Recipients - supports multiple formats (comma-separated):
USER_ID = 123456789, @johndoe, username123    # Mix of IDs and usernames

# Purchase filters
PURCHASE_NON_LIMITED_GIFTS = False      # Whether to buy non-limited gifts
PURCHASE_ONLY_UPGRADABLE_GIFTS = False  # Buy only upgradable gifts

# Smart prioritization
PRIORITIZE_LOW_SUPPLY = True            # Prioritize gifts matching ranges with lowest supply first
```

#### Unified Gift Ranges Configuration

The `GIFT_RANGES` parameter uses an elegant unified format: `min_price-max_price: supply_limit x quantity`

**Examples:**

- `1-1000: 500000 x 1` - Buy gifts priced 1-1000 stars (supply ≤ 500,000) and send 1 copy
- `1001-5000: 100000 x 2` - Buy gifts priced 1001-5000 stars (supply ≤ 100,000) and send 2 copies
- `5001-10000: 50000 x 3` - Buy gifts priced 5001-10000 stars (supply ≤ 50,000) and send 3 copies

**Key Features:**

- All ranges are **inclusive** (≤)
- Different quantities per price range
- Automatic supply-based filtering
- Multiple ranges supported (comma-separated)

#### Smart Prioritization

When `PRIORITIZE_LOW_SUPPLY = True`, the bot processes gifts in optimal order:

1. **Priority 1**: Gifts matching your ranges, sorted by lowest supply first
2. **Priority 2**: Remaining gifts in discovery order

**Example Scenario:**

- Gift A: 2000⭐, 50,000 supply, quantity=2 (matches range, low supply)
- Gift B: 1500⭐, 200,000 supply, quantity=1 (matches range, high supply)
- Gift C: 15000⭐, 10,000 supply (doesn't match any range)

**Processing Order:** A (2x) → B (1x) → C (skipped)

## 🚀 Usage

Run the bot with:

```bash
python main.py
```

The bot will:

1. Log in to your Telegram account
2. Start monitoring for new gifts
3. Purchase gifts matching your ranges with specified quantities
4. Send notifications through your specified channel

## 📊 Monitoring & Notifications

The bot provides detailed notifications including:

- ✅ Successful purchases with recipient information and quantities
- ❌ Failed purchases with error explanations
- 📊 Processing summaries (skipped gifts breakdown)
- 💰 Balance notifications for insufficient funds
- 🎯 Range mismatch notifications

## 📝 Notes & Best Practices

- **Balance Management**: Ensure sufficient stars for multiple quantities per gift
- **Range Strategy**: Use higher quantities for rarer, more expensive gifts
- **24/7 Operation**: Run on VPS/server for continuous monitoring
- **Rate Limiting**: Built-in delays respect Telegram's API limits
- **Priority Strategy**: Enable `PRIORITIZE_LOW_SUPPLY` for competitive advantage

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

<div align="center">
    <h4>Built with ❤️ by <a href="https://t.me/meow" target="_blank">Meow</a></h4>
</div>
