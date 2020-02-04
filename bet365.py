from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.chrome.options import Options


dic = {
    'ATL': 'Atlanta Hawks',
    'BOS': 'Boston Celtics',
    'BKN': 'Brooklyn Nets',
    'CHA': 'Charlotte Hornets',
    'CHI': 'Chicago Bulls',
    'CLE': 'Cleveland Cavaliers',
    'DAL': 'Dallas Mavericks',
    'DEN': 'Denver Nuggets',
    'DET': 'Detroit Pistons',
    'GSW': 'Golden State Warriors',
    'HOU': 'Houston Rockets',
    'IND': 'Indiana Pacers',
    'LA': 'Los Angeles Clippers',
    'LAL': 'Los Angeles Lakers',
    'MEM': 'Memphis Grizzlies',
    'MIA': 'Miami Heat',
    'MIL': 'Milwaukee Bucks',
    'MIN': 'Minnesota Timberwolves',
    'NO': 'New Orleans Pelicans',
    'NY': 'New York Knicks',
    'OKC': 'Oklahoma City Thunder',
    'ORL': 'Orlando Magic',
    'PHI': 'Philadelphia 76ers',
    'PHX': 'Phoenix Suns',
    'POR': 'Portland Trail Blazers',
    'SAC': 'Sacramento Kings',
    'SA': 'San Antonio Spurs',
    'TOR': 'Toronto Raptors',
    'UTA': 'Utah Jazz',
    'WAS': 'Washington Wizards'
}


class Bet365Bot:
    def __init__(self):
        WINDOW_SIZE = "1920,1080"
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def closeBrowser(self):
        self.driver.close()
        self.driver.quit()


    def scrapeNba(self):
        driver = self.driver
        driver.get('https://www.365sport365.com/#/AC/B18/C20604387/D48/E1453/F10/')
        time.sleep(8)
        df = pd.DataFrame(columns=['Date', 'Time', 'Home Team', 'Away Team', 'Bet365 HW', 'Bet365 AW'])
        try:
            findedtimes = driver.find_elements_by_xpath("//div[@class='sl-CouponParticipantGameLineTwoWay_Time ']")
            findeddate = driver.find_element_by_xpath("//div[@class='gll-MarketColumnHeader sl-MarketHeaderLabel sl-MarketHeaderLabel_Date ']")
            findedteams = driver.find_elements_by_xpath("//div[@class='sl-CouponParticipantGameLineTwoWay_NameText ']")
            findednames = driver.find_elements_by_xpath("//span[@class='gll-ParticipantCentered_Name']")
            findedodds = driver.find_elements_by_xpath("//span[@class='gll-ParticipantCentered_Odds']")
            for i in range(1, len(findedtimes)+1):
                upperi = i * 2 - 1
                loweri = upperi - 1
                df = df.append({'Date': findeddate.text, 'Time': findedtimes[i-1].text[:-1] + '0',
                                'Home Team': dic[findedteams[upperi].text.split(" ", 1)[0]], 'Away Team': dic[findedteams[loweri].text.split(" ", 1)[0]],
                                'Bet365 HW': findedodds[upperi + len(findedtimes) * 4].text,
                                'Bet365 AW': findedodds[loweri + len(findedtimes) * 4].text},
                               ignore_index=True)
            print(df)
            print('Bet365 was successful')
            self.closeBrowser()
            return df
        except Exception as e:
            print("Bet365 did not work", format(e))
            self.closeBrowser()
