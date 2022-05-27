# -*- coding: utf-8 -*-
from importlib_metadata import entry_points
from telegram.ext import (Updater, CommandHandler, ConversationHandler, MessageHandler, Filters)
from FASE_V_auto_table  import(test_ports,show_tables_telegram,delete_data_log,no_works_log)

input_text = 0
def start(update, context):
	''' START '''
	# Enviar un mensaje a un ID determinado.
	context.bot.send_message(update.message.chat_id, "YourMessage")
def execute(update, context):
	''' Execute '''
	test_ports()
def show(update, context):
	''' Show tables '''
	show_tables_telegram()
def destroy(update, context):
	''' Show tables '''
	delete_data_log()
def no_works(update, context):
	''' Show tables '''
	no_works_log()


def main():
	TOKEN="yourtoken"
	updater=Updater(TOKEN, use_context=True)
	dp=updater.dispatcher


	dp.add_handler(CommandHandler('start',	start))
	dp.add_handler(CommandHandler('execute', execute))
	dp.add_handler(CommandHandler('show', show))
	dp.add_handler(CommandHandler('destroy', destroy))
	dp.add_handler(CommandHandler('status_off', no_works))
	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	main()
