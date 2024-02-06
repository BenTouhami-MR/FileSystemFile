from configparser import ConfigParser
import os 
def setin(path,section) :
    config =ConfigParser()
    config.read(r'C:\racine\users\CONFIG.ini')
    with open(path,'w') as file:
            section_options = config.items(section)
            for name ,value in section_options:
                file.write(f'{name}={value}\n')

def getsec(path,section):
    with open(path) as f:
        option=[(line.split('=')[0].strip(),line.split('=')[1].strip()) for line in f]
    config =ConfigParser()
    config.read(r'C:\racine\users\CONFIG.ini')
    if config.has_section(section):
        config.remove_section(section)
    config.add_section(section)
    for key,value in option:
        config.set(section,key,value)
    with open(r'C:\racine\users\CONFIG.ini', 'w') as f:
        config.write(f)

def userexist(mylist):
    config =ConfigParser()
    config.read(r'C:\racine\users\CONFIG.ini')
    a=0 

    for w in  list(config['passwd']):
        if w in mylist and w!='root':
            a=1
            break
    return a
