import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkUpload
import random
import subprocess as sp
from termcolor import colored
import pyfiglet
import parser  as pr
import preparation as pre
import requests

SeparationString = "=========================================================="

# Функция вывода сообщения
def WriteMsgFunc(user_id, message,vk):
    random_id = random.randint(0, 12345678900987654321)
    vk.method('messages.send', {'user_id': user_id,'message': message,'random_id':random_id})

# Функция с приветственным сообщением 
def StartFunc(event,user_id,vk):
    hello = open("/home/frizik/Projects/ScanTelegramBot/TextMessages/Hello_Massage.txt")
    StringFromCommands = hello.read()
    WriteMsgFunc(event.user_id,StringFromCommands,vk)
    hello.close()

# Функция для вывода списка доступных команд
def HelpFunc(event,user_id,vk):
    commands=open("/home/frizik/Projects/ScanTelegramBot/TextMessages/Commands.txt","r")
    StringFromCommands=commands.read()
    WriteMsgFunc(event.user_id,StringFromCommands,vk)
    commands.close()

# Подготовительная функция
def Prepare(Answer,CountOfDash,CountOfZeros,TownName):    
    pre.StringParser(Answer,CountOfDash,CountOfZeros,TownName)

#Функция выдающая диапозон ip адрессов на город
def NewTownFunc(event,user_id,vk,TownName,login,password):
    Answer = pr.AutoParserIPs(TownName)
    logPath = "/home/frizik/Projects/ScanTelegramBot/Data/ips.txt"
    ips = open(logPath,"w")
    ips.write(Answer)
    ips.close()

    vk_session = vk_api.VkApi(login, password)
    vk_session.auth(token_only=True)

    upload = vk_api.VkUpload(vk_session)
    document = upload.document("/home/frizik/Projects/ScanTelegramBot/Data/ips.txt","db",group_id = 184430889)
    DocumentUrl = "vk.com/doc{}_{}".format(document["doc"]["owner_id"],document["doc"]["id"])
    WriteMsgFunc(event.user_id,"Получен диапозон ip адрессов города,в этом текстовом файле вы можете их просмотреть",vk)
    WriteMsgFunc(event.user_id,DocumentUrl,vk)
    print(colored("Город ","blue"),colored(TownName,"red"),colored(" обработан!!!","blue"))
    
# Основная функция 
def main():
    AsciiArt = pyfiglet.figlet_format("ScanVkBot")
    tmp = sp.call('clear',shell=True)
    print(colored(AsciiArt,"yellow"))
    print(colored(SeparationString,"magenta"))
    
    print(colored("Введите ключ бота:","yellow"),end = "")
    token = input()
    print(colored("Введите логин от страницы администратора:","yellow"),end = "")
    login = input()
    print(colored("Введите пароль от страницы администратора:","yellow"),end = "")
    password = input()
    
    try:
        vk = vk_api.VkApi(token=token)
        print(colored("Успешное подключение,бот запущен!!!","green"))
        print(colored(SeparationString,"magenta"))
    except:
        print(colored("Не удалось подключится,проверьте правильность введённых данных","red"))

    random.seed(version=2)
    longpoll = VkLongPoll(vk)
    Triger = False
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text
                if request == "старт" or request == "Старт":
                    StartFunc(event,event.user_id,vk)
                if request == "помощь" or request == "Помощь":
                    HelpFunc(event,event.user_id,vk)
                if request == "город" or request == "Город":
                    WriteMsgFunc(event.user_id,"Введите название города для скана",vk)
                    Triger = True
                else:
                    if Triger == True:
                        Triger = False
                        WriteMsgFunc(event.user_id,"Подготавливается диапозон адрессов,пожалуйста подождите",vk)
                        NewTownFunc(event,event.user_id,vk,request,login,password)

# При импорте 
if __name__ == "__main__":
    main()