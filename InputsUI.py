import PySimpleGUI as sg

sg.theme('DarkGrey14') 
times = ["12:00 AM", "12:30 AM", "1:00 AM", "1:30 AM", "2:00 AM", "2:30 AM", "3:00 AM", "3:30 AM", "4:00 AM", "4:30 AM", "5:00 AM", "5:30 AM", "6:00 AM", "6:30 AM", 
"7:00 AM", "7:30 AM", "8:00 AM", "8:30 AM", "9:00 AM", "9:30 AM", "10:00 AM", "10:30 AM", "11:00 AM", "11:30 AM", "12:00 PM", "12:30 PM", "1:00 PM", "1:30 PM",
"2:00 PM", "2:30 PM", "3:00 PM", "3:30 PM", "4:00 PM", "4:30 PM", "5:00 PM", "5:30 PM", "6:00 PM", "6:30 PM", "7:00 PM", "7:30 PM", "8:00 PM", "8:30 PM", "9:00 PM",
"9:30 PM", "10:00 PM", "10:30 PM", "11:00 PM", "11:30 PM"] 
party_sizes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]

layout = [
    [sg.Text("Find Your Table", justification="center", size=(45,1), font=("Source Sans Bold", 25))],
    [sg.Text("")],
    [sg.CalendarButton("Date", font=("Source Sans Bold", 14), close_when_date_chosen=True,  target='-IN-', no_titlebar=False, format='%b %d, %Y' ), sg.Input(key='-IN-', size=(15,1), font=("Source Sans Bold", 14)), 
    sg.Text("Time", font=("Source Sans Bold", 14)), sg.Combo(times, font=("Source Sans Bold", 14)), sg.Text("Party Size", font=("Source Sans Bold", 14)), sg.Combo(party_sizes, font=("Source Sans Bold", 14)), sg.Text("Neighborhood", font=("Source Sans Bold", 14)), sg.InputText(size=(15,1), font=("Source Sans Bold", 14))],
    [sg.Text("")],
    [sg.Exit(font=("Source Sans Bold", 14))]
    ]

window = sg.Window('Reservation Details', layout)

while True:
    event, values = window.read()
    print(event, values)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
window.close()