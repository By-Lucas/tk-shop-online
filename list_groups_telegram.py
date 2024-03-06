import configparser

from telethon import TelegramClient

config = configparser.ConfigParser()
config.read('config.ini')

phone = config['AUTH']['PHONE']
api_id = config['AUTH']['API_ID']
token = config['AUTH']['BOT_TOKEN']
name_bot = config['AUTH']['NAME_BOT']
api_hash = config['AUTH']['API_HASH']
password = config['AUTH']['PHONE_PASSWORD']


client = TelegramClient(f'sessions/{name_bot}', api_id, api_hash)


async def main():
    await client.start(phone)
    dialogs = await client.get_dialogs()
    for dialog in dialogs:
        if dialog.is_group or dialog.is_channel:
            print(f"{dialog.name}: {dialog.id}")

    await client.run_until_disconnected()


client.loop.run_until_complete(main())
