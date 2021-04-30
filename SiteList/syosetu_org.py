from SiteList._requirement_func import *

baseURL = 'https://syosetu.org'



def main(novelURL, chat_id, bot):
    R_18 = False
    novel_id = sub('[\D]', '', novelURL)


    soup = GetSoup(novelURL, baseURL)
    

    if 'あなたは18歳以上ですか？' in str(soup):
        R_18 = True
        soup = GetSoup(baseURL+f'/novel/?mode=r18_cs_end&nid={novel_id}volume=', baseURL)


    try:
        bigTitle = soup.find('span', {'itemprop':'name'}).text
    except AttributeError:
        bot.sendMessage(chat_id, "주소를 잘 입력했는지 확인해주세요!")
        return
    

    author = soup.find('span', {'itemprop':'author'}).text
    c = soup.find('div', {'id':'maind'}).find_all('div', {'class':'ss'})[2].find_all('tr')


    titleList = []
    for i in c:
        l = i.find_all('a', {'style':'text-decoration:none;'})
        if len(l) != 0:
            titleList.append(l[0].text)


    epiCount = len(titleList)
    
    T_Title = t_j2k(bigTitle)
    
    # clear()
    # print(banner)

    info_text = f"\n제목: {T_Title}" + \
                  f"\n\n작가: {author}" + \
                  f"\n\n소설 주소: {novelURL}" + \
                  f"\n\n회차수: {len(titleList)}\n"

    bot.sendMessage(chat_id, info_text)


    T_Content = f"원본: {novelURL}\n저자: {author}\n\n\n"

    for i, j in enumerate(titleList):
        PrintProgressbar(i+1, epiCount, prefix='[번역 진행도]', suffix=f'({i+1}/{epiCount})', length=50)

        monoEpi = u""

        if R_18:
            epiURL = f'https://syosetu.org/novel/?mode=r18_cs_end&nid={novel_id}&volume={i+1}'
        else:
            epiURL = f'https://syosetu.org/novel/{novel_id}/{i+1}.html'
        
            
        nSoup = GetSoup(epiURL, baseURL).find('div', {'id':'honbun'}).find_all('p')

        monoEpi += f'\n\n[{i+1}/{epiCount}] ' + j + '\n' + '-'*100 

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