import untangle
import requests

league_url = 'http://www.hbw-hockey.de/VVI-web/Ergebnisdienst/HED-XML.asp?XML=J&saison=FELD19&liga=BAW-JP-MA'
#             http://www.hbw-hockey.de/VVI-web/Ergebnisdienst/HED-XML.asp?XML=J&saison=FELD19&liga=BAW-JP-WJB
#             http://www.hbw-hockey.de/VVI-web/Ergebnisdienst/HED-XML.asp?XML=J&saison=FELD19&liga=BAW-JP-MB
#             http://www.hbw-hockey.de/VVI-web/Ergebnisdienst/HED-XML.asp?XML=J&saison=FELD19&liga=BAW-JP-MJB
#             http://www.hbw-hockey.de/VVI-web/Ergebnisdienst/HED-XML.asp?XML=J&saison=FELD19&liga=BAW-JP-KB

url_template = 'http://www.hbw-hockey.de/VVI-web/Ergebnisdienst/HED-XML.asp?XML=J&saison=FELD19&liga=BAW-{}'

leagues = ['JP-MA', 'JP-WJB', 'JP-MB', 'JP-MJB', 'JP-KB']
tournaments = ['JP-MB', 'JP-KB']




our_team = 'Karlsruher TV'
home_games = True
headers = 'Subject, Start Date, Start Time, End Date, End Time, All Day Event, Description, Location'
subject = 'MA VL'
all_day_event = 'False'
description_template = 'Andreas Anpfiff {} - Spiel {}'
location = 'Platzanlage'

def parse_calendar(xml_content, team_name, file_name):
    calendar_xml = untangle.parse(file_name)
    for gruppe in calendar_xml.Liga.Gruppe:
        for spiel in gruppe.Spiel:
            hosting_team_name = str(spiel.STEA.cdata)
            if (hosting_team_name == our_team):
                date = spiel.SDAG.cdata
                visitor = spiel.STEG.cdata
                kickoff_time = spiel.SUHR.cdata
                game_id = spiel.SNAM.cdata
                description = description_template.format(kickoff_time, game_id)
                line_entry = f"{team_name}, {date}, {kickoff_time}, {date}, {kickoff_time}, {all_day_event}, {description}, {location}"
                print(line_entry)

def retrieve_league_data(leagues):
    for league in leagues:
        league_url = url_template.format(league)
        team_name = league.rpartition('-')[-1]
        response = requests.get(league_url)
        file_name = f"{team_name}.xml"
        with open(file_name, "w") as text_file:
            text_file.write(response.text)

        if (league in tournaments):
            print(f"{league} hat Turnierbetrieb!")
        else:
            parse_calendar(response.text, team_name, file_name)

retrieve_league_data(leagues)

