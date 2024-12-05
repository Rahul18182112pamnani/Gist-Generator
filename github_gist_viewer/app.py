from flask import Flask, request, jsonify, render_template
import requests
from datetime import datetime

app = Flask(__name__)

GITHUB_API_URL = "https://api.github.com/users/{username}/gists"

def fetch_gists(username):
    """Fetch gists for a given GitHub username."""
    url = GITHUB_API_URL.format(username=username)
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

def group_gists_by_month(gists):
    """Group gists by month."""
    grouped = {}
    for gist in gists[:5]:  # Fetch only the last 5 gists
        created_at = datetime.strptime(gist['created_at'], "%Y-%m-%dT%H:%M:%SZ")
        month = created_at.strftime("%B %Y")
        if month not in grouped:
            grouped[month] = []
        grouped[month].append({
            "description": gist['description'] or "No description",
            "url": gist['html_url']
        })
    return grouped

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_gists", methods=["POST"])
def get_gists():
    username = request.form.get("username")
    gists = fetch_gists(username)
    if gists is None:
        return jsonify({"error": "User not found or rate limit exceeded"}), 404

    grouped_gists = group_gists_by_month(gists)
    return jsonify(grouped_gists)

if __name__ == "__main__":
    app.run(debug=True)

