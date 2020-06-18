function request(url, method, data, token = null, header = null) {
    method = method || "GET";
    console.log("ajax.request");
    console.log(method);
    data = data || {};
    if (!header) {
        header = {
            "Content-Type": "application/json",
        };
    }
    if (token) {
        header["Authorization"] = "Token " + token;
    }
    console.log(url, token);
    return new Promise((resolve, reject) => {
        wx.request({
            url: url,
            method: method,
            data: data,
            header: header,
            timeout: 30000,
            success(res) {
                resolve(res.data);
            },
            fail(err) {
                console.log("ajax error: ", err);
                reject(err);
            },
        });
    });
}

module.exports = {
    request: request,
};