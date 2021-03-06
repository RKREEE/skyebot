import discord
from discord.ext import commands

import time
import sys


class General(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(description='Invite this bot to your server!', aliases=['addbot', 'botinvite'])
	async def invite(self, ctx):
		url = discord.utils.oauth_url(
			self.bot.user.id,
			permissions = discord.Permissions.all()
		)
		await ctx.send(f'Invite link: <{url}>')

	@commands.command(description='Sends a report to the bot developer')
	async def report(self, ctx, *, report_message: str):
		await self.bot.owner.send(f'**report from {ctx.author} (id: {ctx.author.id})**\n```{report_message}```')

		await ctx.send('Your report was sent to the developer!')

	@commands.command(description='Displays information about the bot', aliases=['ping', 'uptime', 'source'])
	async def info(self, ctx):
		seconds = time.time() - self.bot.start_time
		m, s = divmod(seconds, 60)
		h, m = divmod(m, 60)
		d, h = divmod(h, 24)
		w, d = divmod(d, 7)
		uptime_str = f'{int(w)}w : {int(d)}d : {int(h)}h : {int(m)}m : {int(s)}s'

		py_version = f'{sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}'

		member_count = len(self.bot.users)

		embed = discord.Embed(
			title='Information about SkyeBot',
			colour=self.bot.main_colour,
			description=f'This bot was made by `{self.bot.owner}`. The full source code can be found at https://github.com/Skycloudd/skyebot.'
		)

		embed.set_thumbnail(url=self.bot.user.avatar_url_as(format="png"))

		embed.add_field(
			name='Info',
			value=f'ID: {self.bot.user.id}\nName: {self.bot.user.name}',
			inline=True
		)
		embed.add_field(
			name='Bot ping to Discord servers',
			value=f'{round(self.bot.latency * 1000)}ms',
			inline=True
		)
		embed.add_field(
			name='Library',
			value=f'Discord.py v{discord.__version__}',
			inline=True
		)
		embed.add_field(
			name='Python version',
			value=py_version,
			inline=True
		)
		embed.add_field(
			name='Uptime',
			value=uptime_str,
			inline=True
		)
		embed.add_field(
			name='User count',
			value=f'{member_count} users in {len(self.bot.guilds)} servers'
		)

		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(General(bot))
