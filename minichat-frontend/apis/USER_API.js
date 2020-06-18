import { USER_TOKEN } from "./APIURL";
const ajax = require("ajax.js");

// Fetch user token from server side API
function getUserToken(js_code) {
    return ajax.request(USER_TOKEN, "POST", {
        login_id: js_code,
        login_type: "WECHAT",
    });
}

function loginAndGetToken() {
    return new Promise((resolve, reject) => {
        wx.login({
            success: (res) => {
                // 发送 res.code 到后台换取 openId, sessionKey, unionId
                getUserToken(res.code)
                    .then((res) => {
                        resolve(res);
                    })
                    .catch((error) => {
                        console.log("getUserToken", error);
                    });
            },
        });
    });
}

module.exports = {
    loginAndGetToken: loginAndGetToken,
};