import requests,http.cookiejar 
import json  
import os,time
import qrcode,tqdm
import tkinter
from tkinter import ttk
class biliLogin:
    def QR(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'
        }
        respone = requests.get('http://passport.bilibili.com/qrcode/getLoginUrl').json()
        oauthKey = respone['data']['oauthKey']
        QRimg = qrcode.make('https://passport.bilibili.com/qrcode/h5/login?oauthKey='+oauthKey)
        QRimg.show(title='扫描完成后关闭')
        while True:
            try:
                time.sleep(2)
                auth = requests.post('http://passport.bilibili.com/qrcode/getLoginInfo',headers=headers,data={'oauthKey':oauthKey})
                if auth:
                    if auth.json()['code'] == 0:
                        print('200 OK AUTHED.')
                        with open('login.data','w') as data:
                            print('正在保存登录依据到login.data')
                            data.write(auth.cookies.get('SESSDATA'))
                            return auth.cookies.get('SESSDATA')
                    else:
                        return False
                else:
                    return False
            except:
                print('没登陆')
    
    def loginData(self):
        if os.path.isfile('login.data'):
            SESSDATA = open('login.data','r').read()
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0','Cookie':'SESSDATA='+SESSDATA}
            user = requests.get('http://api.bilibili.com/nav',headers=headers)
            if user:
                return SESSDATA
            else:
                return 'notlogin'
        else:
            return 'notlogin'   
        
                 

def getVideo(SESSDATA,vid,cid,qn):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
        'Cookie':'SESSDATA=' + SESSDATA,
        'Referer':'https://www.bilibili.com'
    }
    videoInfo = requests.get('http://api.bilibili.com/x/web-interface/view?bvid='+vid,headers=headers).json()
    print('标题:'+videoInfo['data']['title'])
    videoData = requests.get('http://api.bilibili.com/x/player/playurl?bvid=' + vid + '&cid=' + str(cid) + '&fourk=1' + '&qn=' + qn,headers=headers)
    lista = videoData.json()['data']['durl']
    print('开始下载....')
    for i in lista:
        videoStreamUrl = videoData.json()['data']['durl'][lista.index(i)]['url']
        videoStream = requests.get(videoStreamUrl,headers=headers,stream=True)
        videoSize = int(int(videoStream.headers['Content-Length'])/1024+0.5)
        with open('./'+str(cid)+str(lista.index(i))+'.flv','wb+') as video:
            for chunk in tqdm.tqdm(iterable=videoStream.iter_content(1024),total=videoSize,unit='k',desc=None):
                if chunk:
                    video.write(chunk)
                    
        #print('转码中...' + str(cid) + str(lista.index(i))+'.mp4')
        #os.system('ffmpeg.exe -i '+str(cid)+str(lista.index(i))+'.flv '+str(cid)+str(lista.index(i))+ '.mp4')
        os.rename(str(cid)+str(lista.index(i))+'.flv',videoInfo['data']['title']+cid+'第'+str(int(lista.index(i)+1))+'段.flv')
        #os.remove(str(cid)+str(lista.index(i))+'.flv')
    exit()
def getVideoInfo(SESSDATA,bvid):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
        'Cookie':'SESSDATA=' + SESSDATA,
        'Referer':'https://www.bilibili.com'
    }
    videoInfo = requests.get('http://api.bilibili.com/x/web-interface/view?bvid='+bvid,headers=headers).json()
    return videoInfo

def gui(SESSDATA):
    mainGui = tkinter.Tk()
    mainGui.title('bilibili')
    mainGui.geometry('300x500')
    l1=tkinter.Label(mainGui,text='BV号:') 
    l1.pack()
    l2=tkinter.Label(mainGui,text='请选择分P:')
    l3=tkinter.Label(mainGui,text='请选择清晰度:')
    qntips=tkinter.Label(mainGui,text=qntip)
    cidchoose=ttk.Combobox(mainGui)
    qnchoose=ttk.Combobox(mainGui)
    bvinput=tkinter.Entry()
    bvinput['width']=250
    bvinput.pack()
    chooses=[]
    cidlist=[]
    def getdata():
        bvid=bvinput.get()
        if bvid:
            data=getVideoInfo(SESSDATA,bvid)
            videoNumber=data['data']['videos']
            for i in range(1,int(videoNumber+1)):
                chooses.append(str(i))
                cidlist.append(data['data']['pages'][int(i-1)]['cid'])
                print(chooses)
            cidchoose['value']=chooses
            cidchoose.current(0)
            cidchoose['width']=250
            l2.pack()
            cidchoose.pack()
            l3.pack()
            b2.pack()
            b1.pack_forget()
    def getqnlist():
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
                'Cookie':'SESSDATA=' + SESSDATA,
                'Referer':'https://www.bilibili.com'
            }
            choose=cidchoose.get()
            if choose:
                videoqn=requests.get('https://api.bilibili.com/x/player/playurl?bvid='+bvinput.get()+'&cid='+str(cidlist[int(int(choose)-1)]),headers=headers).json()
                qnlist=videoqn['data']['accept_quality']
                qnchoose['value']=qnlist
                qnchoose['width']=250
                b2.pack_forget()
                qnchoose.pack()
                qntips.pack()
                qnchoose.current(0)
                b3.pack()
    def download():
        choose=qnchoose.get()
        if choose:
            bvid=bvinput.get()
            cid=str(cidlist[int(int(cidchoose.get())-1)])
            qn=str(qnchoose.get())
            getVideo(SESSDATA,bvid,cid,qn)
    b1=tkinter.Button(mainGui,text='获取',command=getdata)
    b2=tkinter.Button(mainGui,text='点击获取清晰度列表',command=getqnlist) 
    b3=tkinter.Button(mainGui,text='下载!',command=download)
    b1['width']=250
    b1.pack()
    b2['width']=250
    mainGui.mainloop()

    


if __name__ == '__main__': 
    tips = '''
    本python脚本由IMIN制作。QQ:3377911508. 本人只有14岁希望大家多多包涵。。
    感谢SocialSisterYi.
    在工作中使用了https://github.com/SocialSisterYi/bilibili-API-collect.
    使用前必须安装qrcode requests tqdm这三个库。
    没有建议pip install qrcode && pip install requests && pip install tqdm
    在二维码扫描完成后关闭二维码窗口才能继续。
    在二维码扫描完成后关闭二维码窗口才能继续。
    在二维码扫描完成后关闭二维码窗口才能继续。
    （好像是因为qrimg.show会阻塞线程）
    '''
    canlogin=biliLogin().loginData()
    qntip='''    
    代码  值  含义
    16	360P 流畅
    32	480P 清晰
    64	720P 高清（登录）
    74	720P60 高清（大会员）
    80	1080P 高清（登录）
    112	1080P+ 高清（大会员）
    116	1080P60 高清（大会员）
    120	4K 超清（大会员）
    '''
    if not canlogin == 'notlogin':
        SESS=canlogin
        gui(SESSDATA=SESS)
    else:
        QRDATA = biliLogin().QR()
        if not QRDATA == False:
            SESS=QRDATA
            gui(SESSDATA=SESS)