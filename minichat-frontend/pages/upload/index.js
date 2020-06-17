// pages/upload/index.js
const EditingStage = {
    entry: "entry",
    uploading: "uploading",
    uploaded: "uploaded",
    share: "share",
}

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
                console.log("image choosed: ", res);
                that.setData({
                    imgPath: res.tempFilePaths[0],
                    stage: EditingStage.uploaded,
                });
            },
        });
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