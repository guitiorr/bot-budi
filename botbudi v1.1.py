import discord
import asyncio 
from asyncio import run_coroutine_threadsafe as rct
from discord.ext import commands, tasks
from discord.voice_client import VoiceClient
from keep_alive import keep_alive
import youtube_dl
import os
import random

from random import choice

my_secret = os.environ['BOT KEY']

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
			#this loop variable is not the same as the boolean loop variable used to indicate queue loop
			#it's for event loop
      isYoutube = True #TODO: change this variable automatically; by checking url 
      loop = loop or asyncio.get_event_loop()#get event loop from loop argument or asyncio.get_event_loop

      data = None
      if (isYoutube):
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream)) 
      else:
      #  spotifySrc= spotify.track(url)#spotify search
      #  spotifyName = f"{spotifySrc['album']['artists'][0]['name']}-{spotifySrc['name']}"
      #  print(spotifyName)
      #  data = await loop.run_in_executor(None, lambda: ytdl.extract_info(spotifyName, download=not stream))
      #print(data)#debugging purposes
        pass
      
      if 'entries' in data:#if it's a youtube playlist
      # take first item from a playlist if the youtube link is a playlist
        data = data['entries'][0]
			
      filename = data['url'] if stream else ytdl.prepare_filename(data)
			#spotipy doesnt have properties called url
      #print(filename)#debugging purposes
      return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data) 

class CustomHelp(commands.DefaultHelpCommand):#inherit from default help command
	def get_ending_note(self):#override ending note function
		return "Type ?help command for more info on a command.\n**Currently this bot can only play songs from youtube**"

def is_connected(ctx):
    voice_client = ctx.message.guild.voice_client
    return voice_client and voice_client.is_connected()


intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='?', intents = intents)

#status = ['?help','AAAA','EEEEE']
queue = []
loop = False
player1 = ""
player2 = ""
turn = ""
gameOver = True

board = [0,0,0,0,0,0,0,0,0]

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@client.event
async def on_ready():
    print('Successful log in as {0.user}'.format(client)) #Prints when log in to Bot Budi is successful

@client.event
async def on_connect():
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="?help"))

@client.event
async def on_message(msg):
	if(client.user.mentioned_in(msg)):
		await msg.channel.send('(*・ω・)ﾉ')
	await client.process_commands(msg)

@client.event#moderately annoying stuff
async def on_typing(channel,user,when):
	if(not user.bot):
		await channel.trigger_typing()
		await asyncio.sleep(3)

@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='general')
    await channel.send(f'Hi fuck you {member.mention}')

@client.command(name='tictactoe', help='TIC TAC TOE DA GAME',aliases=['ttt'])
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("A game is already in progress! Finish it before starting a new one.")

@client.command(name='place',help='Place command for TTT')
async def place(ctx,x ,y):#pos: int):#alternate
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    #minus 1 so coordinates start from 1 1
    x = int(x) - 1
    y = int(y) - 1
    pos = y*3+x # the formula is y * width + x;remember width is not array length
    #pos -= 1 #alternate
    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            
            #if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :#alternate
            if (x>=0 and x < 3 and y>=0 and y < 3 and board[pos] == ":white_large_square:" ) :
                board[pos] = mark 
                count += 1
                #print('{} {}'.format(x,y))#debug
                #print(board)#debug

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the !tictactoe or !ttt command.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        print(error)
        await ctx.send("Missing argument, please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")

@client.command(name='ping', help='This command returns the latency')
async def ping(ctx):
    await ctx.send(f'{round(client.latency * 1000)}ms')

@client.command(name='hi', help='This command returns a random welcome message')
async def hi(ctx):
    responses = ['Yo', 'Hello my name is bady, but you can call me anytime']
    await ctx.send(choice(responses))

