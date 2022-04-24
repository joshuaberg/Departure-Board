#!/usr/bin/env python3
from flask import Flask , render_template, request, redirect
import requests
import json
import datetime

app = Flask(__name__)

@app.route('/')
def main():

    # get departure indices and then format the output to pass to HTML page.
    indices = getDepartures()
    formatedSchedule = formatDepartures(indices)
    return render_template('home.html', formatedSchedule = formatedSchedule)


def getDepartures():
    ROUTE = 'Route_1'
    STATION = 'Station_1'
    #get current time in minutes + current day of the week
    now = datetime.datetime.now()
    h = now.hour
    m = now.minute
    timeNow = (h*60) + m

    #print(time_now)
    with open('sample_schedule.json') as file:
        parsed_json = json.load(file)

        #go through json data. Get the indices of the stops that are past the current time
        #the thinking is if i convert the current time and the departure times to
        #minutes since midnight.  ITs an eas comparison as i loop through the list
        departure_indices = []
        for i in range(len(parsed_json[ROUTE][STATION])):
            time = parsed_json[ROUTE][STATION][i]['time']
            if time[-2:] == "PM":
                if int(time[0:2]) == 12:
                    depTime = (int(time[0:2])*60) + (int(time[3:5]))
                else:
                    depTime = (int(time[0:2])*60) + (int(time[3:5])) + (12*60)
            else:
                depTime = (int(time[0:2])*60) + (int(time[3:5]))

            if depTime >= timeNow:
                departure_indices.append(i)
    return(departure_indices)

def formatDepartures(indices):
    #Formats a list of 8 items to make sure the board doesnt get overrun if the schedule is long
    # if 8 departures arent avaliable, fils in the blanks with " "

    ROUTE = 'Route_1'
    STATION = 'Station_1'
    with open('sample_schedule.json') as file:
        parsed_json = json.load(file)

    departures = []
    for i in range(8):
        if i < len(indices):
            time = parsed_json[ROUTE][STATION][i]['time']
            transit_number = parsed_json[ROUTE][STATION][i]["Transit_Number"]
            STATION = 'Station_1'

            text = '  ' + time + '  ' + STATION + '  ' + transit_number
            departures.append(text)

        else:
            departures.append(' ')

    return(departures)


#app.run(debug=True)
app.run()
