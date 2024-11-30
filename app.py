from flask import Flask, session, jsonify, render_template, redirect, request, url_for
import os
import time
from flask_cors import CORS
from strava_api import fetch_activities, fetch_stream, fetch_user, get_access_token, refresh_access_token, get_authorization_url

SCOPE = "read,activity:read_all"
app = Flask(__name__)
CORS(app)

# Secret key for Flask sessions
app.secret_key = os.urandom(24)

def ensure_access_token():
    """
    Checks if the access token is valid and refreshes it if expired.
    """
    if 'access_token' in session and 'expires_at' in session:
        current_time = time.time()
        if current_time >= session['expires_at']:
            # Token has expired, refresh it
            try:
                refreshed_data = refresh_access_token(session['refresh_token'])
                session['access_token'] = refreshed_data['access_token']
                session['refresh_token'] = refreshed_data['refresh_token']
                session['expires_at'] = refreshed_data['expires_at']
            except Exception as e:
                return jsonify({"error": "Failed to refresh access token", "details": str(e)}), 500
    else:
        return jsonify({"error": "Not authenticated"}), 401

@app.route('/')
def index():
    if 'access_token' not in session:
        return redirect(get_authorization_url())
    try:
        return render_template("index.html")
    except Exception as e:
        return f"Error: {e}"

@app.route("/callback")
def callback():
    code = request.args.get("code")
    scope = request.args.get("scope")
    if scope != SCOPE:
        return redirect(get_authorization_url())
    
    # Save tokens and expiry in session
    token_data = get_access_token(code)
    session['access_token'] = token_data['access_token']
    session['refresh_token'] = token_data['refresh_token']
    session['expires_at'] = token_data['expires_at']
    return redirect("/")

@app.route('/get_activities')
def get_activities():
    # Ensure token is valid before proceeding
    ensure_access_token()
    if 'access_token' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    try:
        data = fetch_activities(session['access_token'])
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_stream')
def get_stream():
    # Ensure token is valid before proceeding
    ensure_access_token()
    if 'access_token' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    try:
        activity_id = request.args.get('activity_id')
        if not activity_id:
            return jsonify({"error": "Missing required query parameters"}), 400
        response = fetch_stream(session['access_token'], activity_id)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_user')
def get_user():
    # Ensure token is valid before proceeding
    ensure_access_token()
    if 'access_token' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    try:
        response = fetch_user(session['access_token'])
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
