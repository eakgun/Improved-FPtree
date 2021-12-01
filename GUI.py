import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import R
from igraph.layout import Layout
from main import *
from fpGrowth import *

left_layout = [[sg.Text("Choose a dataset.csv"),sg.Input(),sg.FileBrowse(key='-IN-')],[sg.Button("Load")], [sg.Button('Exit')]]
right_layout = [[sg.Image(key='-IMAGE-')]]

layout = [[sg.Column(left_layout),sg.VSeparator(),sg.Column(right_layout)]]


window = sg.Window('FPTree Viewer', layout)


while True:
    event, values = window.read()

    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    elif event == "Load":
        fpTree, headerTable, itemSet =    fpTreeFromFile(values['-IN-'], 0.5, 0.5)
        g, visual_style, layout = fpTree.fpPlot(values['-IN-'])
        ig.plot(g, "FPTree.png",layout=layout, **visual_style)
        
        window['-IMAGE-'].update(source="FPTree.png")

window.close()