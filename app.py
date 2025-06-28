from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb+srv://thirulingeshwart:<db_password>@cluster0.osyvkoa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['hmi_class']
users = db['users']

# -------------------------
# CLASS WEB ROUTES
# -------------------------

@app.route('/')
def class_home():
    return render_template('class/index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = {
        "name": data['name'],
        "phone": data['phone'],
        "email": data['email'],
        "status": "pending"
    }
    users.insert_one(user)
    return jsonify({"message": "Registered successfully!"})

@app.route('/status/<email>')
def check_status(email):
    user = users.find_one({"email": email})
    if user:
        return jsonify({"status": user['status']})
    return jsonify({"status": "not found"})

@app.route('/videos/<email>')
def videos(email):
    user = users.find_one({"email": email})
    if user:
        if user["status"] == "accepted":
            return render_template('class/videos.html', name=user["name"], email=email)
        elif user["status"] == "rejected":
            return "❌ You have been rejected."
        else:
            return "⏳ Please wait for admin approval."
    return "❌ User not found."

@app.route('/complete', methods=['POST'])
def complete():
    data = request.get_json()
    users.update_one({"email": data["email"]}, {"$set": {"status": "completed"}})
    return jsonify({"message": "Class marked as completed"})

# -------------------------
# ADMIN DASHBOARD ROUTES
# -------------------------

@app.route('/admin')
def admin_dashboard():
    all_users = list(users.find())
    return render_template('admin/dashboard.html', users=all_users)

@app.route('/update_status', methods=['POST'])
def update_status():
    data = request.get_json()
    users.update_one({"email": data["email"]}, {"$set": {"status": data["status"]}})
    return jsonify({"message": "Status updated."})

# -------------------------
# MAIN
# -------------------------

if __name__ == "__main__":
    app.run(port=5000, debug=True)
