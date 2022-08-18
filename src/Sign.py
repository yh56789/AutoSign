import requests
import random
import time
import re
import rsa
import base64
from src.log import Log

log = Log()

class gtfed():
    """好游快爆签到
    """
    Url = 'https://huodong3.3839.com/n/hykb/grow/ajax.php'
    SowUrl = ""
    def __init__(self,SignToken) -> None:
        self.gtfed = SignToken['gtfed']['cookie']
        self.head = {
            "User-Agent":"Mozilla/5.0 (Linux; Android 7.0; Meizu S6 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/65.0.3325.110 Mobile Safari/537.36Androidkb/1.5.5.305(android;Meizu S6;7.0;720x1374;4G);@4399_sykb_android_activity@",
            "Origin":"https://huodong3.3839.com",
            "X-Requested-With":"XMLHttpRequest",
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
            "Referer":"https://huodong3.3839.com/n/hykb/grow/index.php",
	    }
        
    def Sign(self):
        if self.gtfed != "":
            zz = requests.post(url=self.Url,data=self.gtfed,headers=self.head).json()
            print(zz)
            if zz['key'] == 'ok':
                if zz['csd_jdt'] == "100%":
                    cookie = self.gtfed.replace("Watering","PlantRipe")
                    SowRes = requests.post(url=self.Url,data=cookie,headers=self.head).json()
                    if SowRes['key'] == 513:
                        cookie = self.gtfed.replace("Watering","PlantSow")
                        SowRes = requests.post(url=self.Url,data=cookie,headers=self.head).json()
                        if SowRes['key'] == "ok":
                            log.info("好游快爆:收获，重新播种完成")
                            return "好游快爆:收获，重新播种完成"
                        else:
                            log.info("好游快爆:收获完成，重新播种失败")
                            return "好游快爆:收获完成，重新播种失败"
                    else:
                        log.info("好游快爆:收获，重新播种完成")
                        return "好游快爆:收获，重新播种完成"
                else:
                    log.info("好游快爆:浇水完成")
                    return "好游快爆:浇水完成"
            elif  zz['key'] == '502':
                cookie = self.gtfed.replace("Watering","PlantRipe")
                SowRes = requests.post(url=self.Url,data=cookie,headers=self.head).json()
                if SowRes['key'] == 513:
                    cookie = self.gtfed.replace("Watering","PlantSow")
                    SowRes = requests.post(url=self.Url,data=cookie,headers=self.head).json()
                    if SowRes['key'] == "ok":
                        log.info("好游快爆:收获，重新播种完成")
                        return "好游快爆:收获，重新播种完成"
                    else:
                        log.info("好游快爆:收获，重新播种完成")
                        return "好游快爆:收获，重新播种完成"
                else:
                    log.info("好游快爆:收获失败，请手动收获")
                    return "好游快爆:收获失败，请手动收获"
            elif zz['key'] == '501':
                cookie = self.gtfed.replace("Watering","PlantSow")
                SowRes = requests.post(url=self.Url,data=cookie,headers=self.head).json()
                if SowRes['key'] == "ok":
                    log.info("好游快爆:收获，重新播种完成")
                    return "好游快爆:收获，重新播种完成"
                else:
                    log.info("好游快爆:收获完成，重新播种失败")
                    return "好游快爆:收获完成，重新播种失败"
            else:
                log.info(f"好游快爆:{zz['info']}")
                return f"好游快爆:{zz['info']}"
        else:
            log.info("好游快爆:没有配置cookie")
            return "好游快爆:没有配置cookie"
            
