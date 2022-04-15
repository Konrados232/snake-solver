import PySimpleGUI as sg

# basic config
sg.theme('DarkGrey5')

# all elements
layout = [  [sg.Text('Some text on Row 1')],
            [sg.Text('Enter something on Row 2'), sg.InputText()],
            [sg.Button('Ok'), sg.Button('Cancel')] ]

for i in range(0,10):
    cells_row = []
    for j in range (0,10):
        cell_name = 'Cell' + str(i) + str(j)
        cells_row.append(sg.Button(cell_name))
        print(cell_name)

    layout.append(cells_row)



window = sg.Window('', layout)


# event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    print('You entered ', values[0])

window.close()

