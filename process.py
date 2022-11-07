from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
import configparser
import csv
#get data
config_file = configparser.ConfigParser()
config_file.read("test.cfg")
api_id=config_file["GeneralConfig"]["api_id"]
api_hash=config_file["GeneralConfig"]["api_hash"]
phone=config_file["GeneralConfig"]["phone"]
gpLink=config_file["GeneralConfig"]["gpLink"]

print(gpLink)


def cleaner(testString) :
    testString = testString.replace('"', "")
    testString = testString.replace("'", '')
    testString = testString.replace("/", '')
    testString = testString.replace("\\", '')

    return testString

client = TelegramClient(phone, api_id, api_hash)
client.start()





try :
    if 'joinchat' in gpLink :
        exGpLink=gpLink.split('joinchat/')
        client(ImportChatInviteRequest(exGpLink[1]))

    else :

        receiver = client.get_entity(gpLink)
        client(JoinChannelRequest(receiver))

except Exception as e :
    print("ERROR IS :",str(e))
    if 'is already a participant of the chat' in str(e) :
        print('this is ok')
    else :
        print("Error")
        exit()


try :
    receiver = client.get_input_entity(gpLink)
except :
    notification.sendMessage('system , scrapping from public group section ,we can not enter this group ' + gpLink + ' ')
    exit()


all_participants = []
try :
    all_participants = client.get_participants(receiver)
    fountOkNumber='yes'
except Exception as e :
    print('can not scrap using this number va '+str(e))
    exit()



limit=10
counter=0
with open('data.csv', "w", encoding='UTF-8') as f:
   
    counter+=1
    if counter > limit : 
        print('we are done')


    writer = csv.writer(f, delimiter=",", lineterminator="\n")
    writer.writerow(['first name', 'last name', 'username', 'userid'])

    for user in all_participants:
        if user.username:
            username = user.username
        else:
            username = "--"
        if user.first_name:
            first_name = user.first_name
        else:
            first_name = "--"
        if user.last_name:
            last_name = user.last_name
        else:
            last_name = "--"

        first_name = cleaner(first_name) 
        last_name = cleaner(last_name) 
        username = cleaner(username) 
        writer.writerow([first_name, last_name,username,user.id])
        print("inserting username : " + username + ' first : ' + first_name + ' last : ' + last_name)

     



