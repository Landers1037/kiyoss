#! /usr/bin/python3
'''
kiyo归属于Mgek开源项目，是一个命令行ss/ssr工具
可以帮助你快速搭建本地的代理服务，或者连接代理服务器
有关kiyo的详细信息可以查看 http://kiyo.mgek.cc
使用文档请查看 http://mgek.cc/kiyo.md
'''
import click
from app import app
import platform
import time,json
import subprocess

from shadowsocks.common import to_bytes, to_str
from shadowsocks.shell import parse_json_in_str, remove_comment


@click.group()
def kiyo():
    pass

@click.command(help='版本号')
def version():
    click.echo('kiyo version 1.0.1')
    subprocess.run('ssserver --version')

@click.command(help='kiyo介绍')
def info():
    click.echo('这是测试版的pysock服务，属于Mgek项目\n它的功能是为使用者创建可靠的socke代理，让你可以浏览Google，Wikipidia等\n'
               'kiyo是对shadowxxr的高级封装的本地web客户端，在linux平台更好地使用代理服务，基于Ubuntu18.04构建测试通过\n'
               '使用命令--help      查看全部命令\n'
               '使用命令kiyo web    激活webui界面\n'
               '使用命令kiyo ss     激活ss代理服务\n'
               '使用命令kiyo ssr    激活ssr代理服务\n'
               '使用命令kiyo server 开启server模式\n'
               '更多使用参考项目文档http://mgek.cc/kiyo.md')

@click.command(help='启动web服务')
@click.option('--open',is_flag=True,help='允许外网访问')
@click.option('--port',default=5000,help='默认web端口设置')
def web(port,open):
    click.echo('你正在允许web服务，打开浏览器访问以下网址即可进入设置')
    if open:
        app.run(host='0.0.0.0')
    else:
        app.run(port=port)

@click.command(help='连接ss代理')
@click.option('-d',is_flag=True,help='允许后台运行')
def ss(d):
    plat = platform.system()
    if d:
        if plat == 'Windows' or plat == 'WINDOWS':
            click.echo('windows不支持设置后台运行，请保持该程序运行')
        elif plat == 'Linux' or plat == 'LINUX':
            click.echo('后台运行客户端')
            subprocess.run('nohup sslocal -c local.json -d start &')

    else:
        click.echo('启动ss客户端')
        subprocess.run('sslocal -c local.json start')

@click.command(help='搭建代理服务')
@click.option('-d',is_flag=True,help='允许后台运行')
def server(d):
    plat = platform.system()
    if d:
        if plat == 'Windows' or plat == 'WINDOWS':
            click.echo('windows不支持后台运行')
        elif plat == 'Linux' or plat == 'LINUX':
            click.echo('后台运行服务端')
            subprocess.run('nohup ssserver -c server.json -d start &')
    else:
        click.echo('启动ss服务')
        subprocess.run('ssserver -c server.json')

@click.command(help='本地ssr代理')
@click.option('--run',help='指定配置文件地址')
def ssr(run):
    config = {}
    from shadowsocks import local
    if run:
        file_path = run
    else:
        file_path = 'ssr.json'
    with open(file_path, 'rb') as f:
        try:
            config = parse_json_in_str(remove_comment(f.read().decode('utf8')))
            config['password'] = to_bytes(config.get('password', b''))
            config['method'] = to_str(config.get('method', 'aes-256-cfb'))
            config['protocol'] = to_str(config.get('protocol', 'origin'))
            config['protocol_param'] = to_str(config.get('protocol_param', ''))
            config['obfs'] = to_str(config.get('obfs', 'plain'))
            config['obfs_param'] = to_str(config.get('obfs_param', ''))
            config['port_password'] = config.get('port_password', None)
            config['additional_ports'] = config.get('additional_ports', {})
            config['additional_ports_only'] = config.get('additional_ports_only', False)
            config['timeout'] = int(config.get('timeout', 300))
            config['udp_timeout'] = int(config.get('udp_timeout', 120))
            config['udp_cache'] = int(config.get('udp_cache', 64))
            config['fast_open'] = config.get('fast_open', False)
            config['workers'] = config.get('workers', 1)
            config['pid-file'] = config.get('pid-file', '/var/run/shadowsocksr.pid')
            config['log-file'] = config.get('log-file', '/var/log/shadowsocksr.log')
            config['verbose'] = config.get('verbose', False)
            config['connect_verbose_info'] = config.get('connect_verbose_info', 0)
            config['local_address'] = to_str(config.get('local_address', '127.0.0.1'))
            config['local_port'] = config.get('local_port', 1080)

        except Exception as e:
            with open('kiyo.log', 'a', encoding='utf-8')as f:
                f.write(time.strftime("%Y-%m-%d %H:%M:%S") + '    ' + str(e) + '\n')
                f.close()

    local.main(config=config)

@click.command(help='停止服务，仅适用于linux')
def stop():
    subprocess.getoutput('pgrep kiyo | xargs kill -s 9')

@click.command(help='无聊的彩蛋')
def cd():
    click.echo('一个水b的交友账号')
    for i in 'https://github.com/landers1037':
        click.echo(i,nl=False)
        time.sleep(0.2)
    click.echo('\n个人网站')
    for i in 'http://lrenj.top':
        click.echo(i,nl=False)
        time.sleep(0.2)
    click.echo('\n')
    click.echo('感谢关注!!!')


kiyo.add_command(info)
kiyo.add_command(web)
kiyo.add_command(ss)
kiyo.add_command(ssr)
kiyo.add_command(stop)
kiyo.add_command(server)
kiyo.add_command(version)
kiyo.add_command(cd)

if __name__ == '__main__':

   kiyo()
