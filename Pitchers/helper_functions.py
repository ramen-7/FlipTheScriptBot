import discord
import pandas as pd
from random import choice
from string import ascii_uppercase



teams = pd.read_csv('teams.csv')
print(teams.head())

def make_embed(text, titl, color=discord.Colour.blue(), url=None):
    embed = discord.Embed(color=color, description=text, title=titl)
    if url != None:
        embed.set_image(url=f"{url}")
    return embed

def generate_team_code():
    code = ''.join(choice(ascii_uppercase) for i in range(12))
    if code not in teams['TeamCode']:
        return code
    else:
        return generate_team_code()