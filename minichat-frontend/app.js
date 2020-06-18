//app.js
import { loginAndGetToken } from "apis/USER_API.js";

App({
  onLaunch: function () {
    wx.showLoading({
        icon: "loading",
        title: "正在加载中...",
        mask: true,
    });

    // 先查缓存看有没有存在token
    let user_token = wx.getStorageSync("userToken");
    if (user_token) {
      console.log("this user has token in cache", user_token);
      this.globalData.userToken = user_token;
      wx.hideLoading();
      return;
    }

    // 登录
    loginAndGetToken().then((res) => {
      console.log("finish function loginAndGetToken()");
      console.log(res);
      this.globalData.userToken = res.token;
      console.log(this.globalData);
      wx.setStorageSync("userToken", res.token);
    });
    wx.hideLoading();
  },
  globalData: {
    userToken: null,
  }
})