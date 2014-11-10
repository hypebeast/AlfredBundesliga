#!/usr/bin/python
# encoding: utf-8

import sys
import datetime

from workflow import Workflow


def parseDateTime(time):
    return datetime.datetime.strptime(time[:-6], '%Y-%m-%dT%H:%M:%S')


def getCurrentResults(bundesliga):
    matchday = bundesliga.getNextMatchday()
    matches = bundesliga.getMatchdayResults(matchday)
    processMatches(matches)


def getRecentResults(bundesliga):
    matchday = bundesliga.getRecentMatchday()
    matches = bundesliga.getMatchdayResults(matchday)
    processMatches(matches)


def processMatches(matches):
    if matches == None:
        return

    for match in matches:
        goalsInfo = ""
        now = datetime.datetime.utcnow()
        matchDate = parseDateTime(match['match_date_time_utc'])
        if matchDate > now:
            status = "Starts at: " + matchDate.strftime('%H:%M %d.%m.%Y')
            points = "-:-"
        else:
            if match['match_is_finished'] == True:
                status = 'Finished'
            else:
                status = 'Running'

            if match['goals'] != None and match['goals']['goal'] != None:
                goals = match['goals']['goal']
                for goal in goals:
                    if 'goal_getter_name' in goal:
                        goalsInfo += goal['goal_getter_name'] + ', '

                goalsInfo = goalsInfo[:-2]
                goalsInfo = '(' + goalsInfo + ')'

            points = match['points_team1'] + ":" + match['points_team2']

        title = match['name_team1'] + ' - ' + match['name_team2']
        subtitle = points + '   ' + status + '  ' + goalsInfo
        wf.add_item(title=title,
                    subtitle=subtitle)

def getTable(bundesliga):
    table = bundesliga.getTable(bundesliga.getSeason())

    rank = 1
    for team in table:
        title = "%d. %s" % (rank, team['team_name'])

        wins = team['wins']
        draws = team['draws']
        losses = team['losses']
        goals = team['goals']
        received_goals = team['received_goals']
        goals_difference = goals - received_goals
        points = team['points']
        subtitle = "W: %d D: %d L: %d, G: %d:%d, GD: %d, Pts: %d" % (wins,
                                                                    draws,
                                                                    losses,
                                                                    goals,
                                                                    received_goals,
                                                                    goals_difference,
                                                                    points)

        rank += 1
        wf.add_item(title=title,
                    subtitle=subtitle)

def main(wf):
    from bundesliga import Bundesliga

    if len(wf.args):
        command = wf.args[0]
    else:
        command = 'next'

    bundesliga = Bundesliga()

    if command == 'next':
        getCurrentResults(bundesliga)
    elif command == 'recent':
        getRecentResults(bundesliga)
    elif command == 'table':
        getTable(bundesliga)

    # Send output to Alfred
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
