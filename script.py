import bet365
import topsport
import optibet
import cbet
import olybet
import unibet
import betsafe
import pandas
import os
from functools import reduce
import processor

# bet365bot = bet365.Bet365Bot()
topbot = topsport.TOPsportBot()
optibot = optibet.OptibetBot()
cbetbot = cbet.CbetBot()
olybetbot = olybet.OlybetBot()
unibetbot = unibet.UnibetBot()
betsafebot = betsafe.BetsafeBot()

nbadfs = [topbot.scrapeNba(), betsafebot.scrapeNba(), optibot.scrapeNba(), cbetbot.scrapeNba(),
           olybetbot.scrapeNba(), unibetbot.scrapeNba()]
realenbadfs = []

for df in nbadfs:
    if df is not None:
        realenbadfs.append(df)

nba_merged = reduce(lambda left,right: pandas.merge(left,right,on=['Home Team', 'Away Team'],
                                            how='left'), realenbadfs)
print(nba_merged)


# data = mergeddf.copy()
#
# operators_cols = ['TOPsport HW','TOPsport AW','Optibet HW','Optibet AW','Cbet HW','Cbet AW','Olybet HW','Olybet AW','Unibet HW','Unibet AW','Betsafe HW','Betsafe AW']
# result_cols = ['Report Time', 'Time', 'Home Team', 'Away Team', 'Home Max', 'Away Max', 'Margin', 'Max Home Operator', 'Max Away Operator']
# home_cols = [col for col in data.columns if 'HW' in col]
# away_cols = [col for col in data.columns if 'AW' in col]
# for c in operators_cols:
#     data[c] = pandas.to_numeric(data[c])
# data['Home Max'] = data[home_cols].max(axis=1)
# data['Away Max'] = data[away_cols].max(axis=1)
# data['Margin'] = (1 - (1/data['Home Max']) - (1/data['Away Max']))*100
# data['Max Home Operator'] = data[home_cols].idxmax(axis=1)
# data['Max Away Operator'] = data[away_cols].idxmax(axis=1)
# results = data[result_cols]
# print(results)

# mergeddf.to_csv('odds.csv')
# results.to_csv('odds_results.csv')
#
# dir_path = os.path.dirname(os.path.abspath(__file__))
# mergeddf.to_csv(os.path.join(dir_path, 'odds.csv'), mode='a', header=False)
# results.to_csv(os.path.join(dir_path, 'odds_results.csv'), mode='a', header=False)

# opps = results[results['Margin'] > 0]
# if len(opps) > 0:
#     for index, row in opps.iterrows():
#         if row['Margin'] > 3:
#             msngr = messenger.MessengerBot()
#             msngr.sendMessage(home_operator=row['Max Home Operator'], away_operator=row['Max Away Operator'],
#                               home_odds=row['Home Max'], away_odds=row['Away Max'], home_team=row['Home Team'],
#                               away_team=row['Away Team'], margin=row['Margin'])

topbot = topsport.TOPsportBot()
optibot = optibet.OptibetBot()
cbetbot = cbet.CbetBot()
olybetbot = olybet.OlybetBot()
unibetbot = unibet.UnibetBot()
betsafebot = betsafe.BetsafeBot()

eurodfs = [topbot.scrapeEuroleague(), betsafebot.scrapeEuroleague(), optibot.scrapeEuroleague(), cbetbot.scrapeEuroleague(),
           olybetbot.scrapeEuroleague(), unibetbot.scrapeEuroleague()]
realeurodfs = []

for df in eurodfs:
    if df is not None:
        realeurodfs.append(df)

euroleague_merged = reduce(lambda left,right: pandas.merge(left,right,on=['Home Team', 'Away Team'],
                                            how='left'), realeurodfs)
print(euroleague_merged)

nbaprocessor = processor.Processor(df=nba_merged.copy())
nba_results = nbaprocessor.proccess()
nbaprocessor.proccessOpps(results=nba_results)

euroleague_processor = processor.Processor(df=euroleague_merged.copy())
euroleague_results = euroleague_processor.proccess()
nbaprocessor.proccessOpps(results=euroleague_results)

dir_path = os.path.dirname(os.path.abspath(__file__))
if os.path.exists(os.path.join(dir_path, 'nba_odds.csv')):
    nba_merged.to_csv(os.path.join(dir_path, 'nba_odds.csv'), mode='a', header=False)
    nba_results.to_csv(os.path.join(dir_path, 'nba_odds_results.csv'), mode='a', header=False)
else:
    nba_merged.to_csv('nba_odds.csv')
    nba_results.to_csv('nba_odds_results.csv')

if os.path.exists(os.path.join(dir_path, 'euroleague_odds.csv')):
    euroleague_merged.to_csv(os.path.join(dir_path, 'euroleague_odds.csv'), mode='a', header=False)
    euroleague_results.to_csv(os.path.join(dir_path, 'euroleague_odds_results.csv'), mode='a', header=False)
else:
    euroleague_merged.to_csv('euroleague_odds.csv')
    euroleague_results.to_csv('euroleague_odds_results.csv')