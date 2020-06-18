import { SERVER_DOMAIN, PHOTO_CREATE } from "./APIURL";

function uploadPhoto(imgPath, token = null) {
    return new Promise((resolve, reject) => {
        wx.uploadFile({
            url: PHOTO_CREATE,
            filePath: imgPath,
            name: "image",
            header: {
                "Content-Type": "multipart/form-data",
                Authorization: "Token " + token,
            },
            formData: {},
            success: function (res) {
                resolve(res);
            },
            fail: function (error) {
                console.log("error in uploadFile: ", error);
                wx.showToast({
                    title: "出问题啦！！",
                    icon: "loading",
                    duration: 2000,
                });
            },
        });
    });
}

function downloadProcessedPhoto(img_url) {
    // append domain to the url
    // example: /media/uploads/3/photo/image_VRZdAQn.png
    // to: http://localhost:8000/media/uploads/3/photo/image_VRZdAQn.png
    img_url = "http://localhost:8000" + img_url;
    return new Promise((resolve, reject) => {
        wx.downloadFile({
            url: img_url,
            success(res) {
                console.log("downloadFile", res);
                // 只要服务器有响应数据，就会把响应内容写入文件并进入 success 回调，业务需要自行判断是否下载到了想要的内容
                resolve(res);
            },
            fail(res) {
                wx.showToast({
                    title: "出问题啦！！",
                    icon: "loading",
                    duration: 2000,
                });
                console.log("error in downloadFile", res);
            },
        });
    });
}


module.exports = {
    uploadPhoto: uploadPhoto,
    downloadProcessedPhoto: downloadProcessedPhoto,
}; 