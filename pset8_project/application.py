import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import random
import string


from helpers import apology, login_required, lookup, usd



# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    portfolios = []
    cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])[0]['cash']
    balance = cash
    stocks = db.execute("SELECT DISTINCT(symbol) FROM trades WHERE userid = :user_id",
                          user_id=session["user_id"])
    stocks = [d['symbol'] for d in stocks]
    initialcap = db.execute("SELECT initialcap FROM users WHERE id = :user_id", user_id=session["user_id"])[0]['initialcap']
    for stock in stocks:
        symbol = stock
        name = lookup(stock)['name']
        price = lookup(stock)['price']
        shares = db.execute("SELECT SUM(numofshare) FROM trades WHERE symbol=:symbol AND userid = :user_id", symbol = symbol, user_id=session["user_id"])[0]['SUM(numofshare)']
        total = round(shares * price, 2)
        startprice = db.execute("SELECT SUM(numofshare*price) FROM trades WHERE symbol=:symbol AND userid = :user_id", symbol = symbol, user_id=session["user_id"])[0]['SUM(numofshare*price)']
        if startprice == 0:
            ret = 0;
            retpct = 0
        else:
            ret = total - startprice
            retpct = 100*(total/startprice - 1)
        balance = balance + total
        item = [symbol, name, usd(price), shares, total, usd(total), usd(ret), round(retpct, 2)]
        if item[3] != 0:
            portfolios.append(item)

    balanceret = balance - initialcap
    balanceretpct = 100*(balance/initialcap - 1)
    labels = [portfolio[0] for portfolio in portfolios]
    labels.append('Cash')
    values = [(100*portfolio[4]/balance) for portfolio in portfolios]
    values.append(100*cash/balance)
    numofcolor = len(labels)
    colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(numofcolor)]
    pie_labels = labels
    pie_values = values

    return render_template("index.html", portfolios=portfolios, cash = usd(cash), balance = usd(balance), balanceret = usd(balanceret), balanceretpct = round(balanceretpct, 2), title='Portfolio Diversity', set=zip(values, labels, colors))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    index()
    if request.method == "GET":
        return render_template("buy.html")

    else:
        buy = lookup(request.form.get("buy"))

        if not buy:
            return apology("You must enter a valid symbol.")

        balance = db.execute("SELECT * FROM users WHERE id = :user_id",
                          user_id=session["user_id"])[0]["cash"]
        buy_amount = buy["price"] * float(request.form.get("shares"))
        if balance < buy_amount:
            return apology("You do not have sufficient balance.")

        db.execute("INSERT INTO trades (userid, trade, symbol, company, price, numofshare) VALUES (:userid, :trade, :symbol, :company, :price, :numofshare)", userid = session["user_id"], trade="BUY",
symbol=buy["symbol"], company=buy["name"], price=buy["price"], numofshare=float(request.form.get("shares")))

        new_balance = balance - buy_amount
        db.execute("UPDATE users SET cash = :new_balance WHERE id=:user_id", new_balance=new_balance, user_id=session["user_id"])

        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    portfolios = []
    stocks = db.execute("SELECT * FROM trades WHERE userid = :user_id",
                          user_id=session["user_id"])

    for stock in stocks:
        symbol = stock['symbol']
        shares = stock['numofshare']
        price = stock['price']
        transacted = stock['created_at']
        transaction = [symbol, shares, price, transacted]
        portfolios.append(transaction)

    return render_template("history.html", portfolios=portfolios)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("/quote.html")

    else:
        quote = lookup(request.form.get("quote"))

        if not quote:
            return apology("Please provide a valid symbol.")

        return render_template("/price.html", name=quote["name"], symbol=quote["symbol"], price=quote["price"])



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("/register.html")

    else:
        username = request.form.get("username")
        if not username:
            return apology("You must provide a valid username", 403)

        password = request.form.get("password")
        if not password:
            return apology("You must provide a valid password", 403)

        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username = username, hash = generate_password_hash(password))
        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        stocks = db.execute("SELECT symbol, SUM(numofshare)  FROM trades WHERE userid = :user_id GROUP BY symbol HAVING SUM(numofshare) > 0", user_id=session["user_id"])
        stocks = [d['symbol'] for d in stocks]

        return render_template("sell.html", stocks = stocks)

    else:
        sell = lookup(request.form.get("sell"))

        if not sell:
            return apology("You must select from your current portfolio.")

        balance = db.execute("SELECT * FROM users WHERE id = :user_id",
                          user_id=session["user_id"])[0]["cash"]
        sell_amount = float(request.form.get("shares"))
        share_avil = db.execute("SELECT SUM(numofshare) FROM trades WHERE userid = :userid AND symbol = :symbol", symbol = sell["symbol"],
                          userid=session["user_id"])[0]["SUM(numofshare)"]
        if share_avil < sell_amount:
            return apology("You do not have enough shares.")

        db.execute("INSERT INTO trades (userid, trade, symbol, company, price, numofshare) VALUES (:userid, :trade, :symbol, :company, :price, :numofshare)", userid = session["user_id"], trade="SELL",
symbol=sell["symbol"], company=sell["name"], price=sell["price"], numofshare=-float(request.form.get("shares")))

        new_balance = balance + sell_amount*sell["price"]
        db.execute("UPDATE users SET cash = :new_balance WHERE id=:user_id", new_balance=new_balance, user_id=session["user_id"])

        return redirect("/")



