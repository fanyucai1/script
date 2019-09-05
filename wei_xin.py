from wxpy import *

bot = Bot()
my_friend = bot.friends().search('廖*')[0]
my_friend.send('Hello huai dan!')