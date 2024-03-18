import imaplib
import email
import time
from email.header import decode_header
import asyncio
import logging
import sys
from os import getenv

import aiogram.exceptions
from aiogram import Bot

BOT_TOKEN = getenv("BOT_TOKEN")
CHAT_ID = int(getenv("CHAT_ID"))
IMAP_SERVER = getenv("IMAP_SERVER")
USER_EMAIL = getenv("USER_EMAIL")
USER_APP_PASSWORD = getenv("USER_APP_PASSWORD")


def get_actual_body(body: str) -> str:
    lines = body.split('\n')
    for line in lines.copy():
        if line.startswith('>'):
            lines.remove(line)
    return '\n'.join(lines)


async def send_message(bot: aiogram.Bot, folder: str, from_: str, subject: str, body: str, chat_id: int) -> None:
    message_text = f"Новое сообщение в папке '{folder}':\n\nОт: {from_}\nТема: {subject}\n\n{body}"
    try:
        await bot.send_message(chat_id=chat_id, text=message_text)
    except aiogram.exceptions.TelegramBadRequest:
        message_text = (f"Новое сообщение в папке '{folder}':\n\nОт: {from_}\nТема: {subject}\n\n"
                        f"Слишком большое сообщение")
        await bot.send_message(chat_id=chat_id, text=message_text)


async def check_and_send_unread_emails(bot: aiogram.Bot, chat_id: int) -> None:
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(USER_EMAIL, USER_APP_PASSWORD)

    for folder in ["INBOX"]:
        mail.select(folder)

        status, messages = mail.search(None, '(UNSEEN)')
        if status == 'OK':
            messages = messages[0].split()

            for mail_id in messages:
                status, data = mail.fetch(mail_id, '(RFC822)')
                if status == 'OK':
                    raw_email = data[0][1]
                    msg = email.message_from_bytes(raw_email)

                    subject = decode_header(msg['Subject'])[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode()
                    from_ = decode_header(msg['From'])[0][0]
                    if isinstance(from_, bytes):
                        from_ = from_.decode()

                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            if content_type == "text/plain" or content_type == "text/html":
                                body = part.get_payload(decode=True).decode(part.get_content_charset())
                                break
                    else:
                        body = msg.get_payload(decode=True).decode(msg.get_content_charset())
                    actual_body = get_actual_body(body)
                    await send_message(bot, folder, from_, subject, actual_body, chat_id)
                time.sleep(1)
    mail.logout()


async def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    bot = Bot(token=BOT_TOKEN)

    while True:
        await check_and_send_unread_emails(bot, CHAT_ID)
        await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
