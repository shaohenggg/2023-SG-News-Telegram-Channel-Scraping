# Initial imports
from datetime import datetime, timezone
import time
import asyncio

# Telegram imports for asynchronous operations
from telethon import TelegramClient

# Google Sheets imports
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Setup Google Sheets Authentication
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('XXX', scope) #insert the file path for your key
gc = gspread.authorize(creds)

# Setup for Telegram
username = 'XXXX'  # Your Telegram username (without @)
phone = 'XXX'    # Your Telegram account phone number (+country code, number, no spaces)
api_id = XXXX        # Your Telegram API ID (as an integer)
api_hash = 'XXXXX'  # Your Telegram API Hash
index = 1

# Define scraping parameters
channel = '@XXX'  # Name of the Telegram channel or group
worksheet_name = 'XXXX'  # Name of the Google Sheets file 
d_min, m_min, y_min = DD, MM, YYYY # Start date (included)
d_max, m_max, y_max = DD, MM, YYYY  # End date (not included)
key_search = ''  # Keyword search (leave as '' if not needed)
your_email = 'XXX@XXX.com'  # Replace with your gmail

# Try to open or create the worksheet in Google Drive
try:
    spreadsheet = gc.open(worksheet_name)
    sheet = spreadsheet.sheet1
    print(f"Sheet found successfully: {spreadsheet.url}")
except gspread.exceptions.SpreadsheetNotFound:
    # Create a new sheet
    created_spreadsheet = gc.create(worksheet_name)
    # Share the newly created sheet with your personal email
    created_spreadsheet.share(your_email, perm_type='user', role='writer')
    sheet = created_spreadsheet.sheet1
    print(f"Sheet created and shared successfully: {created_spreadsheet.url}")

# Clear the worksheet and define titles
sheet.clear()
titles = ['Scraping ID', 'Group', 'Author ID', 'Content', 'Date', 'Message ID', 'Author', 'Views', 'Reactions', 'Shares', 'Media', 'Comments']
sheet.append_row(titles)

# Scraping function
async def scrape_telegram():
    global index
    async with TelegramClient(username, api_id, api_hash) as client:
        async for message in client.iter_messages(channel, search=key_search):
            if datetime(y_min, m_min, d_min, tzinfo=timezone.utc) <= message.date < datetime(y_max, m_max, d_max, tzinfo=timezone.utc):
                url = f'https://t.me/{channel}/{message.id}'.replace('@', '') if message.media else 'no media'
                emoji_string = "".join([f"{reaction_count.reaction.emoticon} {reaction_count.count} " for reaction_count in message.reactions.results]) if message.reactions else ""
                content = [f'#ID{index:05}', channel, message.sender_id, message.text, message.date.strftime('%Y-%m-%d %H:%M:%S'), message.id, message.post_author, message.views, emoji_string, message.forwards, url]

                comments = []
                try:
                    async for reply_message in client.iter_messages(channel, reply_to=message.id):
                        comments.append(reply_message.text)
                except:
                    comments = ['possible adjustment']
                content.append('; '.join(comments))

                sheet.append_row(content)
                print(f'Item {index:05} completed!')
                print(f'Id: {message.id:05}.\n')
                index += 1
                time.sleep(1)

# Replace the asyncio event loop initialization
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Run the scraping process
loop.run_until_complete(scrape_telegram())

print(f'----------------------------------------\n#Concluded! #{index-1:05} posts were scraped!\n----------------------------------------\n\n\n\n')
