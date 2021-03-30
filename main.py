import discord
from discord.ext import commands

from local import discord_token

bot_client = commands.Bot(command_prefix='?')

@bot_client.command()
async def mute(ctx, member: discord.Member, reason="None given"):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

    if not muted_role:
        muted_role = await ctx.guild.create_role(name="Muted")

        for channel in ctx.guild.channels:
            await channel.set_permissions(muted_role, speak=False, send_messages=False, add_reactions=False)

    await member.add_roles(muted_role, reason=reason)
    await member.send(f"You have been muted in {ctx.guild.name} for {reason}.")
    await ctx.send(f"{member.name} has been muted.")
    

@bot_client.command()
async def unmute(ctx, member: discord.Member):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(muted_role)
    await member.send(f"You have been unmuted in {ctx.guild.name}.")
    await ctx.send(f"{member.name} has been unmuted.")

@bot_client.command()
async def get_role(ctx, name):
    role = discord.utils.get(ctx.guild.roles, name=name)

    if not role:
        await ctx.send(f"{name} is not a role.")
        return

    await ctx.author.add_roles(role)
    await ctx.author.send(f"You have been given the {role.name} role in {ctx.guild.name}.")
    await ctx.send(f"{ctx.author.name} has been giving the role {role.name}.")

@bot_client.command()
async def remove_role(ctx, name):
    role = discord.utils.get(ctx.guild.roles, name=name)

    if not role:
        await ctx.send(f"{name} is not a role.")
        return
        
    await ctx.author.remove_roles(role)
    await ctx.author.send(f"The role {role.name} has been removed in {ctx.guild.name}.")
    await ctx.send(f"The role {role.name} has been removed from {ctx.author.name}.")

@bot_client.command()
async def give_role(ctx, member: discord.Member, name):
    if discord.utils.get(ctx.guild.roles, name="admin") not in ctx.author.roles:
        await ctx.send(f"You must be an admin to use this command.")
        return

    role = discord.utils.get(ctx.guild.roles, name=name)

    if not role:
        await ctx.send(f"{name} is not a role.")
        return

    await member.add_roles(role)
    await member.send(f"You have been given the role {role.name} in {ctx.guild.name}.")
    await ctx.send(f"The role {role.name} has been given to {member.name}.")

@bot_client.command()
async def take_role(ctx, member: discord.Member, name):
    if discord.utils.get(ctx.guild.roles, name="admin") not in ctx.author.roles:
        await ctx.send(f"You must be an admin to use this command.")
        return

    role = discord.utils.get(ctx.guild.roles, name=name)

    if not role:
        await ctx.send(f"{name} is not a role.")
        return

    await member.remove_roles(role)
    await member.send(f"The role {role.name} has been taken in {ctx.guild.name}.")
    await ctx.send(f"The role {role.name} has been taken from {member.name}.")

bot_client.run(discord_token)
