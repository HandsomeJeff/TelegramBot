
import sys
import datetime
import telepot
import random
import time

bot = telepot.Bot('264767367:AAGztA76Q8cv5RGXSWemn4X693XE0XtezL8')

handsomelist = ['Steve']
not_handsomelist = []
somewhat_handsomelist = []

handsomelistno = ['93']
not_handsomelistno = []
somewhat_handsomelistno = []


def main(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print 'Got command: %s' % command
    print command[0:9]
    print command[10:]
    if command[0:9] == '/handsome':
        print 'success'
        name = str(command[10:])
        if name not in handsomelist and name not in somewhat_handsomelist and name not in not_handsomelist:
            bot.sendMessage(chat_id, '--NEW NAME DETECTED--')
            bot.sendMessage(chat_id, '--CALCULATING HANDSOMENESS...--')
            d = random.randint(1,100)
            print d
            sd = str(d)
            if d > 60:
                handsomelist.append(name)
                handsomelistno.append(sd)
            elif d < 20:
                not_handsomelist.append(name)
                not_handsomelistno.append(sd)
            else:
                somewhat_handsomelist.append(name)
                somewhat_handsomelistno.append(sd)
            bot.sendMessage(chat_id, 'Handsomeness Index: %s' % d)
            if name in handsomelist:
                bot.sendMessage(chat_id, '%s is very handsome!' % name)
            elif name in somewhat_handsomelist:
                bot.sendMessage(chat_id, '%s is somewhat handsome' % name)
            elif name in not_handsomelist:
                bot.sendMessage(chat_id, '%s is not handsome' % name)
        else:
            bot.sendMessage(chat_id, '--NAME RECOGNISED--')
            bot.sendMessage(chat_id, '--RETRIEVING DATA...--')
            if name in handsomelist:
                bot.sendMessage(chat_id, 'Handsomeness Index: %s' % handsomelistno[handsomelist.index(name)])
                bot.sendMessage(chat_id, '%s is very handsome!' % name)
            elif name in somewhat_handsomelist:
                bot.sendMessage(chat_id, 'Handsomeness Index: %s' % somewhat_handsomelistno[somewhat_handsomelist.index(name)])
                bot.sendMessage(chat_id, '%s is somewhat handsome' % name)
            elif name in not_handsomelist:
                bot.sendMessage(chat_id, 'Handsomeness Index: %s' % not_handsomelistno[not_handsomelist.index(name)])
                bot.sendMessage(chat_id, '%s is not handsome' % name)
    elif command == '/time':
        bot.sendMessage(chat_id, str(datetime.datetime.now()))

bot.message_loop(main)
print 'I am listening...'

while 1:
    time.sleep(10)
