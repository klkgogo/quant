import requests
import time
import ast
http_proxy  = "dev-proxy.oa.com:8080"
https_proxy = "dev-proxy.oa.com:8080"
proxyDict = {
              "http"  : http_proxy,
              "https" : https_proxy,
            }

cookies_str = "SINAGLOBAL=14.17.22.34_1448252810.829171; SGUID=1456968469334_6609832; vjuids=-23af4e26.1533a169202.0.182063c9; U_TRS1=00000022.ff0e4c73.56d7932e.215864ac; UOR=www.google.com.hk,blog.sina.com.cn,; SR_SEL=1_511; vjlast=1518428925; FINA_DMHQ=1; SCF=Ai5LLN-GLCaPMZohR0RzHEpLU7Vk2r7LvxMNZ4sNsmROPZOpMpf-B4ySqXf31yj50b7znNo5CToYlN4Cpu1NwBI.; sso_info=v02m6alo5qztaubhq2nm7adr4yDgLaJp5WpmYO0tY6TlLGNg5S3jaOUsw==; lxlrtst=1525918316_o; FINA_V5_HQ=0; FIN_ALL_VISITED=sz002007%2Csh000001%2Csh601228%2Csz002271%2Csz002108%2Csz002399%2Csz002085%2Csz002340%2Csz002299%2Csz002491%2Csz002635%2Csz002285%2Csz002013%2Csz002411%2Csz002508%2Csz002311%2Csh603456%2Csz002038%2Csz002475%2Csz002573%2Csz002701%2Csz002572%2Csz002081%2Csz002010%2Csz002050%2Csz002179%2Csz399005%2Csh603348%2Csz002889%2Csz000725%2Csz000651%2Csz300077%2Csh600030%2Csz002049; rotatecount=4; FINA_V_S_2=sz002007,sh000001,sh601228,sz002271,sz002108,sz002399,sz002085,sz002340,sz002299,sz002491,sz002635,sz002285,sz002013,sz002411,sz002508,sz002311,sh603456,sz002038,sz002475,sz002573; U_TRS2=00000024.7c2b7d8f.5af42258.31e837f6; FINANCE2=64389c0b7b58b668bb4b6ef98bfa29da; Apache=14.17.22.36_1525949056.625766; ALF=1557485058; ULV=1525949058403:36:10:6:14.17.22.36_1525949056.625766:1525949056495; SUB=_2A2538FLUDeRhGeNH7lMV9SnKzj-IHXVUhMMcrDV_PUJbm9BeLVbSkW9NSrd_F1hez-IiC45qvkbEUF_YqsS4cjSt; lxlrttp=1525918316"

def eval_to_dict(str):
    ss = str.split(";")
    dict_str = "{"
    for s in ss:
        if len(s) == 0:
            continue
        v = s.split("=")
        dict_str = dict_str + '"' + v[0] + '"' + ':' + '"' + v[1] + '",'
    dict_str = dict_str + '}'
    return ast.literal_eval(dict_str)

cookies = eval_to_dict(cookies_str)
# cookies = dict(
#     SINAGLOBAL="14.17.22.34_1448252810.829171",
#     SGUID="1456968469334_6609832",
#     vjuids="-23af4e26.1533a169202.0.182063c9",
#     U_TRS1="00000022.ff0e4c73.56d7932e.215864ac",
#     UOR="www.google.com.hk,blog.sina.com.cn,",
#     SR_SEL="1_511",
#     vjlast="1518428925",
#     FIN_ALL_VISITED="sz399005%2Csh603348%2Csz002889%2Csz000725%2Csz000651%2Csz300077%2Csh600030%2Csz002049%2Csh000001",
#     FINA_V_S_2="sz399005,sh603348,sz002889,sz000725,sz000651,sz300077,sh600030,sz002049,sh000001,sh600036,sh603533",
#     FINA_V5_HQ="0",
#     FINA_DMHQ="1",
#     SCF='Ai5LLN-GLCaPMZohR0RzHEpLU7Vk2r7LvxMNZ4sNsmROPZOpMpf-B4ySqXf31yj50b7znNo5CToYlN4Cpu1NwBI.',
#     lxlrtst="1525444416_o",
#     Apache="14.17.22.33_1525776024.847723",
#     ULV="1525776026516:32:6:2:14.17.22.33_1525776024.847723:1525776024580",
#     U_TRS2="00000021.bdcc7ca7.5af17e9d.b503858b",
#     FINANCE2="16cdb66a3cc3918e98465d5ef39137bd",
#     hqEtagMode="1",
#     directAd_samsung="true",
#     rotatecount="8",
#     lxlrttp="1525745003",
#     SINA_FINANCE="klkgogo006%3A5951457653%3A1",
#     ALF="1557314008",
#     sso_info="v02m6alo5qztaubhq2nm7adr4yDgLaJp5WpmYO0tY6TlLGNg5S3jaOUsw==",
#     SUB="_2A2539fYMDeRhGeNH7lMV9SnKzj-IHXVUg2DErDV_PUJbm9BeLWvAkW9NSrd_Fy_MMV3Ocv0jPrOJ5vcHHCJ90Wf6",
#     SUBP="0033WrSXqPxfM725Ws9jqgMF55529P9D9WW2HLT3ZkWmCsuGheTqTGJB5NHD95Qf1K-pSh-NSo-0Ws4DqcjZIcpu9cvrd057Sntt"
# )

