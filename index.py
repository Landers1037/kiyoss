html = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>Kiyo</title>
    <link rel="stylesheet" href="https://cdn.staticfile.org/twitter-bootstrap/4.3.1/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdn.staticfile.org/font-awesome/5.10.2/css/all.min.css">
    <script src="https://cdn.staticfile.org/jquery/3.4.1/jquery.min.js"></script>
</head>
<style>
    .main{text-align: center;padding: 30px 0;}
    h3{color: #808080}
    .main .sec{width: 80%;margin: 0 auto;background-color: #f5f5f5;padding: 30px 0;margin-top: 30px;border-radius: 10px;text-align: left}
    form{padding: 0 30px;text-align: left}
    form span{color: #404040;display: inline-block;width: 120px}
    form input{width: 50% !important;display: inline!important;margin-bottom: 6px}
    form button{margin-right: 10px}
    .btn-group{padding: 30px 30px;}
    .btn-group button{margin-right: 10px}
</style>
<body>
    <div class="main">
        <h3>Kiyo 配置页面</h3>
        <div class="sec">
        <form method="post">
            <span>服务器地址</span><input type="text" autocomplete="off" class="form-control" name="server" placeholder="服务器ip"><br>
            <span>服务器端口</span><input type="text" autocomplete="off" class="form-control" name="port" placeholder="服务器port"><br>
            <span>本地监听地址</span><input type="text" autocomplete="off" class="form-control" name="local" placeholder="127.0.0.1"><br>
            <span>本地监听端口</span><input type="text" autocomplete="off" class="form-control" name="localport" placeholder="默认2333"><br>
            <span>代理密码</span><input type="text" autocomplete="off" class="form-control" name="passwd" placeholder="password"><br>
            <span>加密方式</span><input type="text" list="method" class="form-control" name="method" placeholder="默认aes-256-cfb">
            <datalist id="method">
                <option value="none"></option>
                <option value="rc4-md5"></option>
                <option value="aes-128-cfb"></option>
                <option value="aes-192-cfb"></option>
                <option value="aes-256-cfb"></option>
                <option value="chacha20"></option>
            </datalist>
            <br>
            <span>Fast open</span><input type="text" autocomplete="off" class="form-control" name="fastopen" placeholder="默认关闭"><br>
            <br>
            <span>通过ssr链接导入</span><input type="text" autocomplete="off" class="form-control" name="ssrlink" placeholder="ssr://"><br>
        </form>
            <div class="btn-group">
            <button type="submit" id="save" class="btn-primary">保存配置</button>
            <button id="start" class="btn-success" onclick="start()">启动服务</button>
            <button id="stop" class="btn-info" onclick="stop()">停止服务</button>
            <button id="check" class="btn-danger" onclick="window.location.href='/all'">查看全部</button>
            </div>

        </div>
    </div>

<script>
    $("#save").click(function () {
        var form = $("form");
        form.submit();
        alert('文件配置已经更新');

    });

    function start() {
        var cmd = 'cc';
        alert('服务开启，如遇错误请查看日志');
        $.ajax({
            url:'/start',
            data:cmd,
            type:'post',
            processData: false,
            contentType: false,
            success: function () {
                alert('服务开启，你可以关闭该页面');
            }

        });

    }
    function stop() {
        $.ajax({
            url:'/stop',
            type:'post',
            processData: false,
            contentType: false,
            success: function () {
                alert('服务关闭，你可以关闭该页面');
            }

        });

    }

</script>
</body>
</html>

'''