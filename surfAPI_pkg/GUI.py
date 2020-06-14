from tkinter import Tk, Label, Button, Entry, StringVar, messagebox
import surfAPI
from functools import partial
import csv


def fenetreAddSpots(root):
    root.destroy()
    ajoutSpot = Tk()
    ajoutSpot.title('Ajout spot')
    label = Label(
        ajoutSpot, text='Nom du spot (Ex : Plage de Primel, Plougasnou) : ')
    label.grid()
    nomSpot = StringVar()
    nomSpot.set('')
    entryNomSpot = Entry(ajoutSpot, textvariable=nomSpot, width=30)
    entryNomSpot.grid()
    label = Label(
        ajoutSpot, text='Points de Géolocalisation (Ex : 48.3,49.6) : ')
    label.grid()
    pointsGeo = StringVar()
    pointsGeo.set('')
    entryPointsGeo = Entry(ajoutSpot, textvariable=pointsGeo, width=30)
    entryPointsGeo.grid()
    directionVent = StringVar()
    directionVent.set('')
    label = Label(
        ajoutSpot, text='Direction du Vent (Ex : Nord-Ouest) : ')
    label.grid()
    entryDirectionVent = Entry(ajoutSpot, textvariable=directionVent, width=30)
    entryDirectionVent.grid()
    button = Button(ajoutSpot, text='Ajouter le spot',
                    command=partial(addSpots, ajoutSpot, entryNomSpot, entryPointsGeo, entryDirectionVent
                                    ))
    button.grid()
    button = Button(ajoutSpot, text='Retour',
                    command=partial(retourSpot, ajoutSpot))
    button.grid(row=6, column=0, sticky='e')


def retourSpot(ajoutSpot):
    ajoutSpot.destroy()
    main()


def addSpots(ajout_spot, entry_spot, entry_location, entry_directionVent):
    fichierSpots = open(f'./spots/spots.csv', 'a+', newline='')
    writer = csv.writer(fichierSpots, delimiter=';', dialect='excel')
    writer.writerow([entry_spot.get(), entry_location.get(),
                     entry_directionVent.get()])
    fichierSpots.close()
    ajout_spot.destroy()
    surfAPI.initSpots()
    main()


def getResultat(location):
    infos = surfAPI.serverResponse(location[1])
    surfAPI.parseResponse(infos, location)
    previsionSurf = surfAPI.writeBestSpot()
    fenetreResultat = Tk()
    fenetreResultat.title(f'Résultat pour {location[0]}')
    label = Label(fenetreResultat, text=previsionSurf)
    label.grid()


def allSpots(root):
    messagebox.showinfo("Mode automatique démarré",
                        "Le mode Mail automatique/24h a démarré vous pouvez quitter cette fenêtre")
    root.destroy()
    surfAPI.allSpots()


def main():
    root = Tk()
    root.title('Surf API')
    surfAPI.initSpots()
    label = Label(
        root, text='Cliquez sur un des boutons :')
    label.grid()
    for spot in surfAPI.locations:
        button = Button(root, text=surfAPI.locations[spot][0], command=partial(
            getResultat, surfAPI.locations[spot]))
        button.grid(sticky='nesw')
    label = Label(
        root, text='')
    label.grid()
    button = Button(root, text='Ajouter un spot',
                    command=partial(fenetreAddSpots, root))
    button.grid()
    button = Button(root, text='Mode Mail/24h',
                    command=partial(allSpots, root))
    button.grid()
    root.mainloop()


if __name__ == '__main__':
    main()
