from configparser import ConfigParser
config=ConfigParser()
configpath =r'C:\racine\users\CONFIG.ini'
config.read(r'C:\racine\users\CONFIG.ini')
rf=int(config['RF']['value'])
print(rf+2)
print(list(config['passwd']))