import untangle
import requests
import datetime
import collections
import os
from shutil import copyfile

#league_url = 'http://www.hbw-hockey.de/VVI-web/Ergebnisdienst/HED-XML.asp?XML=J&saison=FELD19&liga=BAW-JP-MA'

url_template = 'http://www.hbw-hockey.de/VVI-web/Ergebnisdienst/HED-XML.asp?XML=J&saison=FELD19&liga=BAW-{}'

leagues = ['JP-MA', 'JP-WJB', 'JP-MB', 'JP-MJB', 'JP-KB']
tournaments = ['JP-MB', 'JP-KB']
calendar_start_end = collections.namedtuple('StartEnd', 'start, end')
#see format at https://support.google.com/calendar/answer/37118?hl=en
HEADER_LINE = 'Subject, Start Date, Start Time, End Date, End Time, All Day Event, Description, Location \n'
pre_reservation = {}
pre_reservation["JP-MA"]=30
pre_reservation["JP-WJB"]=30
pre_reservation["JP-MJB"]=30
pre_reservation["JP-KB"]=30
pre_reservation["JP-MB"]=30

post_reservation = {}
post_reservation["JP-MA"]=120
post_reservation["JP-WJB"]=120
post_reservation["JP-MJB"]=120
post_reservation["JP-KB"]=30
post_reservation["JP-MB"]=30

game_duration={}
game_duration["JP-MB"]=60
game_duration["JP-KB"]=60

home_games_file = "heimspiele.csv"
away_games_file = "auswaertsspiele.csv"



our_team = 'Karlsruher TV'
home_games_flag = False
headers = 'Subject, Start Date, Start Time, End Date, End Time, All Day Event, Description, Location'
subject = 'MA VL'
all_day_event = 'False'
home_game_description_template = 'Andreas Anpfiff {} - Spiel {}'
away_game_description_template = 'Andreas Anpfiff {} - Spiel {}'
location = 'Platzanlage'

#new_entries = parse_calendar_for_tournament(team_name, calendar_xml, league, home_games_flag)
def parse_calendar_for_tournament(team_name, calendar_xml, league_name, home_games_flag):
    calendar_entries=[]
    key_days = []
    games_of_day={}
    for tag in calendar_xml.Liga.Tag:
        hosting_club = tag.DNAM.cdata
        #print(hosting_club)
        if (our_team in hosting_club):
            print("*** Spieltag ")
            print(tag.DDAG.cdata)
            print(tag.DLFD.cdata)
            key_days.append(tag.DLFD.cdata)
            games_of_day[tag.DLFD.cdata]=[]

    for gruppe in calendar_xml.Liga.Gruppe:
        for spiel in gruppe.Spiel:
            #print(spiel.SDLF.cdata)
            if (spiel.SDLF.cdata in key_days):
                games_of_day[spiel.SDLF.cdata].append(spiel)


    for day in key_days:
        games = games_of_day[day]
        game_date = games[0].SDAG.cdata
        print(f"Es gibt {len(games)} Spiele am {game_date}")
        kickoff_time = datetime.datetime(2099, 2, 1, 12, 12)

        game_ids=[]
        visiting_teams=set()
        for game in games:
            time_kickoff = game.SUHR.cdata
            game_ids.append(game.SNAM.cdata)
            visiting_teams.add(game.STEA.cdata)
            visiting_teams.add(game.STEG.cdata)
            hour = int(time_kickoff.partition(":")[0])
            minutes = int(time_kickoff.partition(":")[-1])
            zeit_zeit = datetime.datetime(2018, 2, 1, hour, minutes)
            kickoff_time = min(kickoff_time, zeit_zeit)

        visiting_teams.remove("Karlsruher TV")
        overall_duration = len(games) * game_duration[league_name] + post_reservation[league_name]
        end_time = kickoff_time + datetime.timedelta(minutes=overall_duration)
        start_time = kickoff_time - datetime.timedelta(minutes = pre_reservation[league_name])

        if (home_games_flag):
            description = home_game_description_template.format(kickoff_time, str(game_ids).replace(',', ';'))
            visitors = str(visiting_teams).replace(',',';')
            line_entry = f"{team_name} - Anpfiff {kickoff_time.time()} - Gast {visitors}, {game_date}, {start_time.time()}, {game_date}, {end_time.time()}, {all_day_event}, {description}, {location}\n"
            print(line_entry)
            calendar_entries.append(line_entry)

    return calendar_entries



