from SiteList._requirement_func import *

baseURL = 'http://www.tinami.com'



def main(novelURL, chat_id, bot):

    soup = GetSoup(novelURL, baseURL)

    try:
        bigTitle = sub('[\n\r\t]', '', soup.find_all('h1')[1].text)
    except AttributeError:
        bot.sendMessage(chat_id, "주소를 잘 입력했는지 확인해주세요!")
        return

    author = sub('[\n\r\t]', '', soup.find('div', {'class':'prof'}).text)


    T_Title = t_j2k(bigTitle)

    # clear()
    # print(banner)
    
    info_text = f"\n제목: {T_Title}" + \
                  f"\n\n작가: {author}" + \
                  f"\n\n소설 주소: {novelURL}"

    bot.sendMessage(chat_id, info_text)


    T_Content = f"원본: {novelURL}\n저자: {author}\n\n\n"

    monoEpi = '\n'.join([m.text for m in soup.find_all('p', {'class':'body_line'})])

    T_Content += t_j2k(monoEpi)


    

    f_name = GetFileName(T_Title)

    WriteFile(T_Content, dirLoc+f_name+'.txt')

    # clear()
    print(f'"{dirLoc+f_name}.txt" 로 저장되었습니다.')

    bot.sendDocument(chat_id, codecs.open(dirLoc+f_name+'.txt', encoding='utf-8'))