from SiteList._requirement_func import *

baseURL = 'https://novelist.jp'
baseURL2 = 'https://2.novelist.jp'

def main(novelURL, chat_id, bot):
    soup = GetSoup(novelURL, baseURL)

    try:
        bigTitle = soup.select_one('#work_detail > h2').text
    except AttributeError:
        bot.sendMessage(chat_id, "주소를 잘 입력했는지 확인해주세요!")
        return

    T_Title = t_j2k(bigTitle)

    winfo = soup.find('div', {'class':'work_right'})

    author = winfo.p.a.text

    epiCount = int(sub('[\D]', '', str(winfo.find_all('p')[1]).split('<br/>')[1]))


    info_text = f"\n제목: {T_Title}" + \
                  f"\n\n작가: {author}" + \
                  f"\n\n소설 주소: {novelURL}" + \
                  f"\n\n페이지 수: {epiCount}\n"

    bot.sendMessage(chat_id, info_text)


    T_Content = f"원본: {novelURL}\n저자: {author}\n\n\n"
    
    for i in range(epiCount):
        PrintProgressbar(i+1, epiCount, prefix='[번역 진행도]', suffix=f'({i+1}/{epiCount})', length=50)

        rURL = novelURL.replace('.html', f'_p{i+1}.html')

        rSoup = GetSoup(url=rURL, referer=novelURL).find('div', {'class':'work_read'})
        rSoup.find('div', {'class':'work_read_header'}).extract()
        
        monoEpi = ""

        monoEpi += f'[{i+1}/{epiCount}]'+ '\n' + '-'*100
        monoEpi += rSoup.text
        monoEpi += '\n\n\n\n\n\n'

        T_Content += t_j2k(monoEpi)
        

    f_name = GetFileName(T_Title)
    WriteFile(T_Content, dirLoc+f_name+'.txt')

    # clear()
    print(f'"{dirLoc+f_name}.txt" 로 저장되었습니다.')

    bot.sendDocument(chat_id, codecs.open(dirLoc+f_name+'.txt', 'r', encoding='utf-8'))
    remove(dirLoc+f_name+'.txt')