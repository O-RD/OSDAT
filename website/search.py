from flask import render_template,Blueprint

auth = Blueprint("auth",__name__)

@auth.route('/BTC')
def btc():
    return render_template("btc.html")