#MIUI 历史版本签到
class Miui():
    """MIUI 历史版本签到
    """
    LoginUrl = "https://miuiver.com/wp-content/plugins/erphplogin//action/login.php"
    SignUrl = "https://miuiver.com/wp-admin/admin-ajax.php"
    def __init__(self,SignToken) -> None:
        self.switch = SignToken['MiUI']['switch']
        self.user = SignToken['MiUI']['user']
        self.password = SignToken['MiUI']['password']
        self.head = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01'
        }
    #登录
    def Login(self):
        datas = {
            'log':self.user,
            'pwd':self.password,
            'action': 'mobantu_login'
        }
        response = requests.post(url=self.LoginUrl,data=datas,headers=self.head)
        if response.text == '1':
            log.info("MIUI历史版本:登录成功")
            if response.text.__eq__(1):
                cookies = response.cookies
                log.info("MIUI历史版本:cookies获取成功")
            else:
                cookies = "没有获取到cookie"
                log.info("MIUI历史版本:没有获取到cookie")
            return cookies
        else:
            log.info("MIUI历史版本:登录失败,账号或密码错误")
    #签到
    def Sign(self):
        datas = {
            'action': 'epd_checkin'
        }
        if self.user != "" and self.password != "":
            cookies = self.Login()
            if cookies == None:
                pass
            else:
                response = requests.post(url=self.SignUrl,data=datas,headers=self.head,cookies=cookies).json()
                if response['status'] == 200:
                    log.info("MIUI历史版本:" + "签到成功积分+1")
                    return "MIUI历史版本:" + "签到成功积分+1"
                else:
                    log.info("MIUI历史版本:" + response["msg"])
                    return "MIUI历史版本:" + response["msg"]
        else:
            log.info("MIUI历史版本:账号或密码为空")
            return "MIUI历史版本:账号或密码为空"

# 小黑盒签到
class XiaoHeiHe():
    def __init__(self,SignToken) -> None:
        self.Xiaoheihe = SignToken['XiaoHeiHe']['cookie']
        self.imei = SignToken['XiaoHeiHe']['imei']
        self.heybox_id = SignToken['XiaoHeiHe']['heybox_id']
        self.n = self.get_nonce_str()
        self.t = int(time.time())
        self.u = "/task/sign"

    def get_nonce_str(self,length: int = 32) -> str:
            """
            生成随机字符串

            参数:
                length: 密钥参数
            返回:
                str: 随机字符串
            """
            source = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
            result = "".join(random.choice(source) for _ in range(length))
            return(result)

    # 感谢 https://github.com/chr233 的hkey算法接口
    def hkey(self):
        url = "http://146.56.234.178:8077/encode"
        params={"urlpath": self.u, "nonce": self.n, "timestamp": self.t}
        zz = requests.get(url,params=params).text
        return zz
    
    def Sgin(self):
        if self.Xiaoheihe != "":
            try:
                url = "https://api.xiaoheihe.cn/task/sign/"
                p = {
                    "_time":self.t,
                    "hkey":self.hkey(),
                    "nonce":self.n,
                    "imei":self.imei,
                    "heybox_id":self.heybox_id,
                    "version":"1.3.229",
                    "divice_info":"M2012K11AC",
                    "x_app":"heybox",
                    "channel":"heybox_xiaomi",
                    "os_version":"12",
                    "os_type":"Android"
                }
                head = {
                    "User-Agent":"Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36 ApiMaxJia/1.0",
                    "cookie":self.Xiaoheihe,
                    "Referer":"http://api.maxjia.com/"
                }
                req = requests.get(url=url,params=p,headers=head).json()
                if req['status'] == "ok":
                    if req['msg'] == "":
                        log.info("小黑盒:已经签到过了")
                        return "小黑盒:已经签到过了"
                    else:
                        log.info(f"小黑盒:{req['msg']}")
                        return f"小黑盒:{req['msg']}"
                else:
                    log.info(f"小黑盒:签到失败 - {req['msg']}")
                    return f"小黑盒:签到失败 - {req['msg']}"
            except Exception as e:
                log.info(f"小黑盒:出现了错误,错误信息{e}")
        else:
            log.info("小黑盒:没有配置cookie")
            return "小黑盒:没有配置cookie"