@app.route("/setting", methods=["GET", "POST"])
@login_required
def setting():
    username = db.execute("SELECT username FROM users WHERE id = :user_id", user_id = session["user_id"])[0]['username']
    cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id = session["user_id"])[0]['cash']
    cash = round(cash, 2)

    if request.method == "GET":
        return render_template("/setting.html", username = username, cash = usd(cash))

    else:
        password = request.form.get("password")
        topup = request.form.get("topup")
        withdraw = request.form.get("withdraw")
        email = request.form.get("email")

        if email != "":
            db.execute("UPDATE users SET email = :email WHERE id = :user_id", user_id = session["user_id"], email = email)
            return render_template("/setting.html", user_id = session["user_id"], username = username, cash = usd(cash), success = "Success!")
        elif password != "":
            db.execute("UPDATE users SET hash = :hash WHERE id = :user_id", user_id = session["user_id"], hash = generate_password_hash(password))
            return render_template("/setting.html", user_id = session["user_id"], username = username, cash = usd(cash), success = "Success!")
        elif password == "" and int(topup) > 0:
            db.execute("UPDATE users SET cash = cash + :topup WHERE id = :user_id", user_id = session["user_id"], topup = int(topup))
            db.execute("UPDATE users SET initialcap = initialcap + :topup WHERE id = :user_id", user_id = session["user_id"], topup = int(topup))
            return render_template("/setting.html", username = username, cash = usd(cash + int(topup)), success = "Success!")
        elif password == "" and int(withdraw) > 0:
            db.execute("UPDATE users SET cash = cash - :withdraw WHERE id = :user_id", user_id = session["user_id"], withdraw = int(withdraw))
            db.execute("UPDATE users SET initialcap = initialcap - :withdraw WHERE id = :user_id", user_id = session["user_id"], withdraw = int(withdraw))
            return render_template("/setting.html", username = username, cash = usd(cash - int(withdraw)), success = "Success!")
        else:
            return apology("Error")





@app.route("/help", methods=["GET", "POST"])
@login_required
def help():
    if request.method == "GET":
        return render_template("/help.html")

    else:
        name = request.form.get("name")
        phone = request.form.get("phone")
        help = request.form.get("help")
        db.execute("INSERT INTO helps (userid, name, help, phone) VALUES (:userid, :name, :help, :phone)", userid = session["user_id"], name = name, help = help, phone = phone)
        return render_template("/help.html", success = "Success! Thanks for contacting us.")





