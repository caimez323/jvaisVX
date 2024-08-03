import discord
import os

class VXBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reputation_dict = {}
        self.bot_prefix = "§"
    
    async def on_ready(self):
        print(f'We have logged in as {self.user}')
    
    async def on_message(self, message):
        if message.author == self.user:
            return

        if 'https://twitter.com/' in message.content:
            await message.channel.send(
                message.content.replace("https://twitter.com/", "https://vxtwitter.com/") + " (" + message.author.name + ")"
            )
            await message.delete()

        if 'https://x.com/' in message.content:
            await message.channel.send(
                message.content.replace("https://x.com/", "https://fixvx.com/") + " (" + message.author.name + ")"
            )
            await message.delete()

        if "https://www.instagram.com/" in message.content:
            await message.channel.send(
                message.content.replace("https://www.instagram.com/", "https://www.ddinstagram.com/") + " (" + message.author.name + ")"
            )
            await message.delete()
        
        if "//vxtwitter.com/" in message.content or "//fixvx.com/" in message.content or "https://ddinstagram.com/" in message.content:
            await message.add_reaction('♥')
            message_author_name = message.author.name

            if message_author_name in self.reputation_dict:
                self.reputation_dict[message_author_name] += 1
            else:
                self.reputation_dict[message_author_name] = 1
        
        elif "vxtwitter" in message.content or "fixvx" in message.content:
            await message.add_reaction('\N{THUMBS UP SIGN}')

        if message.content.startswith(self.bot_prefix):
            if message.content[1:] == "reputation":
                if not self.reputation_dict:
                    await message.channel.send("Personne n'est dans le leaderboard pour le moment...")
                    return
                buffer = ""
                toCrown = True
                for user, score in dict(sorted(self.reputation_dict.items(), key=lambda x: x[1])).items():
                    buffer += " | {}{} : {} |\n".format(":crown: " if toCrown else "", user, score)
                    if toCrown:
                        toCrown = False
                await message.channel.send(buffer)

def run_bot():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = VXBot(intents=intents)

    try:
        token = os.getenv("DISCORD_TOKEN") or ""
        bot.run(token)
    except discord.HTTPException as e:
        raise e

if __name__ == "__main__":
    run_bot()
