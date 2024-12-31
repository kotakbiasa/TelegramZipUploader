import os
import argparse
from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from PIL import Image

def add_logo_to_image(image_path, logo_path, output_path):
    base_image = Image.open(image_path)
    logo = Image.open(logo_path)

    # Resize logo to fit the base image
    logo.thumbnail((base_image.width // 5, base_image.height // 5), Image.ANTIALIAS)

    # Position the logo at the bottom-right corner
    position = (base_image.width - logo.width, base_image.height - logo.height)
    base_image.paste(logo, position, logo)

    base_image.save(output_path)

def upload_files_in_directory(directory, api_id, api_hash, bot_token, logo_path):
    with Client("deltarvx", api_id=api_id, api_hash=api_hash, bot_token=bot_token) as app:
        chat_id = 'KotakReVanced'
        base_url = f"https://github.com/kotakbiasa/TelegramZipUploader/blob/main/{directory}/"
        
        for root, _, files in os.walk(directory):
            for filename in files:
                file_path = os.path.join(root, filename)
                
                # Create a new file path for the image with the logo
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    output_path = os.path.join(root, f"logo_{filename}")
                    add_logo_to_image(file_path, logo_path, output_path)
                    file_path = output_path
                
                file_url = os.path.join(base_url, filename)
                caption = f"`{filename}`"
                button = InlineKeyboardButton(text="📦 Download", url=file_url)
                reply_markup = InlineKeyboardMarkup([[button]])
                
                app.send_document(chat_id=chat_id, document=file_path, caption=caption, reply_markup=reply_markup)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Upload files in a directory to Telegram.')
    parser.add_argument('--dir', type=str, help='Directory path containing files to upload')
    parser.add_argument('--api_id', type=int, help='API ID for your Telegram app')
    parser.add_argument('--api_hash', type=str, help='API Hash for your Telegram app')
    parser.add_argument('--bot_token', type=str, help='Bot Token for your Telegram bot')
    parser.add_argument('--logo_path', type=str, help='Path to the logo image')

    args = parser.parse_args()

    if args.dir and args.api_id and args.api_hash and args.bot_token and args.logo_path:
        directory = args.dir
        api_id = args.api_id
        api_hash = args.api_hash
        bot_token = args.bot_token
        logo_path = args.logo_path

        upload_files_in_directory(directory, api_id, api_hash, bot_token, logo_path)
    else:
        print("Please provide directory path, api_id, api_hash, bot_token, and logo_path using appropriate arguments.")