@app.route("/message", methods=["GET", "POST"])
@login_required
def message():
    if request.method == "GET":
        users = db.execute("SELECT username FROM users WHERE id in (SELECT senderid FROM messages WHERE senderid=:user_id OR receiverid=:user_id) OR id in (SELECT receiverid FROM messages WHERE senderid=:user_id OR receiverid=:user_id)", user_id=session["user_id"])
        users = [d['username'] for d in users]

        return render_template("/message.html", users = users)

    else:
        if request.form.get("chat") == "Please select ...":
            receiver = request.form.get("receiver")
            receivers = db.execute("SELECT username FROM users")
            if receiver not in (r['username'] for r in receivers) :
                return apology("Can't Find User")
            else:
                user = request.form.get("receiver")
        else:
            user = request.form.get("chat")

        messages = []
        receiverid = db.execute("SELECT id FROM users WHERE username = :username", username = user)[0]['id']
        senderid = session["user_id"]
        records = db.execute("SELECT * FROM messages WHERE (senderid = :senderid AND receiverid = :receiverid) OR (senderid = :receiverid AND receiverid  = :senderid)", senderid = senderid, receiverid = receiverid)
        for record in records:
            sender = record['senderid']
            sender = db.execute("SELECT username FROM users WHERE id=:user_id", user_id=sender)[0]['username']
            msg = record['message']
            time = record['created_at']
            record = [sender, msg, time]
            messages.append(record)


        return render_template("/chatbox.html", user=user, messages = messages)



@app.route("/chatbox", methods=["GET", "POST"])
@login_required
def chatbox():
    if request.method == "POST":

        messages = []

        receiver = request.form.get("receiver")

        receiverid = db.execute("SELECT id FROM users WHERE username = :username", username = receiver)[0]['id']
        senderid = session["user_id"]
        message = request.form.get("message")
        submit1 = request.form.get("submit1")

        db.execute("INSERT INTO messages (senderid, receiverid, message) VALUES (:senderid, :receiverid, :message)", senderid = senderid, receiverid = receiverid, message = message)

        records = db.execute("SELECT * FROM messages WHERE (senderid = :senderid AND receiverid = :receiverid) OR (senderid = :receiverid AND receiverid  = :senderid)", senderid = senderid, receiverid = receiverid)

        for record in records:
            sender = record['senderid']
            sender = db.execute("SELECT username FROM users WHERE id=:user_id", user_id=sender)[0]['username']
            msg = record['message']
            time = record['created_at']
            record = [sender, msg, time]
            messages.append(record)

        if message == "" and submit1 == "Clear All Chat":
            db.execute("DELETE FROM messages WHERE (senderid = :senderid AND receiverid = :receiverid) OR (senderid = :receiverid AND receiverid  = :senderid)", senderid = senderid, receiverid = receiverid)
            return render_template("/chatbox.html", user = receiver)
        else:
            return render_template("/chatbox.html", user = receiver, messages = messages)



@app.route("/price", methods=["GET", "POST"])
@login_required
def price():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if "buy" in request.form:
            return render_template("/buy.html", symbol = symbol)
        elif "sell" in request.form:
            stocks = db.execute("SELECT symbol, SUM(numofshare)  FROM trades WHERE userid = :user_id GROUP BY symbol HAVING SUM(numofshare) > 0", user_id=session["user_id"])
            stocks = [d['symbol'] for d in stocks]
            if symbol in stocks:
                return render_template("/sell.html", symbol = symbol)
            else:
                return apology("Selection not in your portfolio")
        else:
            return apology("Please try again")




@app.route("/reactivate", methods=["GET", "POST"])
def reactivate():

    if request.method == "GET":
        return render_template("/reactivate.html")

    else:
        username_input = request.form.get("username")
        username_rec = db.execute("SELECT username FROM users")
        username_rec = [user['username'] for user in username_rec]
        userid = db.execute("SELECT id FROM users WHERE username = :username", username = username_input)[0]['id']

        email_input = request.form.get("email")
        email_rec = db.execute("SELECT email FROM users")
        email_rec = [email['email'] for email in email_rec]
        emailid = db.execute("SELECT id FROM users WHERE email = :email", email = email_input)[0]['id']



        if (username_input in username_rec)  and (email_input in email_rec) and (emailid == userid):
            letters_and_digits = string.ascii_letters + string.digits
            password = ''.join((random.choice(letters_and_digits) for i in range(9)))
            password = password[1:]
            db.execute("UPDATE users SET hash= :hash WHERE id = :userid", hash = generate_password_hash(password), userid = userid)
            return render_template("/login.html", popup_window=True, password = password)
        else:
            return apology("Please Try Again")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
