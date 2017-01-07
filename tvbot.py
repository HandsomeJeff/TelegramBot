import sys
import time
import threading
import random
from pprint import pprint

import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardHide, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent
from telepot.delegate import pave_event_space, per_chat_id, create_open
import urllib
import json

# install via “easy_install tvdb_api”
import tvdb_api as tv


# retrieves season and episode
def retrieve(x, y):
   return show[x][y]


count = ["game of thrones"]


class MessageCounter(telepot.helper.ChatHandler):
   def __init__(self, *args, **kwargs):
       super(MessageCounter, self).__init__(*args, **kwargs)
       self._count = 0

   def on_chat_message(self, msg):
       self._count += 1

       content_type, chat_type, chat_id = telepot.glance(msg)
       print('Chat:', content_type, chat_type, chat_id)

       if content_type != 'text':
           return

       command = msg['text'].lower()

       print(command)

       # keeps track of which stage of the flow to jump to based on the user’s command
       comd_list = ['/nextairing', '/episodesynopsis', '/cast']
       comd_dict = {'/nextairing': 10, '/episodesynopsis': 200, '/cast': 100}

       if command in comd_list:
           self._count = 0
           self._count += comd_dict[command]
       print(self._count)

       if command.split(" ")[0] == "season":
           self._count = 220
       if command.split(" ")[0] == "episode":
           self._count = 240

       cr = len(count) - 1
       if command == '/reset':
           self._count = 0
       elif command == '/home':
           markup = ReplyKeyboardMarkup(keyboard=[
               [KeyboardButton(text='/NextAiring')], [KeyboardButton(text='/EpisodeSynopsis')],
               [KeyboardButton(text='/Cast')], [KeyboardButton(text='/reset')]
           ])
           t = tv.Tvdb()
           showname = count[len(count) - 1]
           show = t[showname]
           # display the TV series ratings and synopsis when show is found in database
           bot.sendMessage(chat_id, "Series Title: {}\n".format(show["seriesname"]),
                           reply_markup=markup)
       if self._count == 0 or self._count == 1 or command[:3] == '/tv':
           try:
               if command[:3] == '/tv':
                   # if TV show found, display the inline keyboard with choices for user input
                   count.append(command[4:])
                   print(count[len(count) - 1])
                   self._count = 0
                   markup = ReplyKeyboardMarkup(keyboard=[
                       [KeyboardButton(text='/NextAiring')], [KeyboardButton(text='/EpisodeSynopsis')],
                       [KeyboardButton(text='/Cast')], [KeyboardButton(text='/reset')]
                   ])
                   t = tv.Tvdb()
                   showname = count[len(count) - 1]
                   show = t[showname]
                   # display the TV series ratings and synopsis when show is found in database
                   bot.sendMessage(chat_id,
                                   "Series Title: {}\nSeries Ratings: {}\nSynopsis: {} ".format(show["seriesname"],
                                                                                                show["rating"],
                                                                                                show["overview"]),
                                   reply_markup=markup)
               else:
                   bot.sendMessage(chat_id, "Enter /tv {tv show name} to begin", reply_markup=ReplyKeyboardHide())
           except:
               bot.sendMessage(chat_id, "Enter /tv {tv show name} to begin", reply_markup=ReplyKeyboardHide())

               # this section determines if the tv show is still airing. If still airing, it displays the day of the week and timing. Else, it displays the status (eg. ended)
       if self._count == 10:
           t = tv.Tvdb()
           showname = count[len(count) - 1]
           show = t[showname]
           if show["status"] == "Continuing":
               txt = ('The show airs ' + show["airs_dayofweek"] + ', ' + show["airs_time"])
           else:
               txt = ("The show has " + show["status"].lower() + '.')
           markup = ReplyKeyboardMarkup(keyboard=[
               ['/home'], ['/reset']
           ])
           bot.sendMessage(chat_id, txt, reply_markup=markup)

       if self._count == 200:
           t = tv.Tvdb()
           showname = count[len(count) - 1]
           season_num = []
           no_seasons = len(t[showname]) - 1
           # displays all the available seasons as buttons in the inline keyboard
           for x in range(no_seasons):
               season_num.append(KeyboardButton(text='Season %d' % (x + 1)))

           season_num.append('/home')
           season_num.append('/reset')
           markup = ReplyKeyboardMarkup(keyboard=[
               [x] for x in season_num])

           bot.sendMessage(chat_id, 'Which season?', reply_markup=markup)

       if self._count == 220:
           t = tv.Tvdb()
           showname = count[len(count) - 1]
           episode_no = len(t[showname][int(command.split(" ")[1])])
           count.append(int(command.split(" ")[1]) - 1)
           episode_num = []
           # displays all the available episodes as buttons in the inline keyboard
           for x in range(episode_no):
               episode_num.append(KeyboardButton(text='Episode %d' % (x + 1)))
           episode_num.append('/home')
           episode_num.append('/reset')
           markup = ReplyKeyboardMarkup(keyboard=[
               [x] for x in episode_num
               ])
           bot.sendMessage(chat_id, 'Which episode?', reply_markup=markup)

       if self._count == 240:
           t = tv.Tvdb()
           showname = count[len(count) - 2]
           show = t[showname]
           season_num = count[len(count) - 1]
           count.pop(len(count) - 1)
           episode_num = int(command.split(" ")[1])
           synopsis = t[showname][season_num + 1][episode_num]
           markup = ReplyKeyboardMarkup(keyboard=[
               ['/home'], ['/reset']
           ])
           # displays the rating and synopsis for the chosen episode
           bot.sendMessage(chat_id,
                           'Ratings for {}, S{}E{}:\n{}\nSynopsis: {}'.format(show["seriesname"], season_num + 1,
                                                                              episode_num, synopsis["rating"],
                                                                              synopsis["overview"]),
                           reply_markup=markup)

       if self._count == 100:
           t = tv.Tvdb()
           showname = count[len(count) - 1]
           show = t[showname]
           global actorlist
           actorlist = show["actors"]
           actorlist = actorlist[1:len(actorlist) - 1]
           t = tv.Tvdb(actors=True)
           actors = t[showname]['_actors']
           if len(actorlist.split("|")) > 6:
               actorlist = actorlist.split("|")[:6]
           else:
               actorlist = actorlist.split("|")
           actorlist.append('/home')
           actorlist.append('/reset')
           # displays the first 5 actors as buttons for the inline keyboard
           markup = ReplyKeyboardMarkup(keyboard=[
               [x] for x in actorlist
               ])

           bot.sendMessage(chat_id, 'Displaying cast of %s...' % count[len(count) - 1].title(), reply_markup=markup)

       if self._count > 100 and command != '/home':
           t = tv.Tvdb()
           global showname
           t = tv.Tvdb(actors=True)
           actors = t[showname]['_actors']
           global actorlist
           # send chosen actor’s photo as image
           for x in actorlist:
               if x.lower() == command:
                   print('yes')
                   selectactor = actorlist.index(x)
                   bot.sendPhoto(chat_id, actors[selectactor]['image'])


bot = telepot.DelegatorBot("""token here""", [
   pave_event_space()(
       per_chat_id(), create_open, MessageCounter, timeout=100),
])
bot.message_loop(run_forever='Listening ...')
