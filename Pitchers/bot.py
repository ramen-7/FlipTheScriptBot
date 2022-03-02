import discord
import numpy as np
from discord.ext import commands
from discord.utils import get
from discord_slash import SlashCommand
import pandas as pd
from helper_functions import make_embed, generate_team_code


df = pd.read_csv('teams2.csv')
df2 = pd.read_csv('individual.csv')
game = pd.read_csv('game.csv')
participants = pd.read_csv('participants.csv')
register = pd.read_csv('register.csv')
participants.set_index("Name", inplace=True)
game.set_index('Unnamed: 0', inplace=True)
print(game.head(20))
print(participants.head)
print(game.loc['team1','team1'])
r = len(df)
c = len(df.columns)
r2 = len(df2)
intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix='.', intents=intents)
slash = SlashCommand(client, sync_commands=True)


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('creating channels'))
    print("Bot is ready.")


@client.command()
@commands.has_role("Moderator")
async def channel(ctx):
    idg = ctx.message.guild.id
    guild_name = ctx.guild.name
    idc = ctx.channel.category.id
    print(idc)
    idg = int(idg)
    guild = ctx.message.guild
    print(idg)
    print(guild_name)
    category = discord.utils.get(ctx.guild.categories, id=876013167375966288)
    print(category)
    for i in range(r):
        n=df.iloc[i, 0]
        print(n)
        await ctx.guild.create_role(name=df.iloc[i, 0])
        n1 = discord.utils.get(guild.roles, name="Moderator")
        n2 = discord.utils.get(guild.roles, name=n)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            n1: discord.PermissionOverwrite(read_messages=True),
            n2: discord.PermissionOverwrite(read_messages=True)
        }
        await ctx.guild.create_text_channel(df.iloc[i, 0], category=category, overwrites=overwrites)
        await ctx.guild.create_voice_channel(df.iloc[i, 0], category=category, overwrites=overwrites)


@client.command()
@commands.has_role("Moderator")  # This must be exactly the name of the appropriate role
async def addrole(ctx, user: discord.Member, role: discord.Role):
    print(type(user))
    print(user)
    await user.add_roles(role)
    guild = ctx.message.guild
    ro = discord.utils.get(guild.roles, name=role)
    emx = make_embed(text=f"{user.mention} has been given the role {role.mention}")
    await ctx.send(embed=emx)


@client.command()
@commands.has_role("Moderator")
async def autorole(ctx):
    idg = ctx.message.guild.id
    guild = client.get_guild(idg)
    for i in range(r):
        role = df.iloc[i, 0]
        roles = get(ctx.guild.roles, name=role)
        for j in range(1, c):
            name = df.iloc[i, j]
            if type(name) == float:
                continue
            else:
                member = guild.get_member_named(name)
                if member==None:
                    emb = make_embed(text=f"{name} was not found from team {roles.mention}", color=discord.Colour.red())
                    await ctx.send(embed=emb)
                else:
                    await member.add_roles(roles)
                    emx = make_embed(text=f"{member.mention} has been given the role {roles.mention}")
                    print(member.name)
                    await ctx.send(embed=emx)


@client.command()
async def rolerequest(ctx, email):
    channel = client.get_channel(id=876022750286848020)
    idg = ctx.message.guild.id
    guild = client.get_guild(idg)
    core = discord.utils.get(guild.roles, id=870685821957701662)
    for i in range(r2):
        if email == df2.iloc[i, 2]:
            name = df2.iloc[i, 3]
            member = guild.get_member_named(name)
            print(df2.iloc[i, 5])
            role = df2.iloc[i, 5]
            roles = roles = get(ctx.guild.roles, name=role)
            emx = make_embed(text=f"{core.mention} please assign {member.mention} the role {roles.mention}")
            print(member.name)
            await channel.send(embed=emx)


@slash.slash(name='buy_share', description='Buy share of companies using this')
async def buy_share(ctx, buy_share_of: str, quantity: int):
    author = str(ctx.author)
    author_team = participants.loc[author, 'Team']
    print(f"hello {author_team}")
    if quantity <= 10:
        current_shares = game.loc[author_team, buy_share_of]
        if buy_share_of == author_team:
            output = "You cannot buy shares in your own company!"
        elif (current_shares + quantity) > 10:
            output = f"You can only buy 10 shares of a company, please enter an amount less than or equal to {10 - current_shares}"
        else:
            game.loc[author_team, buy_share_of] = game.loc[author_team, buy_share_of] + quantity
            game.loc[buy_share_of, buy_share_of] = game.loc[buy_share_of, buy_share_of] - quantity
            output = f"{author} has bought {quantity} shares in {buy_share_of}"
    else:
        output = "Please enter a value less than 10"
    #outputs of function
    print(game.head(20))
    emx = make_embed(titl="Shares Bought", text=output)
    await ctx.send(embed=emx)

