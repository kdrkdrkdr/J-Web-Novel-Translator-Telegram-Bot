from SiteList._requirement_func import *

baseURL = 'https://kakuyomu.jp'

def main(novelURL, chat_id, bot):
    
    soup = GetSoup(novelURL, baseURL)

    try:
        bigTitle = soup.find('span', {'id':'catchphrase-body'}).text
    except AttributeError:
        bot.sendMessage(chat_id, "주소를 잘 입력했는지 확인해주세요!")
        return

    
    author = soup.find('span', {'id':'catchphrase-authorLabel'}).text

    T_Title = t_j2k(bigTitle)

    info = soup.find_all('li', {'class':'widget-toc-episode'})

    titleList = [i.find('span', {'class':'widget-toc-episode-titleLabel js-vertical-composition-item'}).text for i in info]
    linkList = [baseURL+i.find('a')['href'] for i in info]

    epiCount = len(titleList)

    info_text = f"\n제목: {T_Title}" + \
                f"\n\n작가: {author}" + \
                f"\n\n소설 주소: {novelURL}" + \
                f"\n\n회차 수: {epiCount}\n"

    bot.sendMessage(chat_id, info_text)


    T_Content = f"원본: {novelURL}\n저자: {author}\n\n\n"

    for i in range(epiCount):
        PrintProgressbar(i+1, epiCount, prefix='[번역 진행도]', suffix=f'({i+1}/{epiCount})', length=50)

        epiURL = linkList[i]
        epiTitle = titleList[i]

        monoEpi = ""

        rSoup = GetSoup(epiURL, baseURL).find('div', {'class':'widget-episodeBody js-episode-body'}).find_all('p')

        monoEpi += f'[{i+1}/{epiCount}] ' + epiTitle + '\n' + '-'*100 + '\n'

        for r in rSoup:
            monoEpi += '\n'+(str(r.text))

        monoEpi += '\n\n\n\n\n\n'

        T_Content += t_j2k(monoEpi)


    f_name = GetFileName(T_Title)

    WriteFile(T_Content, dirLoc+f_name+'.txt')

    # clear()
    print(f'"{dirLoc+f_name}.txt" 로 저장되었습니다.')

    bot.sendDocument(chat_id, codecs.open(dirLoc+f_name+'.txt', 'r', encoding='utf-8'))
    remove(dirLoc+f_name+'.txt')