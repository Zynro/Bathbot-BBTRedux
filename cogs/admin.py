from discord.ext import commands
import sys
import config
import traceback

permission = 'You do not have permission to use this command.'
owner_list = config.owner_list

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def check_cog(self, ctx):
        return ctx.author.id in owner_list

    # Hidden means it won't show up on the default help.
    @commands.command(name='load', hidden=True)
    async def load_cog(self, ctx, *, cog: str):
        """Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        try:
            if '.' not in cog:
                self.bot.load_extension('cogs.'+cog)
            else:
                self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**ERROR:** {type(e).__name__} - {e}')
            traceback.print_exc()
        else:
            await ctx.send('**Success: **cogs.'+cog+' has been loaded!')

    @load_cog.error
    async def load_error_cog(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(permission)


    @commands.command(name='unload', hidden=True)
    async def unload_cog(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        try:
            if '.' not in cog:
                self.bot.unload_extension('cogs.'+cog)
            else:
                self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**ERROR:** {type(e).__name__} - {e}')
        else:
            await ctx.send('**Success:** cogs.'+cog+' has been unloaded!')

    @unload_cog.error
    async def unload_error_cog(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(permission)

    @commands.command(name='reload', hidden=True)
    async def reload_cog(self, ctx, *, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        try:
            if '.' not in cog:
                self.bot.unload_extension('cogs.'+cog)
                self.bot.load_extension('cogs.'+cog)
            else:
                self.bot.unload_extension(cog)
                self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**Error:** {type(e).__name__} - {e}')
            traceback.print_exc()
        else:
            await ctx.send('**Success:** cogs.'+cog+' has been reloaded!')

    @reload_cog.error
    async def reload_error_cog(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(permission)

    @commands.command(name='kill', hidden=True)
    async def kill_bot(self, ctx):
        '''Kills the bot. Only useable by Zynro.'''
        await ctx.send("Well, it's time to take a bath. See you soon! \nBathBot is now exiting.")
        sys.exit()

    @kill_bot.error
    async def kill_error(ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(permission)

    @commands.command(name='list-servers')
    async def list_connected_servers(self, ctx):
        servers = ''
        for each in self.bot.guilds:
            servers = servers + each.name + "\n"
        await ctx.send(f"Here are all the servers I'm currently on:\n```{servers}```")
    
    @list_connected_servers.error
    async def list_connected_servers_error(ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(permission)

def setup(bot):
    bot.add_cog(Admin(bot))