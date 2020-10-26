import requests,http.cookiejar 
import json  
import os,time
import qrcode
def QRLogin():
    if os.path.isfile('login.data'):
        print('发现保存的登录依据,正在尝试登陆')
        SESSDATA = open('login.data','r').read()
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0','Cookie':'SESSDATA='+SESSDATA}
        user = requests.get('http://api.bilibili.com/nav',headers=headers).json()
        print('成功:用户名:'+user['data']['uname'])
        getVideo(SESSDATA=SESSDATA)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'
    }
    respone = requests.get('http://passport.bilibili.com/qrcode/getLoginUrl').json()
    oauthKey = respone['data']['oauthKey']
    QRimg = qrcode.make('https://passport.bilibili.com/qrcode/h5/login?oauthKey='+oauthKey)
    QRimg.show(title='扫描完成后关闭')
    print('检测到二维码窗口已经关闭,正在检测是否扫描或确认！')
    for sec in range(0,10):
        time.sleep(1)
        print(sec)
        auth = requests.post('http://passport.bilibili.com/qrcode/getLoginInfo',headers=headers,data={'oauthKey':oauthKey})
        if auth.json()['code'] == 0:
            print('200 OK AUTHED.')
            with open('login.data','w') as data:
                print('正在保存登录依据到login.data')
                data.write(auth.cookies.get('SESSDATA'))
            getVideo(SESSDATA=auth.cookies.get('SESSDATA'))
            break
        if sec == 10:
            print('超时！10秒内未检测到您扫描二维码！') 
            print('正在重新生成...')
            QRLogin()      

def getVideo(SESSDATA):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
        'Cookie':'SESSDATA=' + SESSDATA,
        'Referer':'https://www.bilibili.com'
    }
    vid = input('输入bv号，一定是bv号（因为我懒）:')
    videoInfo = requests.get('http://api.bilibili.com/x/web-interface/view?bvid='+vid,headers=headers).json()
    print('标题:'+videoInfo['data']['title'])
    pid = input('输入分P:')
    cid = videoInfo['data']['pages'][0]['cid']
    print(cid)
    qnlist = '''
    代码  值  含义
    6	240P 极速（仅mp4方式）
    16	360P 流畅
    32	480P 清晰
    64	720P 高清（登录）
    74	720P60 高清（大会员）
    80	1080P 高清（登录）
    112	1080P+ 高清（大会员）
    116	1080P60 高清（大会员）
    120	4K 超清（大会员）（需要fourk=1）
    '''
    print(qnlist)
    qn = input('输入清晰度对应代码:')
    videoData = requests.get('http://api.bilibili.com/x/player/playurl?bvid=' + vid + '&cid=' + str(cid) + '&fourk=1' + '&qn=' + qn,headers=headers).json()
    lista = videoData['data']['durl']
    print('开始下载....')
    for i in lista:
        videoStreamUrl = videoData['data']['durl'][lista.index(i)]['url']
        videoStream = requests.get(videoStreamUrl,headers=headers,stream=True)
        with open('./'+str(cid)+'.flv','wb+') as video:
            for chunk in videoStream.iter_content(chunk_size=1024):
                if chunk:
                    video.write(chunk)
        print('转码中...' + str(cid) + '.mp4')
        os.system('ffmpeg.exe -i ' + str(cid) + '.flv ' + str(cid) + '.mp4')
        os.system('del /f /s /q ' + str(cid) + '.flv')
    exit()


    

    


if __name__ == '__main__': 
    tips = '''
                         //                                                                                     \n
             \\         //                                                                                      \n 
              \\       //                                                                                       \n
        ##DDDDDDDDDDDDDDDDDDDDDD##                                                                              \n                         
        ## DDDDDDDDDDDDDDDDDDDD ##   ________   ___   ___        ___   ________   ___   ___        ___          \n
        ## hh                hh ##   |\   __  \ |\  \ |\  \      |\  \ |\   __  \ |\  \ |\  \      |\  \        \n
        ## hh    //    \\    hh ##   \ \  \|\ /_\ \  \\ \  \     \ \  \\ \  \|\ /_\ \  \\ \  \     \ \  \       \n
        ## hh   //      \\   hh ##    \ \   __  \\ \  \\ \  \     \ \  \\ \   __  \\ \  \\ \  \     \ \  \      \n 
        ## hh                hh ##     \ \  \|\  \\ \  \\ \  \____ \ \  \\ \  \|\  \\ \  \\ \  \____ \ \  \     \n
        ## hh      wwww      hh ##      \ \_______\\ \__\\ \_______\\ \__\\ \_______\\ \__\\ \_______\\ \__\    \n 
        ## hh                hh ##       \|_______| \|__| \|_______| \|__| \|_______| \|__| \|_______| \|__|    \n
        ## MMMMMMMMMMMMMMMMMMMM ##                                                                              \n
        ##MMMMMMMMMMMMMMMMMMMMMM##                                                                              \n
             \/            \/                   VIDEO   DOWNLOADER  BY  IMIN (GARBAGE)                          \n
    本python脚本由IMIN制作。QQ:3377911508. 本人只有14岁希望大家多多包涵。。
    感谢SocialSisterYi.
    在工作中使用了https://github.com/SocialSisterYi/bilibili-API-collect.
    使用前必须安装qrcode requests这两个库。
    没有建议pip install qrcode && pip install requests
    在二维码扫描完成后关闭二维码窗口才能继续。
    在二维码扫描完成后关闭二维码窗口才能继续。
    在二维码扫描完成后关闭二维码窗口才能继续。
    （好像是因为qrimg.show会阻塞线程）
    '''
    print(tips)
    os.system('pause')
    QRLogin() 