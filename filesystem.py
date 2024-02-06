import datetime
import os 
import msvcrt
import gzip
import time
from pathlib import Path
import shutil
from configparser import ConfigParser

config=ConfigParser()
configpath =r'C:\racine\users\CONFIG.ini'

if os.path.exists(configpath): 
    config.read(r'C:\racine\users\CONFIG.ini')
    rf=int(config['RF']['value'])

def permissions(p):
    perfilemetadata=(p+"_metadata.txt")
    with open(perfilemetadata, 'r') as f:
        # Read the contents of the file into a string
        text = f.readlines()
    f.close
    # Split the string into a list of words
    words = text[-1].split(" ")
    permissions=words[-1].split(",")
    return permissions

def compress_file(file_path, gzip_path):
    with open(file_path, 'rb') as f_in, gzip.open(gzip_path, 'wb') as f_out:
        f_out.writelines(f_in)
    
def metadatafile(p):
    pmetadata=p+"_"+"metadata.txt"
    
    with open(pmetadata, 'w') as f:
        file_name = os.path.basename(p)
        file_size = os.path.getsize(p)
        file_extension = os.path.splitext(file_name)[1]

        creation_time = os.path.getctime(p)
        creation_time_tuple = time.gmtime(creation_time)
        creation_time_formatted = time.strftime("%Y-%m-%d %H:%M:%S", creation_time_tuple)

        modification_time= os.path.getmtime(p)
        modification_timt_tuple= time.gmtime(modification_time)
        modification_time_formatted = time.strftime('%Y-%m-%d %H:%M:%S', modification_timt_tuple)

        # Write the metadata to the file
        f.write(f'\nFile name: {file_name}')
        f.write(f'\nFile size: {file_size} bytes')
        f.write(f'\nFile extension: {file_extension}')
        f.write(f'\nFile creation time: {creation_time_formatted}')
        f.write(f'\nFile modified time: {modification_time_formatted}')
        f.write(f'\npermissions: \t. read,write,execute')

def execute(k):


#scanner la commande
    
    try:
        if len(k) != 0:
#cmnd est une list qui contient les arguments des commands 
            cmnd=k.split(" ")
            # Get the current date and time
            now = datetime.datetime.now()
            # Format the date and time as "YYYY-MM-DD HH:MM:SS"
            timestamp = now.strftimef("%Y-%m-%d %H:%M:%S")
            # Open the logging file in append mode
            with open("ID1FS_journalisation.txt", "a") as file:
                # Write the formatted date and time, followed by the command, to the logging file
                file.write(f"{timestamp}: {k}\n")
        else :
            pass      
    except: 
        pass
# Wait for the user to press a key
    
#This code will wait for the user to press a key, and then it will print the key that was pressed to the console.

    if len(cmnd)==1:
        p=''
        n=''
        m=''
        pass
    elif len(cmnd)==2:
        p=cmnd[-1]
        n=''
        m=''
    elif len(cmnd)==3:
        p=cmnd[-1]
        m=cmnd[-2]
        n=''
    elif len(cmnd)==4:
        p=cmnd[-1]
        m=cmnd[-2]
        n=cmnd[-3]
#les éléments qu'on aura d'utiliser pour construir de backups
    backups= r'C:\racine\Backups'
    backupfile=backups+'\\'+p
    if k==("cherche"+" "+p):
        print(p)
        if os.path.exists(p)==True:
            print("le fichier existe")
        else:
            print("le fichier n'existe pas")
#la commande 'info' pour avoir des informations a propos d'un fichier ou un repertoire 
    if k==("info"+" "+p):
        print(os.stat(p))
#info -size file.txt : nous donne la taille d'un fichier
    if k==("info"+" "+"-size"+" "+p):
        print(os.stat(p).st_size)
#info -permission file.txt : affiche les types des acces à 'file.txt' 
    if k==("info"+" "+"-permission"+" "+p):
        print(os.stat(p).st_mode)

#SET permissions(p) FOR A FILE
    # server connection:
        

    if k==("setp"+" "+m+" "+p):
        perfilemetadata=(p+"_metadata.txt")
#permission : juste lire 
        if m=='jr':
            lines=open(perfilemetadata,'r').read()
            # Open the file in read mode
            with open(perfilemetadata, 'r') as f:
                # Read the contents of the file into a string
                text = f.readlines()
                
                f.close
            # Split the string into a list of words
            words = text[-1].split(" ")
            
            # Remove the last word from the list
            words.pop()
            # Join the words back into a single string
            text[-1] = " ".join(words)
            # Open the file in write mode
            with open(perfilemetadata, 'w') as f:
                text=" ".join(text)
                # Write the modified string back to the file
                f.write(text)
            with open (perfilemetadata,'a') as f:
                    f.write(" read,.,.")
            f.close()
            
