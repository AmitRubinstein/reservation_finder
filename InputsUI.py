import PySimpleGUI as sg
import datetime

sg.theme('DarkGrey11') 

def errorWindow(error_message):
    layout = [
        [sg.Text(error_message, font=("Source Sans Bold", 14))]
    ]

    window = sg.Window("Error", layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
    window.close()

def addZeroPadding(time_input):
    if len(time_input) == 7:
        time_input = "0" + time_input
    return time_input

def formatCurrentTime(time_input):
    time_input = list(time_input)
    hour = int("".join(time_input[0:2]))
    minutes = "".join(time_input[3:5])
    ampm = "".join(time_input[6:8])
    if minutes != "00" and int(minutes) < 30:
        time_input[3] = "3"
        time_input[4] = "0"
    elif minutes != "00" and int(minutes) > 30:
        time_input[3] = "0"
        time_input[4] = "0"
        hour = hour + 1
        if hour == 12 and ampm == "AM":
            time_input[6] = "P"
        elif hour == 12 and ampm == "PM":
            time_input[6] = "A"
        elif hour > 12:
            hour = hour - 12
        if hour >= 10:
            time_input[0] = str(hour)[0]
            time_input[1] = str(hour)[1]
        else:
            time_input[0] = "0"
            time_input[1] = str(hour)[0]
    if time_input[0] == "0":
        time_input = time_input[1:]
    return "".join(time_input)

def UserInput():
    times = ["12:00 AM", "12:30 AM", "1:00 AM", "1:30 AM", "2:00 AM", "2:30 AM", "3:00 AM", "3:30 AM", "4:00 AM", "4:30 AM", "5:00 AM", "5:30 AM", "6:00 AM", "6:30 AM", 
    "7:00 AM", "7:30 AM", "8:00 AM", "8:30 AM", "9:00 AM", "9:30 AM", "10:00 AM", "10:30 AM", "11:00 AM", "11:30 AM", "12:00 PM", "12:30 PM", "1:00 PM", "1:30 PM",
    "2:00 PM", "2:30 PM", "3:00 PM", "3:30 PM", "4:00 PM", "4:30 PM", "5:00 PM", "5:30 PM", "6:00 PM", "6:30 PM", "7:00 PM", "7:30 PM", "8:00 PM", "8:30 PM", "9:00 PM",
    "9:30 PM", "10:00 PM", "10:30 PM", "11:00 PM", "11:30 PM"] 
    party_sizes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]

    layout = [
        [sg.Text("Find Your Table", justification="center", size=(45,1), font=("Source Sans Bold", 25))],
        [sg.Text("")],
        [sg.CalendarButton("Date", font=("Source Sans Bold", 14), close_when_date_chosen=True, target="date_input", no_titlebar=False, format='%m/%d/%Y'), sg.Input(key="date_input", size=(15,1), font=("Source Sans Bold", 14), default_text=datetime.datetime.now().strftime("%m/%d/%Y")), 
        sg.Text("Time", font=("Source Sans Bold", 14)), sg.Combo(times, font=("Source Sans Bold", 14), key="time_input", readonly=True, default_value=formatCurrentTime(datetime.datetime.now().strftime("%I:%M %p"))), sg.Text("Party Size", font=("Source Sans Bold", 14)), 
        sg.Combo(party_sizes, font=("Source Sans Bold", 14), key="party_input", readonly=True, default_value=2), sg.Text("Neighborhood", font=("Source Sans Bold", 14)), sg.Input(size=(15,1), font=("Source Sans Bold", 14), key="hood_input", tooltip="Example: Murray Hill")],
        [sg.Text("")],
        [sg.Button("Submit", font=("Source Sans Bold", 14)), sg.Exit(font=("Source Sans Bold", 14))]
        ]

    window = sg.Window('Reservation Details', layout)

    #Loop for open UI window
    while True:
        event, values = window.read()
        if event == "Submit":
            #date = values["date_input"]
            #time = values["time_input"]
            #party_size = values["party_input"]
            #hood = values["hood_input"]
            values.pop("Date")
            if "" in values.values():
                errorWindow("Please complete all the fields")
            else:
                try:
                    datetime.datetime.strptime(values["date_input"], "%m/%d/%Y")
                except:
                    errorWindow("Please enter a valid date format \"MM/DD/YYYY\" ")
                    continue
                if datetime.datetime.strptime(values["date_input"]+" "+addZeroPadding(values["time_input"]), "%m/%d/%Y %I:%M %p") < datetime.datetime.now():
                    values["date_input"] = datetime.datetime.now().strftime("%m/%d/%Y")
                    values["time_input"] = formatCurrentTime(datetime.datetime.now().strftime("%I:%M %p"))
                    break
                else:
                    break
        if event in (sg.WIN_CLOSED, 'Exit'):
            quit()
    window.close()
    
    #print(date)
    #print(time)
    #print(party_size)
    #print(hood)

def main():
    UserInput()

if __name__ == "__main__":
    main()