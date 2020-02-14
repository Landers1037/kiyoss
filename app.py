from flask import Flask,request,render_template,redirect,jsonify
from index import html
import json
import subprocess
import re
import platform
import time


app = Flask(__name__,static_url_path='')

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/ssconf',methods=['GET','POST'])
def ssconf():
    if request.method == 'POST':
        with open('local.json','r',encoding='utf-8')as f:
            data = json.load(f)
            if request.form.get("server"):
                data["server"] = request.form.get("server")
            if request.form.get("port"):
                data["server_port"] = request.form.get("port")
            if request.form.get("local"):
                data["local_address"] = request.form.get("local")
            if request.form.get("localport"):
                data["local_port"] = request.form.get("localport")
            if request.form.get("passwd"):
                data["password"] = request.form.get("passwd")
            if request.form.get("method"):
                data["method"] = request.form.get("method")

        with open('local.json','w',encoding='utf-8') as f:
            f.write(json.dumps(data,indent=4))
            f.close()

        return redirect('/ssconf')
    return redirect('/')
    # return html

@app.route('/start',methods=['GET','POST'])
def start():
    plat = platform.system()

    if plat == 'Windows' or plat == 'WINDOWS':
        if request.form.get("sh")== '0' and request.method == 'POST':
            cmd = 'sslocal -c local.json start'
            try:
                subprocess.run(cmd)#判断是ss启动还是ssr启动
            except Exception as e:
                with open('kiyo.log', 'a', encoding='utf-8')as f:
                    f.write(time.strftime("%Y-%m-%d %H:%M:%S") + '    ' + str(e) + '\n')
                    f.close()

            return redirect('/start')

        elif request.form.get("sh") == '1' and request.method == 'POST':
            #ssr
            cmd = 'sslocal -c local.json start'
            try:
                subprocess.run(cmd)

            except Exception as e:
                with open('kiyo.log', 'a', encoding='utf-8')as f:
                    f.write(time.strftime("%Y-%m-%d %H:%M:%S") + '    ' + str(e) + '\n')
                    f.close()
            return redirect('/start')
        else:
            pass


    elif plat == 'Linux' or plat == 'LINUX':
        if request.form.get("sh") == '0' and request.method == 'POST':
            cmd = 'nohup sslocal -c local.json start &'
            try:
                subprocess.run(cmd)
            except Exception as e:
                with open('kiyo.log', 'a', encoding='utf-8')as f:
                    f.write(time.strftime("%Y-%m-%d %H:%M:%S") + '    ' + str(e) + '\n')
                    f.close()
            return redirect('/start')

        elif request.form.get("sh") == '1' and request.method == 'POST':
            #ssr
            cmd = 'sslocal -c local.json start'
            try:
                subprocess.run(cmd)

            except Exception as e:
                with open('kiyo.log', 'a', encoding='utf-8')as f:
                    f.write(time.strftime("%Y-%m-%d %H:%M:%S") + '    ' + str(e) + '\n')
                    f.close()

            return redirect('/start')

    return redirect('/')

@app.route('/stop',methods=['POST'])
def stop():
    plat = platform.system()

    if plat == 'Windows' or plat == 'WINDOWS':
        try:
            pid = str(subprocess.getoutput('netstat -ano|findstr "2333"'))
            pid = re.search('LISTENING(.*)',pid).group(1).strip()

            cmd = 'taskkill /f /im "sslocal.exe"'
            cmd1 = 'taskkill /f /pid '+ pid
            subprocess.run(cmd)
            subprocess.run(cmd1)
        except Exception as e:
            with open('kiyo.log','a',encoding='utf-8')as f:
                f.write(time.strftime("%Y-%m-%d %H:%M:%S")+'    '+str(e)+'\n')
                f.close()


    elif plat == 'Linux' or plat == 'LINUX':
        subprocess.run('sslocal -c local.json stop')

    return redirect('')

def default(req,de):
    if not req:
        return de
    else:
        return req

@app.route('/ssr')
def gossr():

    return render_template('index_ssr.html')


@app.route('/ssrconf',methods=['GET','POST'])
def gossr_conf():
    if request.method == 'POST':
        try:
            with open('ssr.json','w',encoding='utf-8')as f:
                conf = {}

                conf["server"] = default(request.form.get("server"), '0.0.0.0')
                conf["server_ipv6"] = default(request.form.get("server_ipv6"), '::')
                conf["server_port"] = default(request.form.get("server_port"), 8080)
                conf["local_address"] = '127.0.0.1'
                conf["local_port"] = default(request.form.get("local_port"), 2333)
                conf["password"] = request.form.get("password")
                conf["method"] = default(request.form.get("method"), 'rc4-md5-6')
                conf["protocol"] = default(request.form.get("protocol"), 'auth_aes128_md5')
                conf["protocol_param"] = default(request.form.get("protocol_param"), '')
                conf["obfs"] = default(request.form.get("obfs"), "plain")
                conf["obfs_param"] = default(request.form.get("obfs_param"), '')
                conf["speed_limit_per_con"] = default(request.form.get("speed_limit_per_con"), 0)
                conf["speed_limit_per_user"] = default(request.form.get("speed_limit_per_user"), 0)
                conf["additional_ports"] = {}
                conf["timeout"] = default(request.form.get("timeout"), 120)
                conf["udp_timeout"] = default(request.form.get("udp_timeout"), 60)
                conf["dns_ipv6"] = default(request.form.get("dns_ipv6"), False)
                conf["connect_verbose_info"] = 0
                conf["redirect"] = ""
                conf["fast_open"] = False
                conf["udp_cache"] = default(request.form.get("udp_cache"), 64)

                f.write(json.dumps(conf,indent=4))

        except Exception as e:
            print(e.args)
            pass
        return redirect('/ssrconf')
    return redirect('/ssr')

@app.route('/help')
def help():

    return render_template('help.html')