@client.command(name='join', help='This command makes the bot join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel")
        return
    
    else:
        channel = ctx.message.author.voice.channel

    await channel.connect()
    
@client.command(name='eue',hidden=True)#hehe :D
async def eue(ctx):
	await ctx.send("(⁄ ⁄•⁄ω⁄•⁄ ⁄)")

@client.command(name='ass',hidden=True)#hehe :D
async def ass(ctx):
	ass = """
**ASS**
⠄⠄⣿⣿⣿⣿⠘⡿⢛⣿⣿⣿⣿⣿⣧⢻⣿⣿⠃⠸⣿⣿⣿⠄⠄⠄⠄⠄
⠄⠄⣿⣿⣿⣿⢀⠼⣛⣛⣭⢭⣟⣛⣛⣛⠿⠿⢆⡠⢿⣿⣿⠄⠄⠄⠄⠄
⠄⠄⠸⣿⣿⢣⢶⣟⣿⣖⣿⣷⣻⣮⡿⣽⣿⣻⣖⣶⣤⣭⡉⠄⠄⠄⠄⠄
⠄⠄⠄⢹⠣⣛⣣⣭⣭⣭⣁⡛⠻⢽⣿⣿⣿⣿⢻⣿⣿⣿⣽⡧⡄⠄⠄⠄
⠄⠄⠄⠄⣼⣿⣿⣿⣿⣿⣿⣿⣿⣶⣌⡛⢿⣽⢘⣿⣷⣿⡻⠏⣛⣀⠄⠄
⠄⠄⠄⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠙⡅⣿⠚⣡⣴⣿⣿⣿⡆⠄
⠄⠄⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠄⣱⣾⣿⣿⣿⣿⣿⣿⠄
⠄⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⠄
⠄⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠣⣿⣿⣿⣿⣿⣿⣿⣿⣿⠄
⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠑⣿⣮⣝⣛⠿⠿⣿⣿⣿⣿⠄
⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⠄⠄⠄⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠄
"""
	await ctx.send(ass)



@client.command(name='leave', help='This command stops the music and makes the bot leave the voice channel',aliases=['disconnect','dc'])
async def leave(ctx):
    if not ctx.message.author.voice:
        await ctx.send("I'm not in a voice channel or i have disconnected")
        return
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()
    responses = ['ok bye']
    await ctx.send(choice(responses))
	
@client.command(name='loop', help='Toggles queue loop mode')
async def loop_(ctx):
    global loop

    if loop:
        await ctx.send('Loop mode is now `False!`')
        loop = False
    
    else: 
        await ctx.send('Loop mode is now `True!`')
        loop = True

@client.command(name='play', help='This command plays music in your queue')
async def play(ctx):
	#TODO: add ability to play from spotify
    global queue
    if not ctx.message.author.voice:#if the message author is not on a vc send a message
        await ctx.send("You are not connected to a voice channel")
        return
    
    else:#get message author's vc
        channel = ctx.message.author.voice.channel

    try: await channel.connect()#try to connect to the vc
    except: pass

    server = ctx.message.guild
    voice_channel = server.voice_client
    
    try:
        async with ctx.typing():#while giving a typing notification
            player = await YTDLSource.from_url(queue[0], loop=client.loop,stream=True)#stream from youtube

            voice_channel.play(player, after=lambda e:
			 rct(ctx.invoke(ctx.bot.get_command('play')),client.loop))#play the audio; lambda function is used to play another song after the current one is finished
            
            if loop:#if there's loop append current entry to the end of queue
                queue.append(queue[0])

            del(queue[0])#delete current queue
            
        await ctx.send('**Now playing:** {}'.format(player.title))

    except:
        await ctx.send('Nothing in your queue. Use `?queue` to add a song.')

@client.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_channel = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice_channel.is_playing():
        voice_channel.pause()
    else:
        await ctx.send("No audio is playing.")

@client.command(name='resume', help='This command resumes the song')
async def resume(ctx):
    voice_channel = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice_channel.is_paused():
        voice_channel.resume()
    else:
        await ctx.send("No audio is paused.")

@client.command(name='skip', help='This command skip the song in queue',aliases=['s','stop'])
async def stop(ctx):
    voice_channel = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice_channel.is_playing():
        voice_channel.stop()
    else:
        await ctx.send("No audio is playing.")

@client.command(name='queue', help='Adds a song to the queue',aliases=['q'])
async def queue_(ctx, *args):
    global queue
    url = " ".join(args[:])
    queue.append(url)
    await ctx.send(f'`{url}` added to queue!')

@client.command(name='remove', help='Removes an item from the list',aliases=['rm'])
async def remove(ctx, number=0):#number defaults to 0
		global queue
		number -= 1#decrements number by 1; so 1 would be the first element
		try:
			del(queue[int(number)])
      #await ctx.send(f'Your queue is now `{queue}!`')
			await ctx.invoke(ctx.bot.get_command('list'))
    
		except:
			await ctx.send('Your queue is either **empty** or the index is **out of range**')


@client.command(name='view', help='This command shows the queue',aliases=['v'])
async def view(ctx):
    await ctx.send(f'Your queue is now `{queue}!`')

@client.command(name='list', help='Better than view command',aliases=['ls'])
async def list(ctx):#TODO: show title name instead of url
	lines="**CURRENT QUEUE**:\n>>> "
	idx = 1
	for i in queue:
		lines+=f'`{idx}`. `{i}`\n'
		idx += 1
	await ctx.send(lines)

@client.command(name='clear', help='clears the whole queue',aliases=['cls'])
async def cls(ctx):
	global queue
	
	del(queue[:])
	await ctx.send("queue cleared")


#@tasks.loop(seconds=20)
#async def change_status():
    #await client.change_presence(activity=discord.Game(choice(status)))


keep_alive()
try : 
    client.run(os.getenv('BOT KEY'))
except:
    os.system("kill 1")