import webbrowser
import json, requests, time
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import cloudscraper
import urllib.parse
import re

# enter steamid of your friends
friends = []


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
    
    global friends
    
    
    for i in steam64:
        if i in friends:
            continue
        url = 'https://csgostats.gg/player/'+str(i)
        webbrowser.get('chrome').open(url)
    
def find_rank(steam64id):
    
    global friends

    for id in steam64id:
        if id not in friends:
            url = 'https://csgo-stats.com/player/' + str(id)

            r = requests.get(url=url, )
            soup = BeautifulSoup(r.text, 'lxml')

            rank = soup.find('span', class_='rank-name')
            name = soup.find('div', class_='title-card')
            print("{} : {}".format(name.h1.text,rank.text))


def find_rank_new(steam64id):
    
    global friends
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

def take_input_val():
    s = ""
    ign = []
    while (s!="#end"):
        s = input()
        ign.append(s)
    return ign[:-1]


def find_rank_val(ign):
    tb = PrettyTable()
    rows = []
    tb.field_names = ['Name', 'Rank', 'Best', 'Hours', 'Matches', 'WR', 'MainAgent']

    # TODO: add exception handling when ign doesn't exist or haven't signed up for tracker.gg
    url_placeholder = []
    #ign cant contain '#', according to https://riotidsymbols.com/
    for names in ign:
        # TODO: replace space too
        names = urllib.parse.quote_plus(names)
        url_placeholder.append(names)
        # print(url_placeholder)

    table_rows = []

    # to reference names from list ign
    count = 0

    for placeholder in url_placeholder:
        url = 'https://tracker.gg/valorant/profile/riot/{}/overview?playlist=competitive'.format(placeholder)

        flag = False
        while not flag:
            try:
                sc = cloudscraper.create_scraper()
                html_text = sc.get(url).text
                flag = True
            except:
                time.sleep(2)
                continue
                # waits until scraper starts? bottleneck?
        
        soup = BeautifulSoup(html_text, 'lxml')
        # rank - div class = 'rating-entry__info' - parent, div class = 'value' inside
        rank_div = soup.find_all('div', {'class': 'rating-entry__info'})
        rank_texts = []
        for i in rank_div:
            s = i.get_text()
            s = re.sub(r"[\n\t\s]*", "", s)
            rank_texts.append(s)
        
        rank = rank_texts[0][6:]
        best_rank = rank_texts[1]

        # matches and hours
        title_stats = soup.find('div', {'class': 'title-stats'})
        title_stats_text = re.sub(r"[\n\t\s]*", "", title_stats.get_text())
        hours = title_stats_text[:title_stats_text.index('h')]
        matches = title_stats_text[title_stats_text.find('Time') + 4 : -7]

        # WR
        win_ratio_span = soup.find('span', {'title': 'Win %'})
        win_ratio_span_parent_text = win_ratio_span.find_parent().get_text()
        win_ratio_span_parent_text = re.sub(r"[\n\t\s]*", "", win_ratio_span_parent_text)

        # rat's nest, basically finds the text b/w the first '%' and the second '%' signs
        win_ratio = win_ratio_span_parent_text[4 : (win_ratio_span_parent_text[5 : ]).index('%') + 5]

        # main agent
        agent_name = soup.find('span', {'class': 'agent__name'})
        main_agent = agent_name.get_text()

        # adding to prettytable's rows
        rows.append([ign[count], rank, best_rank, hours, matches, win_ratio, main_agent])
        count += 1

    tb.add_rows(rows)
    print(tb)


        
            
        


# reveal_rank(take_input())
# find_rank(take_input())

# TODO: run this to find csgo rank
# find_rank_new(take_input())


game = input("csgo/val (c/v)?: " )
if game == 'c':
    print("Paste")
    find_rank_new(take_input())

elif game == 'v':
    print("Paste")
    find_rank_val(take_input_val())
else:
    print("exiting")
    exit(1)

