import { PHOTO_CREATE } from "./APIURL";

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

module.exports = {
    uploadPhoto: uploadPhoto,
}; 