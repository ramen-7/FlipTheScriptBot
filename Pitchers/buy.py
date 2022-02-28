import pandas as pd

def load_data():
    game = pd.read_csv('game.csv')
    participants = pd.read_csv('participants.csv')
    participants.set_index("Name", inplace=True)
    game.set_index('Unnamed: 0', inplace=True)
    print(game.head(20))
    print(participants.head)
    return participants, game

load_data()

def buy_share(quantity, team, author):
    participants, game = load_data()
    output = ""
    author_team = participants.loc[author, team]
    if quantity <=10:
        current_shares = game.loc[author_team, team]
        if (current_shares + quantity) > 10:
            output = f"You can only buy 10 shares of a company, please enter an amount less than or equal to {10-current_shares}"
            return output
        else:
            game.loc[author_team, team] = game.loc[author_team, team] + quantity
            game.loc[team,team] = game.loc[team,team]-quantity
            output = f"{author} has bought {quantity} shares in {team}"
            return output
    else:
        output = "Please enter a value less than 10"
        return output

