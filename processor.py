import pandas
import messenger

class Processor:
    def __init__(self, df):
        self.data = df

    def proccess(self):
        data = self.data
        # operators_cols = ['TOPsport HW','TOPsport AW','Optibet HW','Optibet AW','Cbet HW','Cbet AW','Olybet HW','Olybet AW','Unibet HW','Unibet AW','Betsafe HW','Betsafe AW']
        result_cols = ['Report Time', 'Time', 'Home Team', 'Away Team', 'Home Max', 'Away Max', 'Margin', 'Max Home Operator', 'Max Away Operator']
        home_cols = [col for col in data.columns if 'HW' in col]
        away_cols = [col for col in data.columns if 'AW' in col]
        data[home_cols].fillna(0, inplace=True)
        data[away_cols].fillna(0, inplace=True)
        for c in home_cols:
            data[c] = pandas.to_numeric(data[c])
        for c in away_cols:
            data[c] = pandas.to_numeric(data[c])
        data['Home Max'] = data[home_cols].max(axis=1)
        data['Away Max'] = data[away_cols].max(axis=1)
        data['Margin'] = (1 - (1/data['Home Max']) - (1/data['Away Max']))*100
        data['Max Home Operator'] = data[home_cols].idxmax(axis=1)
        data['Max Away Operator'] = data[away_cols].idxmax(axis=1)
        results = data[result_cols]
        return results

    def proccessOpps(self, results):
        opps = results[results['Margin'] > 0]
        if len(opps) > 0:
            for index, row in opps.iterrows():
                if row['Margin'] > 3:
                    msngr = messenger.MessengerBot()
                    msngr.sendMessage(home_operator=row['Max Home Operator'], away_operator=row['Max Away Operator'],
                                      home_odds=row['Home Max'], away_odds=row['Away Max'], home_team=row['Home Team'],
                                      away_team=row['Away Team'], margin=row['Margin'])
