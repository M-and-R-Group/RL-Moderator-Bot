import os
import discord
token = os.environ['token']
from discord.ext import commands

client= commands.Bot(command_prefix="!r", intents = discord.Intents.all())
client.remove_command("help")

#f = open("rules.txt", "r")
#filtered_words = f.readlines()

filtered_words = ["cat", "dog"]

#@client.event
#async def on_message(msg):
	#for word in filtered_words:
		#if word in msg.content:
			#await msg.delete()
#	await client.process_commands(msg)


@client.event
async def on_ready():
	print("Bot is online and ready to serve!")

@client.command()
async def status(ctx):
	await ctx.send("This bot is online! 😀")

@client.group(invoke_without_command=True)
async def help(ctx):
	em = discord.Embed(title = "Help", description = "View all the different commands", colour = ctx.author.color)
	em.add_field(name = "Moderation Commands", value = "Kick, Ban, Mute, Unmute, Whois")
	em.add_field(name = "\nServer Administration", value = "Clear All, Clear Amount")
	await ctx.send(embed=em)


@client.command(aliases=['cam'])
@commands.has_permissions(manage_messages = True)
async def clear_amount(ctx, amount=2):
	await ctx.channel.purge(limit = amount)

@client.command(aliases=['ca'])
@commands.has_permissions(manage_channels = True)
async def clear_all(ctx):
	await ctx.channel.purge()

@client.command(aliases=['wiu'])
#@commands.has_permissions(kick_members=True)
async def whois(ctx, member : discord.Member):
	embed = discord.Embed(title = member.name, description = member.mention, colour = discord.Colour.green())
	embed.add_field(name = "ID", value = member.id, inline = True)
	embed.set_thumbnail(url = member.avatar_url)
	embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
	await ctx.send(embed=embed)

@client.command(aliases=['k'])
@commands.has_permissions(kick_members = True)
async def kick_user(ctx, member: discord.Member,*, reason="no reason provided"):
	try:
		await member.send("You have been kicked from the Revision Lounge Discord server because",reason)
		await member.send("If you would like to challenge this descision, please DM a dev or moderator.")
	except:
		await ctx.send("The user has their DMs closed.")
	await member.kick(reason=reason)
	await ctx.send(member.mention+ " has been kicked from the server")

@client.command(aliases=['b'])
@commands.has_permissions(ban_members = True)
async def ban_user(ctx, member: discord.Member,*, reason="no reason provided"):
	try:
		await member.send("You have been banned from the Revision Lounge Discord server because",reason)
		await member.send("If you would like to challenge this descision, please DM a dev or moderator.")
		await ctx.send(member.mention+"has been banned from the server because", reason)
		await member.ban(reason=reason)
	except:
		await ctx.send("The user has their DMs closed.")
		await ctx.send(member.mention+"has been banned from the server because", reason)
		await member.ban(reason=reason)
	

@client.command(aliases=['ub'])
@commands.has_permissions(ban_members = True)
async def unban(ctx,*,member):
	banned_users = await ctx.guild.bans()
	member_name, member_disc = member.split('#')
	for banned_entry in banned_users:
		user = banned_entry.user
		if(user.name, user.discriminator) == (member_name, member_disc):
			await ctx.guild.unban(user)
			await member.send("You have been unbanned from the Revision Lounge Discord Server. You may now send messages and use voice chat!")
			await ctx.send(member.mention+" has been unbanned")
			return
	await ctx.send(member.mention+" was not found")

@client.command(aliases=['w'])
@commands.has_permissions(ban_members = True)
async def warn(ctx, member: discord.Member,*, reason="no reason provided"):
	await member.send(f"You have been sent a warning from {ctx.author.name}. The message follows:\n"+reason)
	await ctx.send("Warning sent to "+ member.mention)

@client.command(aliases=['m'])
@commands.has_permissions(kick_members=True)
async def mute(ctx, member:discord.Member):
	muted_role = ctx.guild.get_role(922143814725009458)
	await member.add_roles(muted_role)
	await ctx.send(member.mention + " has been muted.")
	await member.send("You have been muted from the Revision Lounge server. This means you can't send messages or join voice-chat. If you would like to appeal this descision, please DM a moderator or developer.")

@client.command(aliases=['um'])
@commands.has_permissions(kick_members=True)
async def unmute(ctx, member:discord.Member):
	muted_role = ctx.guild.get_role(922143814725009458)
	await member.remove_roles(muted_role)
	await ctx.send(member.mention + " has been unmuted.")
	await member.send("You have been unmuted from the Revision Lounge server. You may now chat and speak with other loungers again! 🥳")

@client.event
async def on_command_error(ctx,error):
	if isinstance(error,commands.MissingPermissions):
		await ctx.send("You don't have the permissions to carry out this command.")
		#await ctx.message.delete()
	elif isinstance(error,commands.MissingRequiredArgument):
		await ctx.send("Please enter all required arguments to carry out this command.")
		#await ctx.message.delete()
	else:
		await ctx.send("Please check that you have the permsissions and that you have spelt everything correctly.\nIf it continues to not work, please DM a developer.")
		#await ctx.message.delete()











client.run(token)