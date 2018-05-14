import requests
http_proxy  = "dev-proxy.oa.com:8080"
https_proxy = "dev-proxy.oa.com:8080"
proxyDict = {
              "http"  : http_proxy,
              "https" : https_proxy,
            }
cookies = dict(
    SINAGLOBAL="14.17.22.34_1448252810.829171",
    SGUID="1456968469334_6609832",
    vjuids="-23af4e26.1533a169202.0.182063c9",
    U_TRS1="00000022.ff0e4c73.56d7932e.215864ac",
    UOR="www.google.com.hk,blog.sina.com.cn,",
    SR_SEL="1_511",
    vjlast="1518428925",
    FIN_ALL_VISITED="sz399005%2Csh603348%2Csz002889%2Csz000725%2Csz000651%2Csz300077%2Csh600030%2Csz002049%2Csh000001",
    FINA_V_S_2="sz399005,sh603348,sz002889,sz000725,sz000651,sz300077,sh600030,sz002049,sh000001,sh600036,sh603533",
    FINA_V5_HQ="0",
    FINA_DMHQ="1",
    SCF='Ai5LLN-GLCaPMZohR0RzHEpLU7Vk2r7LvxMNZ4sNsmROPZOpMpf-B4ySqXf31yj50b7znNo5CToYlN4Cpu1NwBI.',
    lxlrtst="1525444416_o",
    Apache="14.17.22.33_1525776024.847723",
    ULV="1525776026516:32:6:2:14.17.22.33_1525776024.847723:1525776024580",
    U_TRS2="00000021.bdcc7ca7.5af17e9d.b503858b",
    FINANCE2="16cdb66a3cc3918e98465d5ef39137bd",
    hqEtagMode="1",
    directAd_samsung="true",
    rotatecount="8",
    lxlrttp="1525745003",
    SINA_FINANCE="klkgogo006%3A5951457653%3A1",
    ALF="1557314008",
    sso_info="v02m6alo5qztaubhq2nm7adr4yDgLaJp5WpmYO0tY6TlLGNg5S3jaOUsw==",
    SUB="_2A2539fYMDeRhGeNH7lMV9SnKzj-IHXVUg2DErDV_PUJbm9BeLWvAkW9NSrd_Fy_MMV3Ocv0jPrOJ5vcHHCJ90Wf6",
    SUBP="0033WrSXqPxfM725Ws9jqgMF55529P9D9WW2HLT3ZkWmCsuGheTqTGJB5NHD95Qf1K-pSh-NSo-0Ws4DqcjZIcpu9cvrd057Sntt"
)

# r = requests.get('http://stock.finance.sina.com.cn/portfolio/api/json.php/HoldService.appendAttentionSymbol?slist=sz000651&pid=900515288&rn=1525777012280&type=cn', cookies=cookies, proxies=proxyDict)
#r = requests.get('http://stock.finance.sina.com.cn/portfolio/api/json.php/HoldService.appendAttentionSymbol?slist=sz000651&pid=900521994&rn=1525778895753&type=cn', cookies=cookies, proxies=proxyDict)
r = requests.get('http://stock.finance.sina.com.cn/portfolio/api/json.php/HoldService.appendAttentionSymbol?slist=sz000651,sz002010,&pid=900515288&rn=1525778895753&type=cn', cookies=cookies, proxies=proxyDict)

#获取组合
#http://stock.finance.sina.com.cn/portfolio/api/json.php/PortfolioService.getPyList?type=cn&rn=1525779358053

#http://stock.finance.sina.com.cn/portfolio/api/json.php/PortfolioService.createPortfolio?name=1&rn=1525778790876&type=cn

print(r.content)
print(r)