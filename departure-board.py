#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for
import requests
import json
import datetime
import os

app = Flask(__name__)

global SCHEDULE
global api_key
global STATION_NAME
STATION_NAME = 'Station_1'

#load schedule file at start.  No need to grab every refresh if schedule is static
#could rewrite to pull the schedule dynamically if there is an API or similar with
#dynamic data
with open('sample_schedule.json') as file:
    SCHEDULE = json.load(file)


# TO DO
#look at rewriting getschedule fuction to format output in same fuction
#instead of passing indicies to another fuction
#that way if a transit option has a dynamic way of getting the schedule, you
#only have to pull the data 1x every refresh and not 2x


@app.route('/')
def main():
    #get what station and route to return on the page
    
    # get departure indices and then format the output to pass to HTML page.
    indices = getDepartures()
    formatedSchedule = formatDepartures(indices)
    return render_template('home.html', formatedSchedule = formatedSchedule)



@app.route('/data', methods=['GET', 'POST'])
def data():
    global api_key
    global STATION_NAME

    stationReturn = request.form.get('Dropdown')
    STATION_NAME = stationReturn
    return(redirect(url_for('Station', whatstation = STATION_NAME)))

@app.route('/Station/<whatstation>')
def Station(whatstation):
    STATION_NAME = whatstation

    indices = getDepartures()
    formatedSchedule = formatDepartures(indices)
    return render_template('home.html', formatedSchedule = formatedSchedule)


def getDepartures():
    ROUTE = 'Route_1'
    STATION = STATION_NAME

    #get current time in minutes + current day of the week
    now = datetime.datetime.now()
    h = now.hour
    #print(h)
    m = now.minute
    #print(m)
    timeNow = (h*60) + m
    #print(timeNow)

    #go through json data. Get the indices of the stops that are past the current time
    #the thinking is if i convert the current time and the departure times to
    #minutes since midnight.  Its an easy comparison as i loop through the list
    departure_indices = []
    for i in range(len(SCHEDULE[ROUTE][STATION])):
        time = SCHEDULE[ROUTE][STATION][i]['time']
        if time[-2:] == "PM":
            if int(time[0:2]) == 12:
                depTime = (int(time[0:2])*60) + (int(time[3:5]))
            else:
                depTime = ((int(time[0:2])+12)*60) + (int(time[3:5]))
        else:
            depTime = (int(time[0:2])*60) + (int(time[3:5]))

        if depTime >= timeNow:
            departure_indices.append(i)
    return(departure_indices)

def formatDepartures(indices):
    #Formats a list of 8 items to make sure the board doesnt get overrun if the schedule is long
    # if 8 departures arent avaliable, fils in the blanks with " "

    ROUTE = 'Route_1'
    #STATION = 'Station_1'
    STATION = STATION_NAME
    print("im in get format departures")
    print(STATION)

    departures = []
    for i in range(8):
        if i < len(indices):
            time = SCHEDULE[ROUTE][STATION][indices[i]]['time']
            transit_number = SCHEDULE[ROUTE][STATION][indices[i]]["Transit_Number"]
            #ßßSTATION = 'Station_1'

            text = '  ' + time + '  ' + STATION + '  ' + transit_number
            departures.append(text)

        else:
            departures.append(' ')

    return(departures)


#app.run(debug=True)
#app.run(host='0.0.0.0')
port = int(os.environ.get('PORT', 4000))
app.run(host='0.0.0.0', port=port, debug = False)
