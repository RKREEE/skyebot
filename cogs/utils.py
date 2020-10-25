import discord
from discord.ext import commands, tasks


class Utils(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.update_activity.start()

	def cog_unload(self):
		self.update_activity.cancel()

	@tasks.loop(seconds=60*5)
	async def update_activity(self):
		activity = f'{self.bot.default_prefixes[0]}help | in {len(self.bot.guilds)} servers'
		await self.bot.change_presence(activity=discord.Game(activity))

	@update_activity.before_loop
	async def before_activity(self):
		await self.bot.wait_until_ready()


	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.CommandNotFound):
			return

		elif isinstance(error, commands.UserInputError):
			await ctx.send(f'Error: `{error}`')
			return

		elif isinstance(error, commands.CommandOnCooldown):
			_retry = round(error.retry_after, 2)

			_rate = error.cooldown.rate
			_per = error.cooldown.per
			_type = str(error.cooldown.type).rsplit('.', 1)[-1]

			await ctx.send(f'{ctx.author.mention}, you have to wait {_retry} seconds before using this again. The cooldown for this command is {_rate} per {_per}s for every {_type}')
			return

		elif isinstance(error, commands.CommandInvokeError):
			await ctx.send(f'Something went wrong! Error: `{error}`')
			# report this error to the developer
			appinfo = await self.bot.application_info()
			await self.bot.owner.send(f'An error occured: `{error}`\nctx.message: `{ctx.message}`\nctx.message.content: `{ctx.message.content}`')
			return

		raise error


def setup(bot):
	bot.add_cog(Utils(bot))
