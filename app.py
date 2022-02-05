from flask import Flask, render_template, request
from scanner import Scanner

app = Flask(__name__)


@app.route('/')
@app.route('/home/')
def home():  # put application's code here
    return render_template('home.html')


@app.route('/search/')
def search():
    target = request.args.get('target')
    mode = request.args.get('mode')
    mode = int(mode)
    custom_ports = request.args.get('custom_ports')
    scanner = Scanner(target=target)
    open_ports = scanner.run(mode, custom_ports)
    return render_template('snanner.html', open_ports=open_ports)


if __name__ == '__main__':
    app.run()
