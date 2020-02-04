from fbchat import Client
from fbchat.models import *


class MessengerBot:
    def __init__(self):
        self.client = Client('YOUR FB USERNAME', 'YOUR FB PASSWORD')

    def logout(self):
        self.client.logout()

    def sendMessage(self, home_operator, away_operator, home_odds, away_odds, home_team, away_team, margin):
        self.client.send(Message(text=f'{home_operator} | {home_team} | {home_odds} ------ {away_operator} | {away_team} | {away_odds} ------'
                                      f' Margin: {margin}'),
                         thread_id=self.client.uid, thread_type=ThreadType.USER)
