import os
import telebot
import wget
from datetime import datetime
from tkinter import filedialog, messagebox

import read_pdf_file
import plot_transactions
import read_transactions
import config

def main():
    bot = telebot.TeleBot(config.token, parse_mode=None)
    current_dir = os.getcwd()

    # create data folder if it does not exist
    data_folder = os.path.join(current_dir, "data")
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    @bot.message_handler(content_types=['document'])
    def content_document(message):
        print(datetime.now(), f"(doc) message_text: {message.document.file_name} by {message.from_user.username}")
        document_id = message.document.file_id
        if message.document.file_size > 20 * 1024 * 1024:
            bot.send_message(message.chat.id, f"File {message.document.file_name} is very large for Telegram API")

        unique_id = message.document.file_name
        with open(f"{current_dir}/data/unique_id", "w") as file:
            file.write(f"{current_dir}/data/{unique_id}")
        print(datetime.now(), "File is sent to bot")
        if message.document.file_name.endswith(".pdf"):
            wget.download(f"http://api.telegram.org/file/bot{config.token}/{bot.get_file(document_id).file_path}",
                          f"{current_dir}/data/{unique_id}")
        # check if pdf file exists
        if os.path.isfile(f"{current_dir}/data/{unique_id}") and os.path.splitext(unique_id)[1].lower() == ".pdf":
            read_pdf_file.read_pdf_file(f"{current_dir}/data/{unique_id}")
        else:
            bot.send_message(message.chat.id, "Error: File does not exist")

        # check if data file exists
        if os.path.isfile(f"{current_dir}/data/data"):
            transactions = read_transactions.read_transactions(f"{current_dir}/data/data")
            plot_transactions.plot_transactions(transactions, f"{current_dir}/data/photo.png")
            with open(f"{current_dir}/data/photo.png", "rb") as photo:
                bot.send_photo(message.chat.id, photo)

            # remove all data
            for file in os.listdir(f"{current_dir}/data"):
                os.remove(os.path.join(f"{current_dir}/data", file))

    bot.infinity_polling()

if __name__ == '__main__':
    main()
