# from youtubesearchpython import ChannelsSearch, ResultMode
# from youtubesearchpython import Channel
from youtubesearchpython import *
import re
import time 
import random 
import asyncio
import aiohttp
import json 
import csv

# python async_yula2.py
resultSearch= []
sett1 = set()
sett2 = []
result_proto = []
result_proto2 = []
tagNamee = 'placeholder'
n = 20
start_time = time.time()

async def hashSearcher():
    channelsSearch = ChannelsSearch(tagNamee, limit = n) 
    r = channelsSearch.result()['result']
    for i, ni in enumerate(r):                
        len1 = len(sett1)
        sett1.add(r[i]['id'])
        len2 = len(sett1)
        if len2 - len1 == 1:
            sett2.append(r[i])

async def gather_searcher():   
    async with aiohttp.ClientSession() as session:       
        tasks = [] 
        for i in range(1, 1000):
            task = asyncio.create_task(hashSearcher())
            tasks.append(task)
            print(i)         
        
            tasks.append(task)
            # time.sleep(random.randrange(1,4))
        await asyncio.gather(*tasks)

def appenderTube():
    print(f"Количество уникальных каналов:__{len(sett2)}")
        
    for item in sett2:
        contacts = ''
        email = ''
        try:
            playlist = Playlist(playlist_from_channel_id(item['id']))
            url_video = playlist.videos[1]['link']   
        except:  
            url_video = ''
            
        try:
            descriptionChanel = Channel.get(f"{eval(item)['id']}")['description'] 
            splitDescriptionChanel = descriptionChanel.split(' ')
            # print(splitDescriptionChanel)
            for str1 in splitDescriptionChanel:
                try:         
                   match = re.search(r'https://', str1)
                   contacts += match.string + '\n'                            
                    
                except:
                    flag = False
               
        except:  
            descriptionChanel = ''    
           
        try:
            tags = Channel.get(f"{item['id']}")['tags'] 
        except:  
            tags = ''
            
        try:
            videoInfo = Video.getInfo(url_video, mode = ResultMode.json) 
        except:  
            videoInfo = ''
        
        # print(videoInfo['description'])
        try:
            splitVideoInfo = videoInfo['description'].split(' ')
            # print(splitVideoInfo)
            for str2 in splitVideoInfo:
                try:         
                   match = re.search(r'https://', str2)
                   contacts += match.string + '\n'                            
                    
                except:
                    flag = False
                
        except:
            print('some ex')
        arrContacts = contacts.split(' ')
        for nn in arrContacts:
            try: 
                match = re.search(r'[\w.-]+@[\w.-]+', nn)
                if match:
                   email +=match.group()            
                      
                        
            except:
                flag = False
       
       
        if contacts != '':
            result_proto2.append({
                    'link': item['link'],
                    'title': item['title'],                 
                    'url_about': f"https://www.youtube.com/{item['subscribers']}/about",
                    'id_chanel': item['id'],
                    'url_video': url_video,
                    'descriptionChanel': descriptionChanel,
                    'tags': tags,
                    'videoDescription_Contacts': videoInfo['description'],
                    'contacts': contacts,
                    'email': email
                                        
            }
            ) 
            
        if email != '':
            result_proto.append({
                    'link': item['link'],
                    'title': item['title'],                 
                    'url_about': f"https://www.youtube.com/{item['subscribers']}/about",
                    'id_chanel': item['id'],
                    'url_video': url_video,
                    'descriptionChanel': descriptionChanel,
                    'tags': tags,
                    'videoDescription_Contacts': videoInfo['description'],
                    'contacts': contacts,
                    'email': email                                        
            }
            ) 

# python async_yula2.py
def wrritter():
    with open(f"{tagNamee}_YouTubeEmailes_5.json", "a", encoding="utf-8") as file: 
      json.dump(result_proto, file, indent=4, ensure_ascii=False) 

    with open(f"Keyword_{tagNamee}_YouTubeEmailes_5.csv", 'w', newline='', encoding='cp1251',  errors="ignore") as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['LINK','TITLE', 'URL_ABOUT', 'ID_CHANEL', 'URL_VIDEO', 'DESCRIPTION_CHANEL', 'TAGS', 'VIDEO_DESCRIPTION_AND_CONTACTS', 'CONTACTS', 'EMAIL'])
            for item in result_proto:
               writer.writerow([item['link'], item ['title'], item['url_about'], item['id_chanel'], item['url_video'], item['descriptionChanel'], item['tags'], item['videoDescription_Contacts'], item['contacts'], item['email']])
    with open(f"{tagNamee}_YouTubeContacts_5.json", "a", encoding="utf-8") as file: 
      json.dump(result_proto2, file, indent=4, ensure_ascii=False) 

    with open(f"Keyword_{tagNamee}_YouTubeContacts_5.csv", 'w', newline='', encoding='cp1251',  errors="ignore") as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['LINK','TITLE', 'URL_ABOUT', 'ID_CHANEL', 'URL_VIDEO', 'DESCRIPTION_CHANEL', 'TAGS', 'VIDEO_DESCRIPTION_AND_CONTACTS', 'CONTACTS', 'EMAIL'])
            for item in result_proto2:
               writer.writerow([item['link'], item ['title'], item['url_about'], item['id_chanel'], item['url_video'], item['descriptionChanel'], item['tags'], item['videoDescription_Contacts'], item['contacts'], item['email']])
def main():    
    asyncio.run(gather_searcher())
    finish_time = time.time() - start_time
    appenderTube()
    wrritter() 
    print(f"количество каналов с контактами:__{len(result_proto2)}")   
    print(f"количество каналов с ємейлами:__{len(result_proto)}")
    print(f"Затраченное на работу скрипта время: {finish_time}")

if __name__ == "__main__":
    main()

# python async_yula2.py
