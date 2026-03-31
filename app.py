from flask import Flask, request, jsonify
from flask_cors import CORS
import json, os, time

app = Flask(name)
CORS(app)

DB_FILE = "db.json"

##===== LOAD / SAVE =====#

def load():
if not os.path.exists(DB_FILE):
return {}
try:
return json.load(open(DB_FILE))
except:
return {}

def save(data):
json.dump(data, open(DB_FILE,"w"), indent=2)

db = load()


@app.route("/")
def home():
return "API RUNNING"


@app.route("/user/<uid>")
def get_user(uid):
return jsonify(db.get(uid, {}))

@app.route("/update", methods=["POST"])
def update():
data = request.json

uid = str(data.get("uid"))
user_data = data.get("data")

if not uid or not user_data:
    return jsonify({"status":"error"})

db[uid] = user_data
save(db)

return jsonify({"status":"ok"})


@app.route("/order", methods=["POST"])
def order():
data = request.json

uid = str(data.get("uid"))
service = data.get("service")
link = data.get("link")
qty = int(data.get("quantity"))

if uid not in db:
    return jsonify({"message":"User not found"})

u = db[uid]

PRICE = {
    "tg_members": 120,
    "tg_react": 80,
    "tg_views": 50,
    "ig_follow": 150,
    "ig_like": 60,
    "ig_views": 40
}

price_per_1000 = PRICE.get(service, 100)
cost = int(qty * price_per_1000 / 1000)

if u.get("credits",0) < cost:
    return jsonify({"message":"Not enough coins"})


u["credits"] -= cost
u["orders"] = u.get("orders",0) + 1


u.setdefault("order_history", []).append({
    "service": service,
    "link": link,
    "quantity": qty,
    "status": "Processing",
    "time": int(time.time())
})

u.setdefault("transactions", []).append({
    "type": "DEBIT",
    "amount": cost,
    "currency": "Credits",
    "note": f"{service} order",
    "time": int(time.time())
})

save(db)

return jsonify({"message":f"Order placed (-{cost} coins)"})

===== RUN =====

if name == "main":
app.run(host="0.0.0.0", port=5000)
