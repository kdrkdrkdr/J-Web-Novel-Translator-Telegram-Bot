from SiteList._requirement_func import *

baseURL = 'https://estar.jp/novels'

def main(novelURL, chat_id, bot):
    
    soup = GetSoup(novelURL, baseURL)

    try:
        bigTitle = soup.find('h1', {'class':'title'}).text
    except AttributeError:
        bot.sendMessage(chat_id, "주소를 잘 입력했는지 확인해주세요!")
        return

    author = soup.find('a', {'class':'link nickname'}).text

    T_Title = t_j2k(bigTitle)

    pCount = int(GetSoup(novelURL+'/viewer?page=1', baseURL).find('input', {'type':'number'})['max'])

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

        rURL = novelURL + f'/viewer?page={i+1}'
        rSoup = GetSoup(rURL, baseURL)

        monoEpi = ""
        try:
            sTitle = rSoup.find('h1', {'class':'subject'}).text
        except AttributeError:
            sTitle = ""


        monoEpi += f'\n\n\n[{i+1}/{pCount}] ' + sTitle + '\n' + '-'*100 + '\n'

        monoEpi += rSoup.find('div', {'lang':'ja'}).text
        
        if sTitle != "":
            monoEpi = '\n\n\n\n\n\n' + monoEpi

        T_Content += t_j2k(monoEpi)

    

    f_name = GetFileName(T_Title)

    WriteFile(T_Content, dirLoc+f_name+'.txt')

    # clear()
    print(f'"{dirLoc+f_name}.txt" 로 저장되었습니다.')

    bot.sendDocument(chat_id, codecs.open(dirLoc+f_name+'.txt', 'r', encoding='utf-8'))
    remove(dirLoc+f_name+'.txt')