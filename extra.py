import re
import requests
import json,csv
import time
from bs4 import BeautifulSoup as bs
from telethon import functions
from telethon.tl.types import *
from telethon.sync import TelegramClient
# from  telethon.sessions import StringSession as Sstring
data = json.load(open('pass.json'))
# db = [('name','id')]


Client =  TelegramClient('bhuvan',data["id"],data["token"])
Client.connect()
Client.parse_mode = 'html'
def main_ref():
    name_id = 0

    li = {}
    num_name_dic = {}
    eng_s, jap_s = set(), set()
    print(*list(map(lambda x:x.message.media_unread,Client.get_dialogs())),sep='\n')
    for x in Client.iter_messages(int(input('gf: ')) ,limit=None,reverse=True):#id,date,sender_id,text
        # try:        # if x.document is not None and x.document.mime_type.find('video/')!=-1:
            #     name,md=x.media.document.attributes[0].file_name,x.media
            #     db.append((name,str(md)))
            #     # print((name))
        if x.media_unread:
            print(x.media_unread)
            break
        if True:pass
        elif x.media is not None:
            temp = [BeautifulSoup(line,features="html.parser").text for line in x.text.split('\n')]
            jap,eng = map(lambda x: x.strip(),temp[0].split('|'))
            epi = temp[2].split(':')[-1].strip()
            audio = temp[3].split(':')[-1].strip()
            subt = temp[-1].split(':')[-1].strip()

            links={z.text:z.url for y in x.reply_markup.rows for z in y.buttons}

            for qlty in links:
                if jap not in jap_s:
                    jap_s.add(jap),eng_s.add(eng)
                    num_name_dic[jap] = name_id
                    num_name_dic[eng] = name_id
                    li[num_name_dic[jap]] = {}
                    name_id += 1
                if li[num_name_dic[jap]].get(audio,-1)==-1:
                    li[num_name_dic[jap]][audio] = {}
                if li[num_name_dic[jap]][audio].get(epi,-1)==-1:
                    li[num_name_dic[jap]][audio][epi] = {}
                qlty1 = tuple(filter(lambda x:x in qlty,('480','720','1080')))
                qlty1 = 'other' if qlty1 == () else qlty1[0]
                li[num_name_dic[jap]][audio][epi][qlty1] = links[qlty]
        # except:
        else:
            print(x.text)

    # json.dump(li,open('onganimedb.json','w'),indent=4)
    # json.dump({'eng':tuple(eng_s),'jap':tuple(jap_s)},open('onganimedb_index.json','w'),indent=4)

    print('DONE1',li)

def Users():
    from operator import itemgetter
    li = []
    for x in Client.iter_dialogs():
        try:
            t = [str(x.entity.username),x.name[:35],int(x.entity.restricted)]
            t.append(int(x.entity.deleted))
        except:
            t.append('channel')
        li.append(t)
    f,s = len(sorted(map(itemgetter(0),li),key=len)[-1]),len(sorted(map(itemgetter(1),li),key=len)[-1])
    print('username'.center(f),'name'.center(s),'ban','type/deleted',sep=' || ')
    for x in li:
        print(x[0].ljust(f),x[1].ljust(s),x[2],x[3],sep=' || ')

def downloader():
    # from tqdm import tqdm
    # def callback(ongoing,tot):
    #     bar.update(ongoing//1e6-bar.n)
    msg = Client.get_messages(entity=Client.get_entity('me'), limit=2)[-1]
    print(msg.document.size)
    # with tqdm(total=msg.document.size//1e6,unit='MB',unit_divisor=1024,ncols=100,unit_scale=True) as bar:
    Client.download_file(msg,'j.mp4')

