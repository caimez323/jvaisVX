import discord
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

reputation_dict = {}

bot_prefix = "§"

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if ('https://twitter.com/') in message.content :
        await message.channel.send(message.content.replace("https://twitter.com/","https://vxtwitter.com/") + " (" + message.author.name + ")")
        await message.delete()

    if ('https://x.com/') in message.content:
        await message.channel.send(message.content.replace("https://x.com/","https://fixvx.com/") + " (" + message.author.name + ")")
        await message.delete()
        
    if ("https://www.instagram.com/") in message.content:
        await message.channel.send(message.content.replace("https://www.instagram.com/","https://www.ddinstagram.com/") + " (" + message.author.name + ")")
        await message.delete()
        
    if "//vxtwitter.com/" in message.content or  "//fixvx.com/" in message.content or "https://ddinstagram.com/" in message.content:
        await message.add_reaction('♥')
        message_author_name = message.author.name

        if(message_author_name in reputation_dict):
            reputation_dict[message_author_name]+=1
        else:
            reputation_dict[message_author_name]=1
        
    elif "vxtwitter" in message.content or "fixvx" in message.content:
        await message.add_reaction('\N{THUMBS UP SIGN}')

    if message.content.startswith(bot_prefix):

        if message.content[1:] == "reputation":
            if (not any(reputation_dict)):
                await message.channel.send("Personne n'est dans le leaderboard pour le moment...")
                return
            buffer = ""
            toCrown = True
            for user,score in dict(sorted(reputation_dict.items(), key=lambda x:x[1])).items():
                buffer += " | {}{} : {} |\n".format(":crown: " if toCrown else "",user,score)
                if toCrown : toCrown = False
            await message.channel.send(buffer)
           

try:
  token = os.getenv("DISCORD_TOKEN") or ""
  client.run(token)
except discord.HTTPException as e:
    raise e