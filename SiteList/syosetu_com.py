from SiteList._requirement_func import *

baseURL_R15 = 'ncode.syosetu.com'

baseURL_R18 = 'novel18.syosetu.com'


def main(novelURL, chat_id, bot):
    R_18 = False

    if list(novelURL)[-1] != '/':
        novelURL += '/'

    if baseURL_R18 in novelURL:
        R_18 = True
        baseURL = 'http://' + baseURL_R18

    else:
        baseURL = 'http://' + baseURL_R15

    if not 'http' in novelURL:
        novelURL = 'http://' + novelURL
    
    
    soup = GetSoup(novelURL, 'https://syosetu.com')


    try:
        bigTitle = soup.find('p', {'class':'novel_title'}).text
    except AttributeError:
        bot.sendMessage(chat_id, "주소를 잘 입력했는지 확인해주세요!")
        return



    author = soup.find('div', {'class':'novel_writername'}).text.replace('\n', '').replace('作者：', '')
    
    titleList = [i.text.replace('\n', '') for i in soup.find('div', {'class':'index_box'}).find_all('dd', {'class':'subtitle'})]


    epiCount = len(titleList)
    
    T_Title = t_j2k(bigTitle)
    
    # clear()
    # print(banner)

    info_text = f"\n제목: {T_Title}" + \
                  f"\n\n작가: {author}" + \
                  f"\n\n소설 주소: {novelURL}" + \
                  f"\n\n회차수: {epiCount}\n"

    bot.sendMessage(chat_id, info_text)

    T_Content = f"원본: {novelURL}\n저자: {author}\n\n\n"

    for i, j in enumerate(titleList):
        PrintProgressbar(i+1, epiCount, prefix='[번역 진행도]', suffix=f'({i+1}/{epiCount})', length=50)

        monoEpi = ""

        epiURL = novelURL+f'{i+1}'

        nSoup = GetSoup(epiURL, baseURL).find('div', {'id':'novel_honbun'}).find_all('p')

        monoEpi += f'[{i+1}/{epiCount}] ' + j + '\n' + '-'*100

        for n in nSoup:
            monoEpi += ('\n' + str(n.text))

        monoEpi += '\n\n\n\n\n\n'

        monoEpi = monoEpi.replace('(・)', '')

        T_Content += t_j2k(monoEpi)

        

    f_name = GetFileName(T_Title)
    if R_18:
        f_name = '[R-18] '+f_name


    WriteFile(T_Content, dirLoc+f_name+'.txt')

    # clear()
    print(f'"{dirLoc+f_name}.txt" 로 저장되었습니다.')

    bot.sendDocument(chat_id, codecs.open(dirLoc+f_name+'.txt', 'r', encoding='utf-8'))
    remove(dirLoc+f_name+'.txt')