# 交易猫签到
class JiaoYiMao():
    def __init__(self,SignToken) -> None:
        self.jiaoyimao = SignToken['JiaoYiMao']['cookie']
        self.url = "https://m.jiaoyimao.com/api2/account/integration/getMyIntegration"
        self.sginurl = "https://m.jiaoyimao.com/api2/account/integration/signin"

    def Sgin(self):
        if self.jiaoyimao != "":
            head = {
                "user-agent":"jym_mobile (Linux; U; Android12; zh_CN; M2012K11AC; Build/SKQ1.220213.001; fca7d8fc-03b5-4fea-97e6-94173844b374; 1080x2400) com.jym.mall/206/JYN_548/7.0.2 AliApp(JYM/7.0.2) UT4Aplus/0.2.29; density/2.7; app_id/23072786;  WindVane/8.5.0; utdid/YH2ygxDifiEDAA6wMV75K10e; umid_token/7+9LGztLOiq8MTWA+l8fZZQW+RjvBE56; oaid/9933af2363237087;",
                "referer":"https://m.jiaoyimao.com/account/integration/center?spm=gcmall.home2022.topshortcut.0",
                "x-csrf-token":"HT-x5YUi3IF7iyVDXY6FBc6g",
                "x-requested-with":"com.jym.mall",
                "cookie":self.jiaoyimao
            }
            try:
                zz = requests.get(url=self.sginurl,headers=head).json()
                if zz['success']:
                    rep = requests.get(self.url,headers=head).json()
                    if rep['stateCode'] == 200:
                        Integral = rep['data']['amountLeft']
                    else:
                        Integral = "获取积分失败"
                    data = f"交易猫:签到成功 - 现有积分{Integral}"
                    log.info(data)
                    return data
                else:
                    data = f"交易猫:签到失败 - 已经签到了"
                    log.info(data)
                    return data
            except Exception as e:
                log.info("交易猫:cookie可能已过期，或出现了错误")
                return "交易猫:cookie可能已过期，或出现了错误"
        else:
            log.info("交易猫:没有配置cookie")
            return "交易猫:没有配置cookie"

