from tkinter import Tk, Label, Button, Entry, StringVar
import surfAPI
from functools import partial
import csv


def fenetreAddSpots():
    ajoutSpot = Tk()
    ajoutSpot.title('Ajout spot')
    label = Label(
        ajoutSpot, text='Nom du spot (Ex : Plage de Primel, Plougasnou) : ')
    label.grid()
    nomSpot = StringVar()
    nomSpot.set("Peu")
    entryNomSpot = Entry(ajoutSpot, textvariable=nomSpot, width=30)
    entryNomSpot.grid()
    label = Label(
        ajoutSpot, text='Points de Géolocalisation (Ex : 48.3, 49.6) : ')
    label.grid()
    pointsGeo = StringVar()
    pointsGeo.set('test')
    entryPointsGeo = Entry(ajoutSpot, textvariable=pointsGeo, width=30)
    entryPointsGeo.grid()
    directionVent = StringVar()
    directionVent.set("test")
    label = Label(
        ajoutSpot, text='Direction du Vent (Ex : Nord-Ouest) : ')
    label.grid()
    entryDirectionVent = Entry(ajoutSpot, textvariable=directionVent, width=30)
    entryDirectionVent.grid()
    button = Button(ajoutSpot, text='Ajouter le spot',
                    command=partial(addSpots, entryNomSpot.get(), entryPointsGeo.get(), entryDirectionVent.get()))
    button.grid()
    ajoutSpot.mainloop()


def addSpots(nom_spot, location, directionVent):
    fichierSpots = open(f'./spots/spots.csv', 'a+', newline='')
    writer = csv.writer(fichierSpots, delimiter=';', dialect='excel')
    writer.writerow([nom_spot, location, directionVent])
    fichierSpots.close()
    print('Bien ajouté')
    surfAPI.initSpots()


def main():
    root = Tk()
    root.title('Surf API')
    surfAPI.initSpots()
    for spot in surfAPI.locations:
        print(surfAPI.locations[spot][0])
        label = Label(root, text=surfAPI.locations[spot][0])
        label.grid()
    button = Button(root, text='Ajouter un spot',
                    command=partial(fenetreAddSpots))
    button.grid()
    root.mainloop()


if __name__ == '__main__':
    main()
