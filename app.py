from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_FILE = "db.json"

def load():
    if not os.path.exists(DB_FILE):
        return {}
    return json.load(open(DB_FILE))

def save(data):
    json.dump(data, open(DB_FILE,"w"))

db = load()

# ✅ FIX (ये missing था)
@app.route("/")
def home():
    return "API RUNNING"

@app.route("/user/<uid>")
def get_user(uid):
    return jsonify(db.get(uid, {}))

@app.route("/update", methods=["POST"])
def update():
    data = request.json
    uid = str(data["uid"])

    if uid not in db:
        db[uid] = {}

    db[uid].update(data["data"])
    save(db)

    return {"ok": True}

app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)))