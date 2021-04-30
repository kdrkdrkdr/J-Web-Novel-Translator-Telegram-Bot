from SiteList._requirement_func import *

baseURL = 'https://www.alphapolis.co.jp'

def main(novelURL, chat_id, bot):
    soup = GetSoup(novelURL, baseURL)

    try:
        bigTitle = soup.find('h2', {'class':'title'}).text.replace('\n', '')
    except AttributeError:
        bot.sendMessage(chat_id, "주소를 잘 입력했는지 확인해주세요!")
        return

    T_Title = t_j2k(bigTitle)

    author = soup.find('div', {'class':'author'}).find('a').text

    e = soup.find('div', {'class':'episodes'}).find_all('div', {'class':'episode '})
    epiCount = len(e)

    titleList = [i.find('span', {'class':'title'}).text for i in e]
    linkList = [baseURL + i.find('a')['href'] for i in e]

    info_text = f"\n제목: {T_Title}" + \
                  f"\n\n작가: {author}" + \
                  f"\n\n소설 주소: {novelURL}" + \
                  f"\n\n회차수: {epiCount}\n"

    bot.sendMessage(chat_id, info_text)


    T_Content = f"원본: {novelURL}\n저자: {author}\n\n\n"
    
    for i in range(epiCount):
        PrintProgressbar(i+1, epiCount, prefix='[번역 진행도]', suffix=f'({i+1}/{epiCount})', length=50)

        monoEpi = ""
        
        epiTitle = titleList[i]
        epiURL = linkList[i]

        nSoup = GetSoup(epiURL, baseURL).find('div', {'id':'novelBoby'}).text.replace('\t', '').replace('\n', '\n\n')

        monoEpi += f'[{i+1}/{epiCount}] ' + epiTitle + '\n' + '-'*100
        monoEpi += nSoup
        monoEpi += '\n\n\n\n\n\n'

        T_Content += t_j2k(monoEpi)
        

    f_name = GetFileName(T_Title)
    WriteFile(T_Content, dirLoc+f_name+'.txt')

    # clear()
    print(f'"{dirLoc+f_name}.txt" 로 저장되었습니다.')

    bot.sendDocument(chat_id, codecs.open(dirLoc+f_name+'.txt', 'r', encoding='utf-8'))
    remove(dirLoc+f_name+'.txt')