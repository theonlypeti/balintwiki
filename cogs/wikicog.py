import aiohttp
import nextcord as discord
from nextcord.ext import commands, tasks

channel = 790588807770669126


class WikiCog(commands.Cog):
    def __init__(self, client, baselogger):
        global logger
        logger = baselogger.getChild(f"{__name__}Logger")
        self.client = client
        self.wiki.start()

    async def get_random(self):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://en.wikipedia.org/wiki/Special:Random') as req:
                link = req.url
        return link

    @tasks.loop(minutes=1)
    async def wiki(self):
        logger.debug("wiki posted")
        link = await self.get_random()
        await self.client.get_channel(channel).send(link)

    @wiki.before_loop
    async def before_wiki(self):
        logger.info('starting wikiloop')
        await self.client.wait_until_ready()

    @discord.slash_command()
    async def postwiki(self, interaction):
        await interaction.send(await self.get_random())


def setup(client, baselogger):
    client.add_cog(WikiCog(client, baselogger))
