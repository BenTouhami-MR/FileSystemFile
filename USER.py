from configparser import ConfigParser
import os,shutil
from function import setin
from function import getsec,userexist
import filesystem
import datetime
import gzip
import time
backups= r'C:\racine\Backups'

mycommande =['newuser','newgroup','sv','rmuserfrom','remuser','remgrp','chguser','addtogrp','seeuser','rf']
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

configpath=r'C:\racine\users\CONFIG.ini'
mypath =r'C:\racine\users'
etcpath= r'C:\racine\etc'
os.chdir(mypath)
config = ConfigParser()

# if CONFIG file exist do not create a new one 
exist= os.path.exists(configpath)#2
if exist == False:
    #ajouter les section dans le fichier config
    config.add_section('passwd')
    config.add_section('group')
    config.add_section('shadow')
    config.add_section('RF')
    config.set('RF','value','2')
    #initialiser UID et GID par 102 et 202 (200,201-100,101 sont prisent seront porter par root et le premier utilisateur que tu va crée)
    UID = 102
    GID = 202
    #changer le path par D:\racine\users pour se connecter
    os.chdir(mypath)
    #cree le mot de passe de root et le deposer sur le fichier de config.ini
    passwd=input("create the password of root : ")
    config.set('passwd','root','root:x:200:100')
    config.set('group','root','root:x:200')
    config.set('shadow','root',f'{passwd}')
    #cree le dossier(son compte) de root
    os.mkdir(mypath+'\\root')
    #cree le mot de passe de votre utilisateur, son dossier et le deposer sur le fichier de config.ini
    user =input("write your nameuser : ")
    passwd = input("create the password of your own user: ")
    config.set('passwd',f'{user}',f'{user}:x:201:101')
    config.set('group',f'{user}',f'{user}:x:201')
    config.set('shadow',f'{user}',f'{passwd}')
    os.mkdir(mypath+f'\\{user}')
    with open(configpath,'w') as file:
        config.write(file)
     #entrer au dossier de votre utilisateur
    os.chdir(mypath+f'\\{user}')#2
    us ='$-'
    
# si le fichier est déja exist
else:
    #ouvrir le ficheir
    config.read(configpath)
    get=list(config['group'].values())[-1]
    # récuperer le le GID et UID du dernier user 
    try:
        GID =int(get.split(":")[2])+1
    except:
        print()
    get=list(config['passwd'].values())[-1]
    UID =int(get.split(":")[3])+1
    # afficher les user disponible et choisir un pour se connecter
    os.chdir(mypath)
    print("-----users avaible :",end=" ")
    for i in list(config['passwd']):
        print(i,end=" ")
    print("-------")
# logging as a user 
    while True:
        machine_time = time.time()
        real_time = time.gmtime()

        real_time_seconds = time.mktime(real_time)
    
        if machine_time-1 <real_time_seconds and  real_time_seconds < machine_time:
            print(' You can sign in or sing up')
        else:
            print('No connection!! ')
            break
        user = input("type the name of user :")
                # Get the current time according to the machine
        # Get the current time according to the machine
      
        
       
        
        if user not in list(config['passwd']):
            print("user does not exist!!")
        else:
            break
    while True:
         users = input("enter the password  :")
         if users != config['shadow'][f'{user}']:
            print("password incorrect,please try again!! :")
         else:
            os.chdir(os.getcwd()+f"\\{user}")
            break
        
#si vous etes un utilisateur normale afficher $- sinon(root) #- sur le cmd
    if user =='root':us ='#-'
    else: us ='$-'

#récuperer les informations sur le fichier (passwd,group,shadow).txt et stocker leur contenu dans la section convenable sur config.ini
if os.path.exists(etcpath+'\\passwd.txt') and os.path.exists(etcpath+'\\group.txt') :
    getsec(etcpath+'\\passwd.txt','passwd')
    getsec(etcpath+'\\group.txt','group')
    getsec(etcpath+'\\shadow.txt','shadow')
    getsec(etcpath+'\\RF.txt','RF')



