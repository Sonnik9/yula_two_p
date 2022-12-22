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

from utils import (
    youtube_authenticate,  
    get_video_details,
    print_video_infos,
    search
)

start_time = time.time()
sett1 = set()
promResult = []
sett2 = []
result_proto = []
tagNamee = 'table'

async def go():     
    youtube = youtube_authenticate()
   
    try:
        response = search(youtube, q="table", maxResults=50)
        items = response.get("items")
    except:
        print("ex1")
        
    
    for item in items:       
        
        try:
            video_id = item["id"]["videoId"]
            video_response = get_video_details(youtube, id=video_id)
            promResult.append(video_response)
            
        except:
            print('ex2')
            continue
 
        
    for i, ni in enumerate(promResult):                
        len1 = len(sett1)
        sett1.add(promResult[i]['items'][0]['snippet']['channelId'])
        len2 = len(sett1)
        if len2 - len1 == 1:
            sett2.append(promResult[i])       
    # print(len(sett2))
# go() 

async def gather_searcher():   
    async with aiohttp.ClientSession() as session:       
        tasks = [] 
        for i in range(0, 50):
            task = asyncio.create_task(go())
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
            playlist = Playlist(playlist_from_channel_id(item['items'][0]['snippet']['channelId']))
            url_video = playlist.videos[1]['link']   
        except:  
            url_video = ''
            
        try:
            descriptionChanel = Channel.get(f"{item['items'][0]['snippet']['channelId']}")['description'] 
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
       
        if email != '':
                result_proto.append({
                    'link': f"https://www.youtube.com/chanel/{item['items'][0]['snippet']['channelId']}",
                    'title': item['items'][0]['snippet']['title'],          
                    'id_chanel': item['items'][0]['snippet']['channelId'],
                    'descriptionChanel': descriptionChanel,
                    'videoDescription_Contacts': videoInfo['description'],
                    'contacts': contacts,
                    'email': email
                                        
            }
            ) 

# python api_by_key_words.py
def wrritter():
    with open(f"{tagNamee}_YouTubeSeriouse_5.json", "a", encoding="utf-8") as file: 
      json.dump(result_proto, file, indent=4, ensure_ascii=False) 

    with open(f"Keyword_{tagNamee}_YouTubeSeriouse_5.csv", 'w', newline='', encoding='cp1251',  errors="ignore") as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['LINK','TITLE', 'ID_CHANEL', 'DESCRIPTION_CHANEL', 'VIDEO_DESCRIPTION_AND_CONTACTS', 'CONTACTS', 'EMAIL'])
            for item in result_proto:
               writer.writerow([item['link'], item ['title'], item['id_chanel'], item['descriptionChanel'], item['videoDescription_Contacts'], item['contacts'], item['email']])
def main():    
    asyncio.run(gather_searcher())
    finish_time = time.time() - start_time
    appenderTube()
    wrritter()    
    print(f"Длинна выхоного массива:__{len(result_proto)}")
    print(f"Затраченное на работу скрипта время: {finish_time}")

if __name__ == "__main__":
    main()
         
# python api_by_key_words.py