#permission : juste ecrire
        if m=='jw':
            lines=open(perfilemetadata,'r').read()
            # Open the file in read mode
            with open(perfilemetadata, 'r') as f:
                # Read the contents of the file into a string
                text = f.readlines()
                
                f.close
            # Split the string into a list of words
            words = text[-1].split(" ")
            
            # Remove the last word from the list
            words.pop()
            

            # Join the words back into a single string
            text[-1] = " ".join(words)
            # Open the file in write mode
            with open(perfilemetadata, 'w') as f:
                text=" ".join(text)
                # Write the modified string back to the file
                f.write(text)
            with open (perfilemetadata,'a') as f:
                    f.write(" .,write,.")
            f.close()
#permission : juste executer
        if m=='jx':
            lines=open(perfilemetadata,'r').read()
            # Open the file in read mode
            with open(perfilemetadata, 'r') as f:
                # Read the contents of the file into a string
                text = f.readlines()
                
                f.close
            # Split the string into a list of words
            words = text[-1].split(" ")
            # Remove the last word from the list
            words.pop()

            # Join the words back into a single string
            text[-1] = " ".join(words)
            # Open the file in write mode
            with open(perfilemetadata, 'w') as f:
                text=" ".join(text)
                # Write the modified string back to the file
                f.write(text)
            with open (perfilemetadata,'a') as f:
                    f.write(" .,.,execute")
            f.close()
#permission : read and write
        if m=='rw':
            lines=open(perfilemetadata,'r').read()
            # Open the file in read mode
            with open(perfilemetadata, 'r') as f:
                # Read the contents of the file into a string
                text = f.readlines()
                
                f.close
        
            # Split the string into a list of words
            words = text[-1].split(" ")
        
            # Remove the last word from the list
            words.pop()
            print(words)

            # Join the words back into a single string
            text[-1] = " ".join(words)
        
            # Open the file in write mode
            with open(perfilemetadata, 'w') as f:
                text=" ".join(text)
                # Write the modified string back to the file
                f.write(text)
            with open (perfilemetadata,'a') as f:
                    f.write(" read,write,.")
            f.close()
            
#permission : read and execute
        if m=='rx':
            lines=open(perfilemetadata,'r').read()
            # Open the file in read mode
            with open(perfilemetadata, 'r') as f:
                # Read the contents of the file into a string
                text = f.readlines()
                
                f.close
            # Split the string into a list of words
            words = text[-1].split(" ")
            
            
            # Remove the last word from the list
            words.pop()
            
            
            # Join the words back into a single string
            text[-1] = " ".join(words)
            
            # Open the file in write mode
            with open(perfilemetadata, 'w') as f:
                text=" ".join(text)
                # Write the modified string back to the file
                f.write(text)
            with open (perfilemetadata,'a') as f:
                    f.write(" read,.,execute")
            f.close()
            
#permission : write and execute
        if m=='wx':
            lines=open(perfilemetadata,'r').read()
            # Open the file in read mode
            with open(perfilemetadata, 'r') as f:
                # Read the contents of the file into a string
                text = f.readlines()
                
                f.close
            # Split the string into a list of words
            words = text[-1].split(" ")
            
            # Remove the last word from the list
            words.pop()
            
        
            # Join the words back into a single string
            text[-1] = " ".join(words)
            # Open the file in write mode
            with open(perfilemetadata, 'w') as f:
                text=" ".join(text)
                # Write the modified string back to the file
                f.write(text)
            with open (perfilemetadata,'a') as f:
                    f.write(" .,write,execute")
            f.close()
        
#permission : read,write and execute
        if m=='rwx':
            lines=open(perfilemetadata,'r').read()
            # Open the file in read mode
            with open(perfilemetadata, 'r') as f:
                # Read the contents of the file into a string
                text = f.readlines()
                
                f.close
            # Split the string into a list of words
            words = text[-1].split(" ")
            
            # Remove the last word from the list
            words.pop()
            
            
            # Join the words back into a single string
            text[-1] = " ".join(words)
            # Open the file in write mode
            with open(perfilemetadata, 'w') as f:
                text=" ".join(text)
                # Write the modified string back to the file
                f.write(text)
            with open (perfilemetadata,'a') as f:
                    f.write(" read,write,execute")
            f.close()
#read a specific number of lines            
    if cmnd[0]=='r':
        if permissions(p)[-3]=="read":
# read specific a specific number of the first lignes:
            if n=='-f':
                try:
                    with open(p,'r') as file:
                        for i in range(int(m)+1):
                            print(file.readline())
                except:
                    print('nombre de ligne Inapproprié ou fichier inexistant ')