# 天翼云盘
# 使用了开源项目https://github.com/xtyuns/cloud189app-action
class TYYP():
    def __init__(self,SignToken) -> None:
        self.username = SignToken['tyyp']['username']
        self.password = SignToken['tyyp']['password']

    def int2char(self,a):
        BI_RM = list("0123456789abcdefghijklmnopqrstuvwxyz")
        return BI_RM[a]

    def b64tohex(self,a):
        d = ""
        e = 0
        c = 0
        b64map = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        for i in range(len(a)):
            if list(a)[i] != "=":
                v = b64map.index(list(a)[i])
                if 0 == e:
                    e = 1
                    d += self.int2char(v >> 2)
                    c = 3 & v
                elif 1 == e:
                    e = 2
                    d += self.int2char(c << 2 | v >> 4)
                    c = 15 & v
                elif 2 == e:
                    e = 3
                    d += self.int2char(c)
                    d += self.int2char(v >> 2)
                    c = 3 & v
                else:
                    e = 0
                    d += self.int2char(c << 2 | v >> 4)
                    d += self.int2char(15 & v)
        if e == 1:
            d += self.int2char(c << 2)
        return d

    def rsa_encode(self,j_rsakey, string):
        rsa_key = f"-----BEGIN PUBLIC KEY-----\n{j_rsakey}\n-----END PUBLIC KEY-----"
        pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(rsa_key.encode())
        result = self.b64tohex((base64.b64encode(rsa.encrypt(f'{string}'.encode(), pubkey))).decode())
        return result

    def Login(self,s,username,password):
        url = "https://cloud.189.cn/api/portal/loginUrl.action?redirectURL=https%3A%2F%2Fcloud.189.cn%2Fweb%2Fredirect.html"
        r = s.get(url)
        captchaToken = re.findall(r"captchaToken' value='(.+?)'", r.text)[0]
        lt = re.findall(r'lt = "(.+?)"', r.text)[0]
        returnUrl = re.findall(r"returnUrl = '(.+?)'", r.text)[0]
        paramId = re.findall(r'paramId = "(.+?)"', r.text)[0]
        j_rsakey = re.findall(r'j_rsaKey" value="(\S+)"', r.text, re.M)[0]
        s.headers.update({"lt": lt})
        username = self.rsa_encode(j_rsakey, username)
        password = self.rsa_encode(j_rsakey, password)
        url = "https://open.e.189.cn/api/logbox/oauth2/loginSubmit.do"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/76.0',
            'Referer': 'https://open.e.189.cn/',
        }
        data = {
            "appKey": "cloud",
            "accountType": '01',
            "userName": f"{{RSA}}{username}",
            "password": f"{{RSA}}{password}",
            "validateCode": "",
            "captchaToken": captchaToken,
            "returnUrl": returnUrl,
            "mailSuffix": "@189.cn",
            "paramId": paramId
        }
        r = s.post(url, data=data, headers=headers, timeout=5)
        if (r.json()['result'] == 0):
            log.info(f"天翼云盘:{r.json()['msg']}")
        else:
            log.info(f"天翼云盘:{r.json()['msg']}")
        try:
            redirect_url = r.json()['toUrl']
            r = s.get(redirect_url)
            return s
        except Exception:
            pass

    def Sgin(self):
        try:
            if self.username != "" and self.password != "":
                s = requests.Session()
                self.Login(s, self.username, self.password)
                rand = str(round(time.time() * 1000))
                surl = f'https://api.cloud.189.cn/mkt/userSign.action?rand={rand}&clientType=TELEANDROID&version=8.6.3&model=SM-G930K'
                url = f'https://m.cloud.189.cn/v2/drawPrizeMarketDetails.action?taskId=TASK_SIGNIN&activityId=ACT_SIGNIN'
                url2 = f'https://m.cloud.189.cn/v2/drawPrizeMarketDetails.action?taskId=TASK_SIGNIN_PHOTOS&activityId=ACT_SIGNIN'
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G930K Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 Ecloud/8.6.3 Android/22 clientId/355325117317828 clientModel/SM-G930K imsi/460071114317824 clientChannelId/qq proVersion/1.0.6',
                    "Referer": "https://m.cloud.189.cn/zhuanti/2016/sign/index.jsp?albumBackupOpened=1",
                    "Host": "m.cloud.189.cn",
                    "Accept-Encoding": "gzip, deflate",
                }
                # 签到
                response = s.get(surl, headers=headers)
                netdiskBonus = response.json()['netdiskBonus']
                if response.json()['isSign'] == "false":
                    log.info(f"天翼云盘:签到成功，获得：{netdiskBonus}M空间")
                    message =  f"天翼云盘:签到成功，获得：{netdiskBonus}M空间"
                else:
                    log.info(f"天翼云盘:已经签到过了，获得：{netdiskBonus}M空间")
                    message =  f"天翼云盘:已经签到过了，获得：{netdiskBonus}M空间"

                # 第一次抽奖
                response = s.get(url, headers=headers).json()
                try:
                    if "errorCode" in response:
                        log.info("天翼云盘:第一次抽奖-没有抽奖次数")
                        message += "\n天翼云盘:第一次抽奖-没有抽奖次数"
                    else:
                        log.info(f"天翼云盘:第一次抽奖获得{response['prizeName']}")
                        message += f"\n天翼云盘:第一次抽奖获得{response['prizeName']}"
                except Exception as er:
                    log.info(f"天翼云盘:第一次抽奖出现了错误:{er}")
                    message += f"\n天翼云盘:第一次抽奖出现了错误:{er}"

                # 第二次抽奖
                response = s.get(url2, headers=headers).json()
                try:
                    if "errorCode" in response:
                        log.info("天翼云盘:第二次抽奖-没有抽奖次数")
                        message += "\n天翼云盘:第二次抽奖-没有抽奖次数"
                    else:
                        log.info(f"天翼云盘:第二次抽奖获得{response['prizeName']}")
                        message += f"\n天翼云盘:第二次抽奖获得{response['prizeName']}"
                except Exception as er:
                    log.info(f"天翼云盘:第二次抽奖出现了错误:{er}")
                    message += f"\n天翼云盘:第二次抽奖出现了错误:{er}"
                return message
            else:
                log.info("天翼云盘:账号或密码不能为空")
                return "天翼云盘:账号或密码不能为空"
        except Exception as er:
            log.info(f"天翼云盘:出现了错误:{er}")
            return f"天翼云盘:出现了错误:{er}"


# 网易云游戏签到
class wyyyx():
    def __init__(self,SignToken) -> None:
        self.wyyyx_cookie = SignToken['wyyyx']['cookie']

    def Sgin(self):
        url='https://n.cg.163.com/api/v2/sign-today'
        header={
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja-JP;q=0.6,ja;q=0.5',
            'Authorization': self.wyyyx_cookie,
            'Connection': 'keep-alive',
            'Content-Length': '0',
            'Host': 'n.cg.163.com',
            'Origin': 'https://cg.163.com',
            'Referer': 'https://cg.163.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            'X-Platform': '0'
        }
        res = requests.post(url=url,headers=header).status_code
        if res == 200:
            log.info("网易云游戏:签到成功")
            return "网易云游戏:签到成功"
        else:
            log.info("网易云游戏:签到失败或已签到")
            return "网易云游戏:签到失败或已签到"
        