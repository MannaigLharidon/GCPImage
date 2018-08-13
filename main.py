# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 10:04:54 2018

@author: Mannaig L'Haridon
"""

import glob
from lxml import etree



def ImGCP(path,nbImages):
    """
    Crée un fichier xml contenant les coordonnées des points d'appuis fournis
    dans les fichiers
    
    IN :
        - path : chemin du dossier contenant les fichiers de coordonnées (au format txt)
        - nbImages : nombre d'images utilisés dans le traitement       
        - Ysize : taille de l'image selon l'axe vertical (pixels)
    """
    
    # Sélection des fichiers de coordonnées contenus dans le dossier
    fichiers = glob.glob(path+'/*.txt')
    
    # Verification du nombre de fichiers trouves
    if len(fichiers) == nbImages:

        # Balise initiale du xml
        balise = etree.Element("SetOfMesureAppuisFlottants")
        
        for fichier in fichiers: 
            # Lecture d'un fichier txt
            with open(fichier,"r") as f:
                pf = [line.split() for line in f]
#            print(pf)
            # Remplissage des balises correspondant au fichier
            image = etree.SubElement(balise,"MesureAppuiFlottant1Im")
            nomImage = etree.SubElement(image,"NameIm")
            nomImgTemp = pf[0][0]
            nomImage.text = nomImgTemp
            for pt in range(2,len(pf)):
                point = etree.SubElement(image,"OneMesureAF1I")
                nomPoint = etree.SubElement(point,"NamePt")
                nomPoint.text = pf[pt][0]
                coordPoint = etree.SubElement(point,"PtIm")
                Xcoord = pf[pt][1]
                # Passage des coordonnées Y SIG au Y MicMac : Ysize - Ymes
                Ycoord = str(float(pf[1][1]) - float(pf[pt][2]))
                coord = Xcoord + ' ' + Ycoord
                coordPoint.text = coord
        
        # Création du fichier de sortie
        filename = "xmlFileTest.xml"
        with open(filename,"w") as nF:
            document = etree.ElementTree(balise)
            document.write(nF,encoding='utf-8',xml_declaration=True)
        
        
        print("Le fichier '%s' a bien été créé !\n" % filename)
 
        # Affichage du fichier
#        x = etree.parse(filename)
#        print etree.tostring(x,pretty_print=True)
    
    else:
        print("ERROR : nombre de fichiers trouvés ne correspond pas au nombre d'images en entrée")
    



if __name__=='__main__':

    path = 'C:\Users\Mannaig\Documents\Etudes\ENSG\IT3\stage\TFE_UMR_EPOC\Script'
    nbImages = 3
    
    ImGCP(path,nbImages)  
    
"""
    ATTENTION : risque d'erreur --> MicMac a un YSize et un XSize global à son jeu d'image
                et ne prend pas en compte les XSize et YSize respectifs de chaque image
                (et donc des coordonnées déterminées dans le SIG)
"""