# read specific a specific number of the last lignes:
            elif n=='-l':
                try:
                    with open(p,'r') as file:
                        for i in range(-int(m)-2,-1, 1):
                            print(file.readline())
                except:
                    print('nombre de ligne Inapproprié ou fichier inexistant ')
        else:
            print("vous n'avez pas la permssion de lire le contenue de ce fichier")

    
#function 01 :READ : lire
    if k==("lire"+" "+p):
        
        if permissions(p)[-3]=='read':
            with open(p,"r") as f:
                text=f.readlines()
                print(text)
            f.close()
        else:
            print("vous n'avez de pirmissions sufisants pour lire ce fichier")
        
# compress a file:
    if k=="compress"+" "+p:
        filetocompress=p.split(".")[0]
        compressedfile=filetocompress+'.gz'
        compress_file(p,compressedfile)
# decompress a file:
    if k=="decompress"+" "+p:
        with gzip.open(p,'rb')as f_in:
            print(f_in)
            with open('file.txt','wb') as f_out:
                shutil.copyfileobj(f_in,f_out)
#function 02: append+write :ecrire-
#'ed' pour ecrire au debut de fichier(write)   
    if k==("ed"+" "+m+" "+p):
        if permissions(p)[-3]=='read':
            try:
                newtxt=[]
                with open(p,"r") as file:
                    text=file.readlines()
                    newtxt.append(m)
                    for i in range(len(text)):
                        newtxt.append(text[i])
                    lasttxt='\n'.join(newtxt)
                with open(p,"w") as file:    
                    file.write(lasttxt)
                file.close()
            except:
                print("le fichier n'existe pas")
        else:
            print("vous n'avez pas la permission de lire ce")

# 'oemi' : ouvrir en mode interactif
    if k==("oemi"+" "+p):
        os.startfile(p)


#'ef' pour ecrire a la fin de fichier(append) 
    if k==("ef"+" "+p):
        if permissions(p)[-2]=='write':
            try:
                with open(p,'a') as file:
                    while True:
                        ln=input("saisi un text")
                        if ln=="close.file":
                            break
                        else:
                            file.write("\n"+ln)
                            
                file.close()
            except:
                print("le fichier n'existe pas")
#Function 03 : DELETE : supr
    if k==("supr"+" "+p):
        os.remove(p)
#copier le contenu d'un fichier dans un auter fichier
    if(k=="copier"+" "+n+" "+"in"+" "+p):
        with open(p,"a") as file:
            with open(n,"r") as secondfile:
                for ln in n:
                    file.write(ln)

#afficher le repertoire actuelle "qrep=quel repertoire":
    if k==("qrep"):
        cwd=Path.cwd()
        print("le repertoire de travail acturlle est \t{}".format(cwd))
#changer le répertoire "chrep=hcanger repertoire":
    if k==("chrep"+" "+p):
        try:
            os.chdir(p)
        except FileNotFoundError:
            print("le repertoirre\t:{}\tn'exist pas".format(p))
        except NotADirectoryError:
            print(f'{p}\tn''est pas un repertoire')
        except PermissionError:
            print("vous n'avez pas la permissions(p) au fichier \t{}".format(p))
#cf pour creer un fichier
    if k==('cf'+" "+p):
        open(p,'w')
        for i in range(1,rf+1):
            file=str(i+1)+p
            shutil.copy2(p,backups+'/'+file)
            metadatafile(p)         
#cr pour creer un repertoire
    if k==("cr"+" "+p):
        os.mkdir(p)
        metadatafile(p)
#cp : copy to directory
    if k=="cp"+" "+m+" "+p: 
            shutil.copy2(m,p)
    
#cut : couper un fichier
    if k=="cut"+" "+m+" "+p:
            shutil.move(m,p)
#supprimer un repertoire sr=supprime repertoire
    if k==("sr"+" "+m+" "+p):
        if m=='-f':
            sure=input(f'voulez-vouz vraiment supprimer le repertoire   {p}  est ces fichiers(oui/non)')
            try:
                if sure=='oui':
                    shutil.rmtree(p)
                elif sure=='non' :
                    pass
            except:
                print('syntax non valide')
                pass
        else:
            try:
                if sure=='oui':
                    shutil.rmtree(p)
                elif sure=='non' :
                    pass
            except:
                print('syntax non valide')
                pass
#sfid : supprimer un fichier definitivement 
    if k==("sfd"+" "+p):
        sure=input(f'voulez-vouz vraiment supprimer le fichier   {p}  (oui/non)')
        try:
            if sure=='oui':
                os.remove(p)
                
                os.remove(backupfile)
            elif sure=='non' :
                pass
        except:
            print('syntax non valide')
            pass