#富途格式SZ.002431 to sina 格式sz002431
def futu_to_sina_code(code):
    ss = code.split('.')
    sina = "%s%s" %( ss[0].lower(), ss[1])
    return sina;

def parse_result(str, key):
    str = str[2:-2]
    splits = str.split(",")
    result = 0
    pfid = 0
    for s in splits:
        if s.startswith(key):
            ss = s.split(":")
            return ss[1]
    return 0

def create_group(name):
    url = "http://stock.finance.sina.com.cn/portfolio/api/json.php/PortfolioService.createPortfolio?name=%s&rn=1525778790876&type=cn" % (name)
    r = requests.get(url, cookies=cookies, proxies=proxyDict)
    str = bytes.decode(r.content, encoding="GBK")
    result = parse_result(str, "result")
    if result != '1':
        print(str)
        print(url)
    pfid = parse_result(str, 'pfid')
    return result, pfid

def add_stock(group_id, stock_code):
    url  = 'http://stock.finance.sina.com.cn/portfolio/api/json.php/HoldService.appendAttentionSymbol?slist=%s&pid=%s&rn=1525777012280&type=cn' %(stock_code, group_id)
    r = requests.get(url, cookies=cookies, proxies=proxyDict)
    str = bytes.decode(r.content, encoding="GBK")
    result = parse_result(str, "result")
    if result != '1':
        print(str)
        print(url)
    return result


def add_to_sina_account(group, stock_list):
    _, pid = create_group(group)
    code_list = ""
    count = 0
    total = 0
    stock_list=stock_list[::-1]
    for ix, row in stock_list.iterrows():
        count = count + 1
        total = total + 1
        code_list = futu_to_sina_code(row['code']) + "," + code_list
        if count > 5:
            add_stock(pid, code_list)
            print("add stock to %s, %d " % (group,  total))
            count = 0
            code_list = ''
    add_stock(pid, code_list)
    print("add stock to %s end, total %d " % (group, total))

# # r = requests.get('http://stock.finance.sina.com.cn/portfolio/api/json.php/HoldService.appendAttentionSymbol?slist=sz000651&pid=900515288&rn=1525777012280&type=cn', cookies=cookies, proxies=proxyDict)
# #r = requests.get('http://stock.finance.sina.com.cn/portfolio/api/json.php/HoldService.appendAttentionSymbol?slist=sz000651&pid=900521994&rn=1525778895753&type=cn', cookies=cookies, proxies=proxyDict)
# r = requests.get('http://stock.finance.sina.com.cn/portfolio/api/json.php/HoldService.appendAttentionSymbol?slist=sz000651&pid=900521995&rn=1525778895753&type=cn', cookies=cookies, proxies=proxyDict)
#
# #获取组合
# #http://stock.finance.sina.com.cn/portfolio/api/json.php/PortfolioService.getPyList?type=cn&rn=1525779358053
#
# #http://stock.finance.sina.com.cn/portfolio/api/json.php/PortfolioService.createPortfolio?name=1&rn=1525778790876&type=cn
#
# print(r.content)
# print(r)
if __name__ == '__main__':
    result, pfid = create_group("abc")
    add_stock(pfid, futu_to_sina_code("SZ.002010"))
    d = eval_to_dict("SINAGLOBAL=14.17.22.34_1448252810.829171; SGUID=1456968469334_6609832;")


    print(result, pfid)
    print(cookies_str)