def parse_calendar(team_name, calendar_xml, league_name, home_games_flag):
    entries = []
    for gruppe in calendar_xml.Liga.Gruppe:
        for spiel in gruppe.Spiel:
            if (home_games_flag):
                hosting_team_name = str(spiel.STEA.cdata)
                visitor = spiel.STEG.cdata
            else:
                hosting_team_name = str(spiel.STEG.cdata)
                visitor = spiel.STEA.cdata

            if (hosting_team_name == our_team):
                date = spiel.SDAG.cdata
                kickoff_time = spiel.SUHR.cdata
                game_id = spiel.SNAM.cdata

                if (home_games_flag):
                    description = home_game_description_template.format(kickoff_time, game_id)
                    reservation_times = calculate_start_and_end_of_reservation(kickoff_time, league_name)
                    line_entry = f"{team_name} - Anpfiff {kickoff_time} - Gast {visitor}, {date}, {reservation_times.start}, {date}, {reservation_times.end}, {all_day_event}, {description}, {location}\n"
                else:
                    description = away_game_description_template.format(kickoff_time, game_id)
                    reservation_times = calculate_start_and_end_of_reservation(kickoff_time, league_name)
                    line_entry = f"{team_name} - Anpfiff {kickoff_time} - beim {visitor}, {date}, {kickoff_time}, {date}, {reservation_times.end}, {all_day_event}, {description}, {visitor}\n"

                entries.append(line_entry)
                print(line_entry)

    return entries

def retrieve_league_data(leagues, home_games_flag):
    calendar_lines=[]
    calendar_lines.append(HEADER_LINE)
    for league in leagues:
        league_url = url_template.format(league)
        team_name = league.rpartition('-')[-1]
        print(f"Working on team {team_name}")
        response = requests.get(league_url)
        file_name = f"{team_name}.xml"
        with open(file_name, "w") as text_file:
            text_file.write(response.text)

        calendar_xml = untangle.parse(file_name)
        if (league in tournaments):
            print(f"{league} hat Turnierbetrieb!")
            new_entries = parse_calendar_for_tournament(team_name, calendar_xml, league, home_games_flag)
            calendar_lines = calendar_lines + new_entries
        else:
            new_entries = parse_calendar(team_name, calendar_xml, league, home_games_flag)
            calendar_lines = calendar_lines + new_entries

    if (home_games_flag):
        current_games_file = home_games_file
    else:
        current_games_file = away_games_file

    # copy away old status so we can compare
    old_file_name = "old_" + current_games_file
    old_entries=[]
    if (os.path.isfile(current_games_file)):
        copyfile(current_games_file, old_file_name)
        with open(current_games_file) as f:
                old_entries = f.readlines()

    # write the new status.
    with open(current_games_file, "w") as text_file:
        for line in calendar_lines:
            text_file.write(line)

    old_set = set(old_entries)
    new_set = set(calendar_lines)
    if (old_set == new_set):
        print("nüscht neues")
    else:
        result = set.intersection(old_set, new_set)
        new_entries = new_set - result
        print("******** neue Einträge")
        for entry in new_entries:
            print(entry)
        print("******** neue Einträge")




def calculate_start_and_end_of_reservation(time_kickoff : str, league : str, number_of_games=0):
    if not time_kickoff:
        return calendar_start_end("00:00", "00:00")
    hour = int(time_kickoff.partition(":")[0])
    minutes = int(time_kickoff.partition(":")[-1])
    zeit_zeit = datetime.datetime(2018, 2, 1, hour, minutes)
    start = zeit_zeit - datetime.timedelta(minutes=pre_reservation[league])
    playing_duration = game_duration.get(league, 0) * number_of_games
    end = zeit_zeit + datetime.timedelta(minutes=post_reservation[league] + playing_duration)
    return calendar_start_end(start=start.time(), end=end.time())


retrieve_league_data(leagues, True)
#retrieve_league_data(leagues, False)
#calendar_xml = untangle.parse("KB.xml")
#result = parse_calendar_for_tournament(calendar_xml, True, "JP-KB", "KB")
#print(result)