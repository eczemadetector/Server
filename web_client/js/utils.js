function httpPostAsync(url, json, callback) {
    var xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200)
            callback(xhr.responseText)
    }
    xhr.open("POST", url, true) 
    xhr.setRequestHeader('Content-Type', 'application/json')
    xhr.send(JSON.stringify(json))
}

function removeCookies() {
    var res = document.cookie.split(';')
    for (var i = 0; i < res.length; i++) {
       var key = res[i].split('=')
       document.cookie = key[0] + ' =; expires = Thu, 01 Jan 1970 00:00:00 UTC'
    }
}