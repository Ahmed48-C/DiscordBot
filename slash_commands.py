#This is the slash commands, when the user writes a slash the commands show up
from settings import TOKEN, GUILD_ID

from typing import Optional, Union
import asyncio

import discord
from discord import app_commands


MY_GUILD = discord.Object(id=GUILD_ID)  # replace with your guild id


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
client = MyClient(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')


@client.tree.command()
async def hello(interaction: discord.Interaction):
    """Says hello!"""
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')


@client.tree.command()
@app_commands.describe(
    first_value='The first value you want to add something to',
    second_value='The value you want to add to the first value',
)
async def add(interaction: discord.Interaction, first_value: int, second_value: int):
    """Adds two numbers together."""
    await interaction.response.send_message(f'{first_value} + {second_value} = {first_value + second_value}')

poll_emojis = ['1⃣','2⃣','3⃣','4⃣','5⃣']
@client.tree.command(name="poll", description="Creates a poll with up to 5 options. (Requires Manage Messages Permission)")
@app_commands.checks.has_permissions(manage_messages=True)
@app_commands.describe(question="What is the question the poll is gonna be asking?", option1="1st option that can be chosen", option2="2nd option that can be chosen", option3="3rd option that can be chosen", option4="4th option that can be chosen",option5="5th option that can be chosen")
async def poll(interaction: discord.Interaction, question: str, option1: str, option2: str, option3:str=None, option4:str=None, option5:str=None,):
    await interaction.response.send_message("Creating poll...", ephemeral=True)
    try:
        listen = [option1, option2, option3, option4, option5]
        yonice = []
        for i in listen:
            if i != None:
                yonice.append(i)

        if len(yonice) == 2:
            emb=discord.Embed(color=discord.Colour.blurple(), title=f"{question}", description=f"Option 1: {yonice[0]}\nOption 2: {yonice[1]}")
            msg=await interaction.channel.send(embed=emb)
            for i in range(len(yonice)):
                await msg.add_reaction(poll_emojis[i])
        elif len(yonice) == 3:
            emb=discord.Embed(color=discord.Colour.blurple(), title=f"{question}", description=f"Option 1: {yonice[0]}\nOption 2: {yonice[1]}\nOption 3: {yonice[2]}")
            msg=await interaction.channel.send(embed=emb)
            for i in range(len(yonice)):
                await msg.add_reaction(poll_emojis[i])
        elif len(yonice) == 4:
            emb=discord.Embed(color=discord.Colour.blurple(), title=f"{question}", description=f"Option 1: {yonice[0]}\nOption 2: {yonice[1]}\nOption 3: {yonice[2]}\nOption 4: {yonice[3]}")
            msg=await interaction.channel.send(embed=emb)
            for i in range(len(yonice)):
                await msg.add_reaction(poll_emojis[i])
        elif len(yonice) == 5:
            emb=discord.Embed(color=discord.Colour.blurple(), title=f"{question}", description=f"Option 1: {yonice[0]}\nOption 2: {yonice[1]}\nOption 3: {yonice[2]}\nOption 4: {yonice[3]}\nOption 5: {yonice[4]}")
            msg=await interaction.channel.send(embed=emb)
            for i in range(len(yonice)):
                await msg.add_reaction(poll_emojis[i])
        await interaction.delete_original_response()
    except Exception as e:
        print(e)
        await interaction.delete_original_response()
        await interaction.followup.send("An error occured, try again later.", ephemeral=True)


@client.tree.command(name='channel-info')
@app_commands.describe(channel='The channel to get info of')
async def channel_info(interaction: discord.Interaction, channel: Union[discord.VoiceChannel, discord.TextChannel]):
    """Shows basic channel info for a text or voice channel."""

    embed = discord.Embed(title='Channel Info')
    embed.add_field(name='Name', value=channel.name, inline=True)
    embed.add_field(name='ID', value=channel.id, inline=True)
    embed.add_field(
        name='Type',
        value='Voice' if isinstance(channel, discord.VoiceChannel) else 'Text',
        inline=True,
    )

    embed.set_footer(text='Created').timestamp = channel.created_at
    await interaction.response.send_message(embed=embed)

# The rename decorator allows us to change the display of the parameter on Discord.
# In this example, even though we use `text_to_send` in the code, the client will use `text` instead.
# Note that other decorators will still refer to it as `text_to_send` in the code.
@client.tree.command()
@app_commands.rename(text_to_send='text')
@app_commands.describe(text_to_send='Text to send in the current channel')
async def send(interaction: discord.Interaction, text_to_send: str):
    """Sends the text into the current channel."""
    await interaction.response.send_message(text_to_send)


# To make an argument optional, you can either give it a supported default argument
# or you can mark it as Optional from the typing standard library. This example does both.
@client.tree.command()
@app_commands.describe(member='The member you want to get the joined date from; defaults to the user who uses the command')
async def joined(interaction: discord.Interaction, member: Optional[discord.Member] = None):
    """Says when a member joined."""
    # If no member is explicitly provided then we use the command user here
    member = member or interaction.user

    # The format_dt function formats the date time into a human readable representation in the official client
    await interaction.response.send_message(f'{member} joined {discord.utils.format_dt(member.joined_at)}')


# A Context Menu command is an app command that can be run on a member or on a message by
# accessing a menu within the client, usually via right clicking.
# It always takes an interaction as its first parameter and a Member or Message as its second parameter.

# This context menu command only works on members
@client.tree.context_menu(name='Show Join Date')
async def show_join_date(interaction: discord.Interaction, member: discord.Member):
    # The format_dt function formats the date time into a human readable representation in the official client
    await interaction.response.send_message(f'{member} joined at {discord.utils.format_dt(member.joined_at)}')

#Error in this code: AttributeError: 'NoneType' object has no attribute 'send'
# # This context menu command only works on messages
# @client.tree.context_menu(name='Report to Moderators')
# async def report_message(interaction: discord.Interaction, message: discord.Message):
#     # We're sending this response message with ephemeral=True, so only the command executor can see it
#     await interaction.response.send_message(
#         f'Thanks for reporting this message by {message.author.mention} to our moderators.', ephemeral=True
#     )

#     # Handle report by sending it into a log channel
#     log_channel = interaction.guild.get_channel(1118441512313835573)  # replace with your channel id

#     embed = discord.Embed(title='Reported Message')
#     if message.content:
#         embed.description = message.content

#     embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
#     embed.timestamp = message.created_at

#     url_view = discord.ui.View()
#     url_view.add_item(discord.ui.Button(label='Go to Message', style=discord.ButtonStyle.url, url=message.jump_url))

#     await log_channel.send(embed=embed, view=url_view)


client.run(TOKEN)