#supprimer un fichier sfi=supprime fichier 
    if k==("sf"+" "+m+" "+p):
        if m=='-f':
            sure=input(f'voulez-vouz vraiment supprimer le fichier   {p}  (oui/non)')
            try:
                if sure=='oui':
                    os.remove(p)
                elif sure=='non' :
                    pass
            except:
                print('syntax non valide')
                pass
    if k==("sf"+" "+p):
            try:
                os.remove(p)
            except:
                print('syntax non valide')
                pass

    if k==("walk"+" "+p):
        # utiliser la fonction walk de os pour parcourir tous les fichiers et dossiers
        for root, dirs, files in os.walk(p):
            # imprimer les fichiers
            for file in files:
                print(os.path.join(root, file))
            # imprimer les sous-répertoires
            for dir in dirs:
                print(os.path.join(root, dir))

#revenir au repertoire parent "rp= repertoire parent":
    if k=="rp":
        os.chdir("..")
# ls :list current directory 
    if k==("ls"+" "+p):
    # chemin du répertoire

        # utiliser la fonction listdir de os pour lister les fichiers
        files = os.listdir(p)

        # afficher les fichiers
        for file in files:
            print(file)
# head:
    if k=="head"+" "+p:
        if permissions(p)[-3]=='read':
            with open(p,'r') as file:
                for i in range(10):
                    print(file.readline())
        else:
            print("vous n'avez de pirmissions sufisants pour lire ce fichier")
        
# tail:
    if k=="tail"+" "+p:
        if permissions(p)[-3]=='read':
            with open(p,'r') as file:
                for i in range(-10,-1,1):
                    print(file.readline())
        else:
            print("vous n'avez de pirmissions sufisants pour lire ce fichier")

# Copy the file 'source_file.txt' to the destination 'destination_folder'
    if k=="cp"+" "+m+" "+p:
        shutil.copy2(m,p)        
#la fonction help
    if k==("help"):
        print("tail <fichier> : permet de lire les dix derniers lignes. ")
        print("r  <fichier> -l d : permet de lire un nombre spécifique de dernier lignes."" l : last"" et "" d : nombre de ligne"". ")
        print("r  <fichier> -f d : permet de lire un nombre spécifique de dernier lignes."" f : last"" et "" d : nombre de ligne"". ")
        print("oemi <fichier> : permet d'ouvrir un fichier en mode interactif en spécifiant bien sur l'extension du fichier. ")
        print("ed <fichier> : permet d'écrire au début du fichier. ")
        print("ef <fichier> : permet d'écrire à la fin du fichier. ")
        print("sf  <fichier> : permet de supprimer un fichier sans confirmation. ")
        print("sf -f <fichier> : permet de supprimer un fichier avec confirmation. ")
        print("cher  <fichier> : permet de chercher si un fichier existe ou pas, elle retourne "" le fichier existe "" s'il existe et "" le fichier n'existe pas "" s'il n'existe pas. ")
        print("info <fichier> : permet de récupérer quelques informations sur le fichier. ")
        print("info -size <fichier> : permet de récupérer la taille de fichier. ")
        print("cpc <fichier1> <fichier2>: permet de copier le contenu d'un fichier dans un autre. ")
        print("ls : permet de lister les fichiers d'un répertoire. ")
        print("com <fichier> : permet de compresser un fichier.")
        print("cp <fichier> destination : copier un fichier dans un autre. ")
        print("cut <fichier> destination : couper un fichier d'un répertoire vers un autre. ")
        print("Permissions : ")
        print("setp jr <fichier> : autoriser le permission de lire seulement. ")
        print("setp jw  <fichier> : : autoriser le permission d'écrire seulement. ")
        print("setp  jx <fichier> : : autoriser le permission d'éxecuter seulement. ")

        print("pour les répertoires : ")
        print(" cr sr <répertoire> : permet de créer un répertoire. ")
        print("sr <répertoire> : permet de supprimer un répertoire sans confirmation. ")
        print("sr -f <répertoire> : permet de supprimer un répertoire avec confirmation. ")
        print("rrepp : permet de revenir au répertoire parent. ")
        print("qrep : permet de récupérer le répertoire actuelle ( current directory). ")
        print("chrep <réperoite> : permet de changer le répertoire du travail si'il existe et si vous avez la permission. ")
        print("walk : permet de lister les répertoires ( et meme des fichiers de ce répertoire si'il existe) et les fichiers d'un répertoire. ")
        print("logout : permet à l'utilisateur de se déconnecter.")