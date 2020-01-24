import numpy
from Numberjack import *
from Numberjack.solvers import Mistral

if __name__ == '__main__':

    R = 4 #numero massimo di articoli che un revisore puo revisionare
    L = 2 # numero massimo di revisori che possono revisionare quel articolo

    articoli = numpy.load('Code/dataset2/articoli.npy')#lista di tutti gli articoli
    autori = numpy.load('Code/dataset2/autori.npy')#lista di tutti gli autori
    settori = numpy.load('Code/dataset2/settori.npy')#lista di tutte le aree scientifiche

    revisori = numpy.load('Code/dataset2/revisori.npy')#lista di tutti i revisori(sott'insieme di autori)
    #matrice booleana di (articoli,autori) dove 1 se autore ha scritto articolo
    autoriarticoli = numpy.load('Code/dataset2/autoriarticoli.npy')
    #matrice booleana di(articoli,settore) dove 1 se articolo appartiene a quel settore
    settorearticoli = numpy.load('Code/dataset2/settorearticoli.npy')
    #matrice booleana di(revisori,settore) dove 1 se revisore appartiene a quel settore
    settorerevisori = numpy.load('Code/dataset2/settorerevisori.npy')
    #matrice booleana di(revisori,autori) dove 1 se revisore  in conflitto con autore(revisore e' in conflitto con se stesso)
    autoriconflitto = numpy.load('Code/dataset2/autoriconflitto.npy')


    """""
    R= 3
    L= 2
    autoriarticoli = numpy.load('Code/dataset1/autoriarticoli.npy')
    
    settorearticoli =numpy.load('Code/dataset1/settorearticoli.npy')
    
    settorerevisori = numpy.load('Code/dataset1/settorerevisori.npy')
    
    
    autoriconflitto = numpy.load('Code/dataset1/autoriconflitto.npy')
    
    
    articoli = numpy.load('Code/dataset1/articoli.npy')
    
    autori = numpy.load('Code/dataset1/autori.npy')
    
    settori = numpy.load('Code/dataset1/settori.npy')
    
    revisori = numpy.load('Code/dataset1/revisori.npy')
    """


    revisori_sched = Matrix(len(revisori), len(articoli))
    # matrice variabile(revisori,articoli) dove 1 se revisori puo revisionare quell'articolo

    matrice_stampa=numpy.ones([len(revisori), len(articoli)])#matrice che serve per print


    model = Model(
    [Sum(row) <= R for row in revisori_sched.row],#controllo se la somma degli articoli revisionati da un revisore<=R
    [Sum(col) == L for col in revisori_sched.col] #controllo se la somma  dei revisiori per ogni articolo = L
    )

    #se il settore del revisiore non appartiene al settore dell'articolo allora non lo puo revisionare
    for i in range(len(revisori)):
        for j in range(len(settori)):
            if (settorerevisori[i][j] == 0):
                for k in range(len(articoli)):
                    if (settorearticoli[k][j] == 1):
                      model.add(revisori_sched[i][k] == 0)
                      matrice_stampa[i][k]=0


    #se il revisore ha conflitti con autori di articoli del suoi settori allora non lo puo revisionare
    for i in range(len(revisori)):
        for j in range(len(settori)):
         if (settorerevisori[i][j] == 1):
            for k in range(len(articoli)):
                if (settorearticoli[k][j] == 1):
                    for p in range(len(autori)):
                        if (autoriconflitto[i][p]):
                            if (autoriarticoli[k][p]):
                                model.add(revisori_sched[i][k] == 0)
                                matrice_stampa[i][k]=0

    solver = Mistral.Solver(model)
    solution = solver.solve()
    #stampo la soluzione se soddisfacibile
    if solution:
        print "revisori_sched:\n"+str(revisori_sched)
    for i in range(len(revisori)):
        for j in range(len(articoli)):
            if(matrice_stampa[i][j]==1):
             print (revisori[i]+":"+(articoli[j])+"\n")
    else:
        print "INSODDISFACIBILE"


