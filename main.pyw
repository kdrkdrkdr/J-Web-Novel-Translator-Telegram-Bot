

from telepot import Bot, glance
from telepot.loop import MessageLoop
import time


from SiteList import (
    syosetu_org,
    syosetu_com,
    alphapolis_co_jp,
    pixiv_net,
    estar_jp,
    kakuyomu_jp,
    tinami_com,
    novelist_jp,
)

from SiteList._translate_j2k import t_j2k
from SiteList._requirement_func import *

from threading import Thread

token = ''

help_msg = '''안녕하세요! 일본 웹소설 번역봇 입니다!

[도움말]

#웹소설 번역:
웹 소설 목차 주소를 보내시면 됩니다.
횟차가 많을수록 번역본 전송 시간이 길어집니다.
가능한 사이트: 하멜룬, 소설가가 되자, 소설가가 되자 R-18, 알파폴리스, 픽시브, 카쿠요무, 에브리스타

#웹페이지 번역: (지원X)
웹페이지의 링크를 보내시면 됩니다.
현재 윈도우 버전으로 따로 개발중입니다.

#텍스트 번역:
번역할 단어나 문장을 보내시면 됩니다.

#첨부 파일 번역:
번역할 파일을 전송하시면 됩니다.
가능한 파일: 사진, 텍스트, 워드, 파워포인트, 녹음파일
'''




def bot_handler(msg):

    try:

        msg_type, chat_type, chat_id, msg_data, msg_id = glance(msg, long=True)
        MessageLog(msg)

            
        if msg_type == 'text':
            msg_text = msg['text']
            

            try:
                entity_type = msg['entities'][0]['type']
            except KeyError:
                entity_type = False

            
            if msg_text in ['/start', '도움말']:
                t = Thread(target=j2k_transbot.sendMessage, args=(chat_id, help_msg))


            elif entity_type == 'url':
                msg_text = msg_text.replace(' ', '')

                if syosetu_org.baseURL in msg_text:
                    t = Thread(target=syosetu_org.main, args=(msg_text, chat_id, j2k_transbot))
                            
                elif (syosetu_com.baseURL_R15 in msg_text) or (syosetu_com.baseURL_R18 in msg_text):
                    t = Thread(target=syosetu_com.main, args=(msg_text, chat_id, j2k_transbot))

                elif alphapolis_co_jp.baseURL in msg_text:
                    t = Thread(target=alphapolis_co_jp.main, args=(msg_text, chat_id, j2k_transbot))
                
                elif pixiv_net.baseURL in msg_text:
                    t = Thread(target=pixiv_net.main, args=(msg_text, chat_id, j2k_transbot))

                elif estar_jp.baseURL in msg_text:
                    t = Thread(target=estar_jp.main, args=(msg_text, chat_id, j2k_transbot))

                elif kakuyomu_jp.baseURL in msg_text:
                    t = Thread(target=kakuyomu_jp.main, args=(msg_text, chat_id, j2k_transbot))

                elif tinami_com.baseURL in msg_text:
                    t = Thread(target=tinami_com.main, args=(msg_text, chat_id, j2k_transbot))

                elif (novelist_jp.baseURL in msg_text or novelist_jp.baseURL2 in msg_text):
                    t = Thread(target=novelist_jp.main, args=(msg_text, chat_id, j2k_transbot))

                else:
                    t = Thread(target=GetTextInWebpage, args=(msg_text, chat_id, j2k_transbot))
                    

            else:
                t = Thread(target=SendLongMessage, args=(msg_text, chat_id, j2k_transbot))


            
        elif msg_type == 'document':
            t = Thread(target=GetTextInDocument, args=(msg[msg_type], chat_id, j2k_transbot))
        

        elif msg_type == 'photo':
            t = Thread(target=j2k_transbot.sendMessage, args=(chat_id, '사진은 첨부파일 형식으로 보내주세요!'))


        elif msg_type in ['audio', 'voice']:
            t = Thread(target=GetTextInAudio, args=(msg[msg_type], chat_id, j2k_transbot))

            
        else:
            t = Thread(target=j2k_transbot.sendMessage, args=(chat_id, help_msg))


        t.start()

    except:
        print("EXCEPTION")


if __name__ == "__main__":
    j2k_transbot = Bot(token)
    msg_loop = MessageLoop(j2k_transbot, bot_handler)
    msg_loop.run_as_thread()

    while True:
        sleep(10)