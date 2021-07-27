import webbrowser
import json, requests, time
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import cloudscraper


def steamid_to_64bit(steamid):
    steam64id = 76561197960265728 # kinda Seed                                 
    id_split = steamid.split(":")
    try:
        steam64id += int(id_split[2]) * 2 
    except:
        return 76561198404529974
    if id_split[1] == "1":
        steam64id += 1
    return steam64id

def take_input():
    s=""
    res=""
    n=0
    steam_id = []
    while(s!="#end"):
        s = input()
        res+='\n'
        res+=s
        n+=1
    for i in range(2,n):
        try:
            steam_id.append(res.split('\n')[i].split()[-6])
        except:
            continue
    steam64 = set()
    for i in steam_id:
        steam64.add(steamid_to_64bit(i))
    return steam64


def reveal_rank(steam64):
    webbrowser.register('chrome',
        None,
        webbrowser.BackgroundBrowser("C://Program Files//Google//Chrome//Application//chrome.exe")
        )
    
    friends = [76561198404529974,76561198816159059, 76561198430918852, 76561198435814829, 76561198807553119, 76561198405059981, 76561198059938292, 76561198401931678]
    
    
    for i in steam64:
        if i in friends:
            continue
        url = 'https://csgostats.gg/player/'+str(i)
        webbrowser.get('chrome').open(url)
    
def find_rank(steam64id):
    
    friends = [76561198404529974,76561198816159059, 76561198430918852, 76561198435814829, 76561198807553119, 76561198405059981, 76561198059938292, 76561198401931678]

    for id in steam64id:
        if id not in friends:
            url = 'https://csgo-stats.com/player/' + str(id)

            r = requests.get(url=url, )
            soup = BeautifulSoup(r.text, 'lxml')

            rank = soup.find('span', class_='rank-name')
            name = soup.find('div', class_='title-card')
            print("{} : {}".format(name.h1.text,rank.text))


def find_rank_new(steam64id):
    
    friends = [76561198404529974,76561198816159059, 76561198430918852, 76561198435814829, 76561198807553119, 76561198405059981, 76561198059938292, 76561198401931678]
    rows = []
    tb = PrettyTable()

    for id in steam64id:
        if id not in friends:
            url = 'https://csgostats.gg/player/' + str(id)

            ranks = {
                "1":"S1",
                "2":"S2",
                "3":"S3",
                "4":"S4",
                "5":"SE",
                "6":"SEM",
                "7":"GN1",
                "8":"GN2",
                "9":"GN3",
                "10":"GNM",
                "11":"MG1",
                "12":"MG2",
                "13":"MGE",
                "14":"DMG",
                "15":"LE",
                "16":"LEM",
                "17":"SMFC",
                "17":"GE"
            }
            flag = False
            while not flag:
                try:
                    sc = cloudscraper.create_scraper()
                    html_text = sc.get(url).text
                    flag = True
                except:
                    time.sleep(2)
                    continue
            soup = BeautifulSoup(html_text, 'lxml')
            rank = soup.find('div', style="float:right; width:92px; height:120px; padding-top:56px; margin-left:32px;")
            wins = soup.find('span', id='competitve-wins')
            name = soup.find('div', id='player-name')

            try:
                player = name.text
            except:
                player = "Unknown"
            try:
                curr_rank = ranks[rank.img['src'].split('/')[-1].split('.')[0]]
            except:
                curr_rank = "Unknown"
            try:
                best_rank = ranks[rank.div.img['src'].split('/')[-1].split('.')[0]]
            except:
                best_rank = "Unknown"
            try:
                total_wins = wins.span.text
            except:
                total_wins = "Unknown"

            rows.append([player, curr_rank, best_rank, total_wins])
            # print("{:<25}[Rank : {:<5}] [Best : {:<5}] [Wins : {:<5}]".format(player,curr_rank,best_rank,total_wins))

    tb.field_names = ['Name', 'Rank', 'Best', 'Wins']
    tb.add_rows(rows)
    print(tb)


# reveal_rank(take_input())
# find_rank(take_input())
find_rank_new(take_input())