// pages/upload/index.js

import { uploadPhoto, downloadProcessedPhoto } from "../../apis/PHOTO_API.js";

const EditingStage = {
    entry: "entry",
    uploading: "uploading",
    uploaded: "uploaded",
    share: "share",
}

const app = getApp();

Page({

    /**
     * 页面的初始数据
     */
    data: {
        stage: EditingStage.entry,
        imgPath: "",
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {

    },

    /**
     * 生命周期函数--监听页面初次渲染完成
     */
    onReady: function () {

    },

    /**
     * 生命周期函数--监听页面显示
     */
    onShow: function () {

    },

    /**
     * 生命周期函数--监听页面隐藏
     */
    onHide: function () {

    },

    /**
     * 生命周期函数--监听页面卸载
     */
    onUnload: function () {

    },

    /**
     * 页面相关事件处理函数--监听用户下拉动作
     */
    onPullDownRefresh: function () {

    },

    /**
     * 页面上拉触底事件的处理函数
     */
    onReachBottom: function () {

    },

    /**
     * 用户点击右上角分享
     */
    onShareAppMessage: function () {
        console.log("share function demo");
        return {
            title: "小程序分享功能演示",
            path: `/pages/index/index`,
        };
    },

    chooseImg() {
        console.log("Enter the function chooseImg");
        let that = this;
        wx.chooseImage({
            count: 1,
            sizeType: ["original", "compressed"],
            sourceType: ["album", "camera"],
            success(res) {
                let imgPath = res.tempFilePaths[0];
                that.uploadPhotoRequest(imgPath);
            },
        });
    },

    uploadPhotoRequest: async function (imgPath) {
        wx.showLoading({
            icon: "loading",
            title: "正在加载中...",
            mask: true,
        });

        console.log("image choosed: ", res);

        let res = await uploadPhoto(imgPath, app.globalData.userToken);
        let data = res.data;
        data = JSON.parse(data);
        console.log("data from uploading", data);

        let img_url = data.image;
        res = await downloadProcessedPhoto(img_url);

        console.log("finish downloaded processed image");
        console.log(res);

        // Send the image to canvas component
        this.setData({
            imgPath: res.tempFilePath,
            stage: EditingStage.uploaded,
        });
        wx.hideLoading();
    },

    // 保存到相册
    saveImg() {
        let imgPath = this.data.imgPath;
        wx.saveImageToPhotosAlbum({
            filePath: imgPath,
            success(res) {
                console.log("save image success! ", res);
                wx.showToast({
                    title: "保存成功",
                });
            },
            fail(err) {
                console.log(err);
                wx.showToast({
                    title: "保存失败",
                });
            },
        });
    },
})