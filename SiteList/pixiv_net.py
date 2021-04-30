from SiteList._requirement_func import *


baseURL = 'https://www.pixiv.net/novel/'

def main(novelURL, chat_id, bot):

    novelId = sub('[\D]', '', novelURL)

    soup = GetSoup(novelURL, baseURL)
    info = loads(soup.find('meta', {'id':'meta-preload-data'})['content'])

    pCount = int(info['novel'][novelId]['pageCount'])
    author = info['novel'][novelId]['userName']

    try:
        bigTitle = soup.find('meta', {'property':'twitter:title'})['content']
    except AttributeError:
        bot.sendMessage(chat_id, "주소를 잘 입력했는지 확인해주세요!")
        return


    T_Title = t_j2k(bigTitle)

    # clear()
    # print(banner)
    
    info_text = f"\n제목: {T_Title}" + \
                  f"\n\n작가: {author}" + \
                  f"\n\n소설 주소: {novelURL}" + \
                  f"\n\n페이지 수: {pCount}\n"

    bot.sendMessage(chat_id, info_text)


    T_Content = f"원본: {novelURL}\n저자: {author}\n\n\n"

    for i in range(pCount):
        PrintProgressbar(i+1, pCount, prefix='[번역 진행도]', suffix=f'({i+1}/{pCount})', length=50)

        rURL = novelURL + f'#{i+1}'
        rSoup = GetSoup(rURL, baseURL)

        monoEpi = loads(rSoup.find('meta', {'id':'meta-preload-data'})['content'])['novel'][novelId]['content'].replace('[newpage]', '')
        
        T_Content += t_j2k(monoEpi)
        break

    

    f_name = GetFileName(T_Title)

    WriteFile(T_Content, dirLoc+f_name+'.txt')

    # clear()
    print(f'"{dirLoc+f_name}.txt" 로 저장되었습니다.')

    bot.sendDocument(chat_id, codecs.open(dirLoc+f_name+'.txt', 'r', encoding='utf-8'))
    remove(dirLoc+f_name+'.txt')