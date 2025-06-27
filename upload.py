import os
import argparse
import requests
from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

THUMB_URL = "https://envs.sh/2e5.jpg"
THUMB_PATH = "thumb.jpg"

def download_thumb():
    if not os.path.exists(THUMB_PATH):
        r = requests.get(THUMB_URL)
        with open(THUMB_PATH, "wb") as f:
            f.write(r.content)

def upload_files_in_directory(directory, api_id, api_hash, bot_token, release_tag, emoji=None):
    if not emoji:
        emoji = "🔥 👍"
    download_thumb()
    with Client("deltarvx", api_id=api_id, api_hash=api_hash, bot_token=bot_token) as app:
        chat_id = 'KotakReVanced'  # Ganti dengan ID chat atau channel tujuan Anda
        base_url = f"https://github.com/muhnurfauzan/revanced-magisk-module/releases/{release_tag}/"
        
        for root, _, files in os.walk(directory):
            for filename in files:
                file_path = os.path.join(root, filename)
                file_url = base_url + filename
                caption = f"`{filename}`"
                button = InlineKeyboardButton(text="📦 Download", url=file_url)
                reply_markup = InlineKeyboardMarkup([[button]])
                message = app.send_document(
                    chat_id=chat_id,
                    document=file_path,
                    caption=caption,
                    reply_markup=reply_markup,
                    thumb=THUMB_PATH
                )
                # Kirim reaksi emoji satu per satu jika ada lebih dari satu
                if emoji:
                    for emj in emoji.split():
                        app.send_reaction(
                            chat_id=chat_id,
                            message_id=message.id,
                            emoji=emj
                        )
                

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Upload files in a directory to Telegram.')
    parser.add_argument('--dir', type=str, help='Directory path containing files to upload')
    parser.add_argument('--api_id', type=int, help='API ID for your Telegram app')
    parser.add_argument('--api_hash', type=str, help='API Hash for your Telegram app')
    parser.add_argument('--bot_token', type=str, help='Bot Token for your Telegram bot')
    parser.add_argument('--release_tag', type=str, help='Release tag for GitHub URL', required=True)
    parser.add_argument('--emoji', type=str, help='Emoji reaction to add to each message', required=False)

    args = parser.parse_args()

    if args.dir and args.api_id and args.api_hash and args.bot_token and args.release_tag:
        directory = args.dir
        api_id = args.api_id
        api_hash = args.api_hash
        bot_token = args.bot_token
        release_tag = args.release_tag
        emoji = args.emoji if args.emoji else "🔥👍"

        upload_files_in_directory(directory, api_id, api_hash, bot_token, release_tag, emoji)
    else:
        print("Please provide directory path, api_id, api_hash, bot_token, and release_tag using appropriate arguments.")