def iter_download():
    import threading, asyncio
    msg = Client.get_messages(entity=Client.get_entity('Auto_encoder_indianime_bot'))[0]
    size = msg.document.size
    print(size)
    parts = 8
    async def parts_download(msg,start,end=None):
        with open('file.mp4','wb') as f:
            f.seek(start)
            async for x in Client.iter_download(msg,offset=start,limit=end):
                f.write(x)

    def run_coroutine_in_thread(coroutine,loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(coroutine)

    threads = []
    for x in range(parts):
        start = x*(size//parts)
        end = start + size//parts - 1 if x < parts - 1 else None
        loop = asyncio.new_event_loop()
        coroutine = parts_download(msg, start, end,)
        thread = threading.Thread(target=run_coroutine_in_thread, args=(coroutine, loop))
        threads.append(thread)
        thread.start()
    for x in threads:
        x.join()
    print('DONE')



def cleaner(username=None,all=False,first=False,msg_count=5,clean=True,dead_removal=True):
    bad_shit = {"p.rv.rt.", "h.nt.i", "pervert", "perv", 'boobs', 'boob', "sexy", "spicy", "sex","p.rn"}
    pattern = re.compile(r"|".join(bad_shit), re.IGNORECASE)
    def dead():
        for x in Client.iter_dialogs():
            if x.entity.restricted:
                if x.is_user or x.entity.deleted:
                    print(Client(functions.contacts.BlockRequest(x.entity.id)), x.name)
                    x.delete()
                elif x.is_channel:
                    print(Client(functions.channels.LeaveChannelRequest(x.entity.id)),x.name)
                    print(Client(functions.channels.DeleteChannelRequest(x.entity.id)), x.name)
                elif x.is_chat:
                    print(Client(functions.chatlists.LeaveChatlistRequest(x.entity.id),x.name))

    def clean_up(name,entity=False,user=None):
        me = Client.get_entity(user) if user is not None and type(user) is str else entity
        if not isinstance(me,Channel):
            ids = [z for z in Client.iter_messages(me,limit=msg_count,reverse=first) for x in str(z.text).split() if pattern.search(x)]
            if ids != []:
                print(name, end="--->")
                print([z.text for z in ids])
                Client.delete_messages(entity=me,message_ids=ids)
    if dead_removal:
        dead()

    if clean:
        if all:
            for x in Client.iter_dialogs():
                clean_up(x.name,x.entity)
        else:
            clean_up(username , user=username)

cleaner(all=True,msg_count=10,clean=False)
# print(type(Client.get_entity('anime_a_to_z')))
def exit_restricted():
    for x in Client.get_dialogs():
        if x.entity.restricted:
            if (x.is_channel):
                print(x.name,x.delete())
            elif (x.is_user and x.entity.bot):
                print(Client(functions.contacts.BlockRequest(x.entity.id)), x.name)
                x.delete()
            else:
                x.delete()
        else:
            if not x.is_channel and x.entity.deleted:
                x.delete()
            else:
                if x.is_user:
                    for y in Client.iter_messages(x.entity):
                        if y.silent:
                            print(x.unread_count,y)
                            break
                # print(x.unread_count)


iter_download()



# asyncio.run(main())

# data = {"name":"bhuvan","token  ":"deaeb3550dad68547e9bc41993556652","id":"27851356","bot":{"token":"6359127570:AAG2B_8LIgVpudoihOil0AEAD37YxQAfF4Y"}}
# with open("pass.json") as f:
#     k = json.load(f)011
#     print(k)
# downloader()
Client.disconnect()

# async for x in Client.iter_messages('anime_database123',limit=None):
#     if x.document is not None and x.document.mime_type.find('video/')!=-1:
#         name,md=x.media.document.attributes[0].file_name,x.media
#         db.update((name,str(md)))
#         j=0
#     else:
#         # break
#         j+=1
#         if j>10:break
#         # print(name)
#         # Client.send_message(Client.get_me().id,'text',file=x.media)
#         # bre
# print(len(db))
# with open('db.csv','w',encoding='utf-8',newline='') as f:
#     f = csv.writer(f)
#     f.writerows(db)
# json.dump(db,open('db.json','w'),indent=4)
# jap, eng = x.text.split('\n')[0].split('|')
# jap, eng = jap.strip().strip('*'), eng.strip().strip('`')
# print(jap, eng)

# for y in x.reply_markup.rows[-1].buttons[-1].url:
#     for z in y.buttons:
#         li.append(z.url.split('=')[-1])
#         print(z.url)
# response = requests.post('tg://resolve?domain=Auto_encoder_indianime_bot&amp;start=filesMTA1ODc')
# print(x.click(0,1))
# print(Client.get_messages('Auto_encoder_indianime_bot',limit=2)[1])
# time.sleep(10)
# Client.send_message('Auto_encoder_indianime_bot','<a href="tg://resolve?domain=Auto_encoder_indianime_bot&start=filesMTA1ODc">',parse_mode='html')#[1][0].click())
# for x in li:
# Client(functions.messages.StartBotRequest(bot='Auto_encoder_indianime_bot',peer=Client.get_me(), start_param=li[-1]))
# li.clear()
# break
# j+=1
# if j>10:break