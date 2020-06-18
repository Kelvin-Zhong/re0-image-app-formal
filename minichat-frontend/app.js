//app.js
import { loginAndGetToken } from "apis/USER_API.js";

App({
  onLaunch: function () {
    // 登录
    loginAndGetToken().then((res) => {
      console.log("finish function loginAndGetToken()");
      console.log(res);
      this.globalData.userToken = res.token;
      console.log(this.globalData);
    });
  },
  globalData: {
    userToken: null,
  }
})