while True:
    
    # copier le contenu de chaque section dans un fichier nommer par le nom de la section qui se trouve dans etc (configuration file) 
    setin(etcpath+'\\passwd.txt','passwd')
    setin(etcpath+'\\group.txt','group')
    setin(etcpath+'\\shadow.txt','shadow')
    setin(etcpath+'\\RF.txt','RF')
    n= input(os.getcwd()+us)

    if n.split(" ")[0] not in mycommande:
        filesystem.execute(n)
        continue
    else:
        try:
            user =n.split()[1]
        except:
            print("ERROR: commande does not exist or it shoud have an argument")
            continue
        # la commande newuser permet de crée un nouveau utilisateur (un utilisateur doit avoir toujours un mot de passe pour la securiter)
        if n.split()[0] == 'newuser':
            # vous devez être le propritaire pour ajouter un noveau utilisateur
            if us!='#-':
                print("permission denied : you should be the root ")
                continue
            #verifier si l'utilisateur deja existe
            elif user in list(config['passwd']):
                print("this user is already exist")
                # ajouter le nouveau utilisateur dans le fichier config.ini anisi que son groupe et son mot de passe
            else:
                pswd= input("entre a password of user: ")
                config.set('passwd',f'{user}',f'{user}:x:{GID}:{UID}')
                #verifier si un group deje existe sur le nom de nouveau utilisateur pour qu'il ne le cree pas une autre fois
                if user  not in config['group']:
                    config.set('group',f'{user}',f'{user}:x:{GID}')
                config.set('shadow',f'{user}',pswd)
                with open(configpath,'w')as file:
                    config.write(file)
                path =mypath+f'\\{user}'
                try:
                    os.mkdir(path)
                except:
                    pass
    # ajouter dans le UID et GID pour le nouveau utilisater qui va se crée 
                UID+=1
                GID+=1


        #la commande newgroup permet de crée un nouveau groupe
        elif n.split()[0] =='newgroup':
            # vous devez être le propritaire pour ajouter un noveau groupe
            if us !='#-':
                print("permission denied : you should be the root ")
                continue
            #verifier si le groupe est  deja existe
            elif user in list(config['group']):
                print("this group is already exist")
            # ajouter le nouveau groupe dans le fichier config.ini     
            else:
                config.set('group',f'{user}',f'{user}:x:{GID}')
                with open(configpath,'w') as file:
                    config.write(file)
                    
                GID+=1


        #verifier si l'utilisateur existe et affichier ses informatoin si c'était le cas 
        elif n.split()[0] =='seeuser':
            config.read(configpath)
            try:
                print(config['passwd'][f'{user}'])
            except:
                print(user+" does not exist ")
        elif n.split()[0] =='GUI':
            config.read(configpath)
            try:
                print(config['grp'][f'{user}'])
            except:
                print(user+" does not exist ")


        #ajouter un utilisateur pour un groupe specifique
        elif n.split()[0] =='addtogrp':
            
            
            #verifier le nombre de parametre convenable
            try:
                user1 =n.split()[2]
            except:
                print("commande need more arguments")
                continue
                    
            #vous devez être le propritaire
            if us !='#-':
                print("permission denied : you should be the root ")
                continue
            #ajouter l'utilisateur apres verification
            else:
                config.read(configpath)
                #verifie si le groupe existe existe
                if user not in list(config['group']):
                        print(user +" is not a group")
                        continue
                else:
                        
                        test =config['group'][f'{user}']
                        
                        #verifier si l'utilisateur existe déja dans ce groupe         
                        if user1 in test:
                            print(user1+" is already exist in this group")
                        #verifier si le l'utilisateur existe

                        elif user1 not in list(config['passwd']):
                            print("user "+user1 +" does not existe")
                        #ajouter l'utilisateur au groupe
                        else:
                            config['group'][f'{user}'] +=":"+user1
                
                with open(configpath,'w') as file:
                    config.write(file)
                    


        #delete a user
        elif n.split()[0] =='remuser':
            #verifier si c'est vous êtes le propriataire (root)
            if us !='#-':
                print("permission denied : you should be the root ")
                continue
            else:
                
                try:
                    try:
                        shutil.rmtree(mypath+f'\\{user}')
                    except:
                        pass
                    #supprimer l'utilisateur de section passwd ainsi que son mot de passe de section shadow
                    del config['passwd'][f'{user}']
                    del config['shadow'][f'{user}']
                    #supprimer l'utilisateur d'un groupe si il appartient à celui-ci
                    for w in list(config['group'].values()):
                        m=w.split(':')[0]
                        if user in w and m !=user:    
                            w=w.replace(f':{user}',"")
                            config['group'][f'{m}'] =w
                            with open(configpath,'w') as file:
                                config.write(file)
                    #suprimer son groupe s'il existe 
                    try:
                        del config['group'][f'{user}']
                    except:
                        pass
                except:
                    #si l'utilsateur n'exsite pas il nous le dire
                    print("user "+user+" does not exist")
                with open(configpath,'w') as file:
                    config.write(file)


    # supprimer un l'utilisateur qui existe dans un groupe
        elif n.split()[0] =='rmuserfrom':
            #verifier le nombre d'argument
            try :
                user1 =n.split()[2]  
            except:
                print("commande needs more argumts")
                continue
            # verifier si vous êtes le propritaire
            if us !='#-':
                    print("permission denied : you should be the root ")
                    continue

            else:
                config.read(configpath)
                #verifier si le user existe 
                    
                if user not in list(config['passwd']):
                    print("user "+user+" does not exist")
                    continue
                # tout d'abord il verifier si le groupe existe 
                if user1 not in config['group']:
                        print('group '+user1+ ' does not exist')
                        continue
                test1 =config['group'][f'{user1}']
                    
                        
                #verification si ce user existe dans ce groupe puis il le supprime si c'était le cas
                if user in test1 and user!=user1:
                            test1 =test1.replace(f':{user}'," ")
                            config['group'][f'{user1}'] =test1
                elif user not in test1 :
                            print(user+" is not in this group ")
                
            with open(configpath,'w') as file:
                                config.write(file)        
                    
                        

        # supprimer un groupe 
        elif n.split()[0] =='remgrp':
            #verifier si vous êtes root
            if us !='#-':
                print("permission denied : you should be the root ")
                continue
            #verifeir sile groupe existe et le supprimer s'il existe
            else:
                try:
                    del config['group'][f'{user}']
                except:
                        print("group "+user+" does not exist")
                with open(configpath,'w') as file:
                        config.write(file)

        # go throught folders
        elif n.split()[0]=='sv':
        #revenir en arrière
            if user=='..' :   #verifier l'utilisateur connecter
                if [os.getcwd()== r'C:\racine\users'+f"\\{i}" for i in config['passwd']] and us!='#-':
                    if len(os.getcwd().split('\\'))>4:
                        pass
                    else:
                        print("permission denied : these are system's folders")
                        continue
                
                curr_fldr=os.getcwd().split("\\")[-1]
                path =os.getcwd().replace('\\'+curr_fldr,"")
                os.chdir(path)
                # acceder directement à la racine bien sur si vous êtes 'root'
            elif user=="/":            
                if us !='#-':
                    print("permission denied : you should be the root ")
                else:
                    os.chdir(r'C:\racine')
            # verifier si le dossier que vous voulez l'acceder est un compte d'un utilisateur
            elif user in list(config['passwd']) :
                print("ERROR this is a folder of another user you can not access to ")
             
            else:
                try:
                        os.chdir(os.getcwd()+f"\\{user}") 
                except: 
                        print("folder doesn't exist in the current folder ")    

        # se connecter avec un autre utilisateur
        elif n.split()[0]=='chguser':
            # verifier si vous etes deje entrain de se connecter avec cette utilisateur
            if user in os.getcwd():#1
                print("you are already this user")#1

            else:
                try:
                    #verifier l'existance d'utilisateur
                    if us=='#-':
                         os.chdir(mypath+f'\\'+user)
                         us='$-'
                         continue
                    if user in list(config['passwd']):
                        pswd =input("enter the password :")
                    # assuurer que le mot de passe est correcte
                    if pswd ==config['shadow'][f'{user}']:
                        os.chdir(mypath+f'\\'+user)
                    else:
                        print("password inccorect")
                except:
                    print("user "+user+" does not exist")
        elif n.split()[0]=='rf':
            if us !='#-':
                print("permission denied : you should be the root ")
                continue
            verify= list(range(0,10))
            verify=list(map(str,verify))
            a=0
            for w in user :
                if w not in verify:
                    print(" please the value should be an integer")
                    a=-1
                    break
            if a==0:
                config['RF']['value']=user
            with open(configpath,'w') as file:
                config.write(file)

            
        else:
            #si la commande n'existe pas 
            pass
        if 'root' in os.getcwd() or userexist(os.getcwd().split('\\'))==0 :
            #si l'utilisateur est simple
            us ='#-'
        else: # si il est un root
            us= "$-"
        