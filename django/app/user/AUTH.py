import json
import requests
from . import CONSTANTS as c


def getOpenIDFromWechat(js_code):
    openid_url = 'https://api.weixin.qq.com/sns/jscode2session?' + \
        'grant_type=authorization_code' + \
        '&appid=' + c.WX_APP_ID + \
        '&secret=' + c.WX_APP_SECRET + \
        '&js_code=' + js_code
    k = requests.get(openid_url).content.decode('utf-8')
    res = json.loads(k)
    print("fetched openid from jscode: ", res)
    return res['openid']