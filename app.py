from flask import Flask, request, render_template_string
import json
import random
import string
from pathlib import Path

app = Flask(__name__)

DATABASE = "data.json"

if Path(DATABASE).exists():
    with open(DATABASE) as f:
        data = json.load(f)
else:
    data = []

def update():
    with open(DATABASE, "w") as f:
        json.dump(data, f)

def account_generate():
    alpha = random.choices(string.ascii_uppercase, k=3)
    num = random.choices(string.digits, k=4)
    acc = alpha + num
    random.shuffle(acc)
    return "".join(acc)

# 🔥 MASTER UI TEMPLATE
def page(title, content):
    return render_template_string(f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title>{title}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            margin:0;
            font-family: 'Segoe UI', sans-serif;
            background: radial-gradient(circle at top,#1f1c2c,#928dab);
            display:flex;
            justify-content:center;
            align-items:center;
            height:100vh;
            color:white;
        }}

        .card {{
            width:400px;
            padding:30px;
            border-radius:20px;
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(15px);
            box-shadow: 0 0 40px rgba(0,0,0,0.6);
            text-align:center;
            animation: fadeIn 0.6s ease-in-out;
        }}

        @keyframes fadeIn {{
            from {{opacity:0; transform:translateY(20px);}}
            to {{opacity:1; transform:translateY(0);}}
        }}

        h1 {{
            margin-bottom:20px;
        }}

        input {{
            width:100%;
            padding:12px;
            margin:10px 0;
            border:none;
            border-radius:10px;
            outline:none;
            font-size:14px;
        }}

        button {{
            width:100%;
            padding:12px;
            border:none;
            border-radius:10px;
            font-weight:bold;
            cursor:pointer;
            background: linear-gradient(45deg,#ff416c,#ff4b2b);
            color:white;
            transition:0.3s;
        }}

        button:hover {{
            transform:scale(1.05);
            box-shadow:0 0 20px #ff4b2b;
        }}

        .link-btn {{
            display:block;
            margin:10px 0;
            padding:12px;
            border-radius:10px;
            background: linear-gradient(45deg,#00c6ff,#0072ff);
            text-decoration:none;
            color:white;
            font-weight:bold;
            transition:0.3s;
        }}

        .link-btn:hover {{
            transform:scale(1.05);
            box-shadow:0 0 20px #00c6ff;
        }}

        .back {{
            margin-top:15px;
            display:inline-block;
            color:#ffd369;
            text-decoration:none;
        }}

    </style>
    </head>
    <body>
        <div class="card">
            <h1>🏦 Bhaukali Bank</h1>
            {content}
        </div>
    </body>
    </html>
    """)

# 🏠 HOME
@app.route('/')
def home():
    return page("Home", """
        <a class="link-btn" href='/create'>🚀 Create Account</a>
        <a class="link-btn" href='/deposit'>💰 Deposit</a>
        <a class="link-btn" href='/withdraw'>💸 Withdraw</a>
        <a class="link-btn" href='/details'>📄 Account Details</a>
    """)

# 🆕 CREATE
@app.route('/create', methods=["GET","POST"])
def create():
    if request.method == "POST":
        info = {
            "name": request.form["name"],
            "age": int(request.form["age"]),
            "email": request.form["email"],
            "pin": int(request.form["pin"]),
            "accountNo.": account_generate(),
            "balance": 0
        }

        if info["age"] < 18 or len(str(info["pin"])) != 4:
            return page("Error","❌ Invalid Age or PIN<br><a class='back' href='/'>Go Back</a>")

        data.append(info)
        update()

        return page("Success", f"""
            ✅ Account Created<br><br>
            <b>Account No:</b> {info['accountNo.']}<br><br>
            <a class='back' href='/'>Go Home</a>
        """)

    return page("Create Account", """
        <form method="POST">
            <input name="name" placeholder="Full Name">
            <input name="age" placeholder="Age">
            <input name="email" placeholder="Email">
            <input name="pin" placeholder="4 Digit PIN">
            <button>Create Account</button>
        </form>
        <a class='back' href='/'>⬅ Back</a>
    """)

# 💰 DEPOSIT
@app.route('/deposit', methods=["GET","POST"])
def deposit():
    if request.method == "POST":
        acc = request.form["account"]
        pin = int(request.form["pin"])
        amount = int(request.form["amount"])

        user = next((i for i in data if i["accountNo."]==acc and i["pin"]==pin), None)

        if not user:
            return page("Error","❌ User Not Found<br><a class='back' href='/'>Go Back</a>")

        user["balance"] += amount
        update()

        return page("Success","💰 Deposit Successful<br><a class='back' href='/'>Go Home</a>")

    return page("Deposit", """
        <form method="POST">
            <input name="account" placeholder="Account Number">
            <input name="pin" placeholder="PIN">
            <input name="amount" placeholder="Amount">
            <button>Deposit</button>
        </form>
        <a class='back' href='/'>⬅ Back</a>
    """)

# 💸 WITHDRAW
@app.route('/withdraw', methods=["GET","POST"])
def withdraw():
    if request.method == "POST":
        acc = request.form["account"]
        pin = int(request.form["pin"])
        amount = int(request.form["amount"])

        user = next((i for i in data if i["accountNo."]==acc and i["pin"]==pin), None)

        if not user:
            return page("Error","❌ User Not Found<br><a class='back' href='/'>Go Back</a>")

        if user["balance"] < amount:
            return page("Error","❌ Insufficient Balance<br><a class='back' href='/'>Go Back</a>")

        user["balance"] -= amount
        update()

        return page("Success","💸 Withdraw Successful<br><a class='back' href='/'>Go Home</a>")

    return page("Withdraw", """
        <form method="POST">
            <input name="account" placeholder="Account Number">
            <input name="pin" placeholder="PIN">
            <input name="amount" placeholder="Amount">
            <button>Withdraw</button>
        </form>
        <a class='back' href='/'>⬅ Back</a>
    """)

# 📄 DETAILS
@app.route('/details', methods=["GET","POST"])
def details():
    if request.method == "POST":
        acc = request.form["account"]
        pin = int(request.form["pin"])

        user = next((i for i in data if i["accountNo."]==acc and i["pin"]==pin), None)

        if not user:
            return page("Error","❌ User Not Found<br><a class='back' href='/'>Go Back</a>")

        return page("Details", f"""
            👤 <b>Name:</b> {user['name']}<br><br>
            📧 <b>Email:</b> {user['email']}<br><br>
            💰 <b>Balance:</b> ₹ {user['balance']}<br><br>
            <a class='back' href='/'>⬅ Home</a>
        """)

    return page("Account Details", """
        <form method="POST">
            <input name="account" placeholder="Account Number">
            <input name="pin" placeholder="PIN">
            <button>Check Details</button>
        </form>
        <a class='back' href='/'>⬅ Back</a>
    """)

if __name__ == "__main__":
    app.run(debug=True)