# @slash.slash(name='sell_shares', description='Sell your existing shares')
# async def sell_shares(ctx, sell_share_of: str, quantity: int):
#     author = str(ctx.author)
#     author_team = participants.loc[author, 'Team']
#     current_shares = game.loc[author_team, sell_share_of]


@slash.slash(name='register', description='Register yourself')
async def register(ctx, name: str, email: str, roll_number: int, phone_number: int):
    register = pd.read_csv('register.csv')
    append = pd.DataFrame({'Name': [name], 'Email': [email], 'Roll Number': [roll_number], 'Phone Number': [phone_number], 'Discord Id': [str(ctx.author)]})
    register = pd.concat((register, append), axis=0)
    register.to_csv('register.csv', index=False)
    output = f"""Name: {name}
Email: {email}
Roll Number: {roll_number}
Phone Number: {phone_number}
Discord Id : {ctx.author.mention}
"""
    emx = make_embed(titl='You have been registered! :)', text=output, color=discord.Color.green())
    await ctx.send(embed=emx)


@slash.slash(name='create_team', description='Create your team')
async def create_name(ctx, team_name: str):
    register = pd.read_csv('register.csv')
    code = generate_team_code()
    teams = pd.read_csv('teams.csv')
    append_data = pd.DataFrame({'TeamName':[team_name], 'TeamCode':[code]})
    teams = pd.concat((teams, append_data), axis=0)
    teams.to_csv('teams.csv', index=False)
    output = f"""Team {team_name} has been created
Unique code for team `{code}`
Please share this code with your team mates"""
    emx = make_embed(titl='Team Created!', text=output, color=discord.Color.green())
    register.to_csv('register.csv', index=False)
    await ctx.send(embed=emx)
    await ctx.guild.create_role(name=team_name)
    role = get(ctx.guild.roles, name=team_name)
    print(role)
    await ctx.author.add_roles(role)


@slash.slash(name='join_team', description='Use this command to join your team by entering the team id')
async def join_team(ctx, id: str):
    register = pd.read_csv('register.csv')
    teams = pd.read_csv('teams.csv')
    teamList = list(teams['TeamCode'])
    if id in teamList:
        team_name = teams[teams['TeamCode'] == id].TeamName.item()
        mask = (register['Discord Id'] == str(ctx.author))
        if register.loc[mask, 'Team Name'].isnull().item():
            print("yes")
            register.loc[mask, 'Team Name'] = team_name
            register.to_csv('register.csv', index=False)
            emx = make_embed(titl='Team joined!', text=f'You were able to join team {team_name}', color=discord.Color.green())
            await ctx.send(embed=emx)
            role = get(ctx.guild.roles, name=team_name)
            await ctx.author.add_roles(role)
        else:
            current_team = register.loc[mask, 'Team Name'].item()
            emx = make_embed(titl='Already part of a team', text=f"You are already a part of the team `{current_team}`", color=discord.Color.blue())
            await ctx.send(embed=emx)
    else:
        emx2 = make_embed(titl='Unable to join team :(', text=f'{id} is invalid', color=discord.Color.red())
        await ctx.send(embed=emx2)


@slash.slash(name='display_team', description='Display your team')
async def display_team(ctx, id: str):
    register = pd.read_csv('register.csv')
    teams = pd.read_csv('teams.csv')
    teamList = list(teams['TeamCode'])
    if id in teamList:
        team_name = teams[teams['TeamCode'] == id].TeamName.item()
        mask = register.loc[register['Team Name'] == team_name]
        team_members = list(mask['Discord Id'])
        output = ""
        for members in team_members:
            output = members + "\n" + output
        emx = make_embed(titl='Team Members', text=output, color=discord.Color.blue())
        await ctx.send(embed=emx)
    else:
        emx2 = make_embed(titl='Unable to join team :(', text=f'{id} is invalid', color=discord.Color.red())
        await ctx.send(embed=emx2)


@slash.slash(name='leave_team', description='Use this command to leave your current team')
async def leave_team(ctx):
    register = pd.read_csv('register.csv')
    teams = pd.read_csv('teams.csv')
    mask = register['Discord Id'] == str(ctx.author)
    current_team = register.loc[mask, 'Team Name'].item()
    if register.loc[mask, 'Team Name'].isnull().item():
        emx = make_embed(titl="Invalid Request", text='You are not a part of any team', color=discord.Color.red())
        await ctx.send(embed=emx)
    else:
        register.loc[mask, 'Team Name'] = np.nan
        register.to_csv('register.csv', index=False)
        emx = make_embed(titl="Team Left", text=f'You have successfully left the team `{current_team}`', color=discord.Color.green())
        await ctx.send(embed=emx)

@slash.slash(name='Ping', description='Ping command')
async def ping(ctx):
    await ctx.send("Pong")


client.run('ODIyMTg4NzU2ODUzMDYzNzAw.YFOo8w.k-FbgQcu_eGcMJ_rEfyZ0jMlRqU')
