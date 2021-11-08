import requests 
from facebook_scraper import get_posts
from bs4 import BeautifulSoup
def login(urlpost):
    session = requests.Session()
    cookies = creat_cookies()
    print(cookies)
    headers = {
    "Host": "mbasic.facebook.com",
    "Cookie":cookies ,
    "Sec-Fetch-Site": "same-origin",
    "Referer":urlpost ,
    "Connection": "close"
    }
    session.headers.update(headers)
    a = session.get(url=urlpost)
    return session
def get_uid(url,session):
    #get link like in post
    session.get(url, headers=dict(referer = url))
    text = session.get(url=url)
    soup = BeautifulSoup(text.text, 'lxml')
    f = open('uid.txt','a',encoding='utf8')
    link = soup.find_all('a', href=True)
    link_Like = ''
    for i in link:
        if "/ufi/reaction/profile/browser/?ft_ent_identifier" in i['href']:
            link_Like = i['href']
            break
    #get  uid
    continues = True
    t = 0
    while continues:
        link_uid = []
        l = getAllUid(link_Like,session)
        link_Like = l[1]
        link_uid = l[0]
        if len(link_uid) == 0:
            continues = False
        else:
            
            for uid in link_uid:
                t = t +1
                print( t , ' : ',uid)
                f.write(uid + '\n')
def getAllUid(link_Like,session):
    url = 'https://mbasic.facebook.com/' + link_Like
    session.get(url, headers=dict(referer = url))
    res = session.get(url=url)
    soup = BeautifulSoup(res.text, 'html.parser')
    link = soup.find_all('a', href=True)
    s = 0
    listUid=[]
    listlink = []
    for i in link:
        listlink.append(i['href'])
        if ( ('profile.php?id=' in (i['href']) ) or ((i['href']).count('/') == 1) and len(i['href']) < 30):
            listUid.append(i['href'])
    link_next = listlink[len(listlink)-1]
    return listUid,link_next
def creat_cookies():
    f = open('cookies.txt','r')
    cookies = f.read()
    c1 = cookies.split('\n')
    lsb = c1[5]
    ldatr = c1[6]
    lc_user = c1[7]
    lxs = c1[8]
    lfr = c1[9]
    lspin = c1[10]
    sb = (lsb.split('\t'))[6]
    datr = (ldatr.split('\t'))[6]
    c_user = (lc_user.split('\t'))[6]
    xs = (lxs.split('\t'))[6]
    fr = (lfr.split('\t'))[6]
    spin = (lspin.split('\t'))[6]
    outcookies = 'sb=' + sb \
        + '; datr=' + datr \
        + '; c_user=' + c_user \
        + '; xs=' + xs\
        + '; fr=' + fr \
        + '; spin=' + spin +';'
    return outcookies
def scanPost(id):
    i = 0
    lPostID = []
    i=0
    for post in get_posts(id,cookies = 'cookies.txt' ,page = 2):
        i =i+1
        print('post id : ' ,post['post_id'] )
        lPostID.append(post['post_id'])
    return lPostID
#list id group
ids =['1228169470849996']
#url Referer
urlReferer = "https://mbasic.facebook.com"
session = login(urlReferer)
#start crawl
for id in ids:
    #get list post
    lPostID = scanPost(id)
    #get list Uid by post
    for Pid in lPostID:
        urlpost1 = "https://mbasic.facebook.com/groups/" + id +  "/posts/" + Pid + "/"
        get_uid(urlpost1,session)

