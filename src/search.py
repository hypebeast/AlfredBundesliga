#!/usr/bin/python
# encoding: utf-8

import sys
import datetime

from workflow import Workflow


def parseDateTime(time):
    return datetime.datetime.strptime(time, '%a, %d %b %Y %H:%M:%S %Z')


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
        match = match['Matchdata']
        goalsInfo = ""
        now = datetime.datetime.utcnow()
        matchDate = parseDateTime(match['matchDateTimeUTC'])
        if matchDate > now:
            status = "Starts at: " + matchDate.strftime('%H:%M %d.%m.%Y')
            points = "-:-"
        else:
            if match['matchIsFinished'] == True:
                status = 'Finished'
            else:
                status = 'Running'

            if match['goals'] != None and len(match['goals']) > 0:
                goals = match['goals']
                for goal in goals:
                    goal = goal['Goal']
                    if 'goalGetterName' in goal:
                        goalsInfo += goal['goalGetterName'] + ', '

                goalsInfo = goalsInfo[:-2]
                goalsInfo = '(' + goalsInfo + ')'

            points = str(match['pointsTeam1']) + ":" + str(match['pointsTeam2'])

        title = match['nameTeam1'] + ' - ' + match['nameTeam2']
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
