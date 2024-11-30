import requests
import os
import re

from APIException import APIException

STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:5000/callback"
BASE_URL = "https://www.strava.com/api/v3"
SCOPE="read,activity:read_all"

#generate authorization url
def get_authorization_url():
    return f"https://www.strava.com/oauth/authorize?client_id={STRAVA_CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&approval_prompt=force&scope={SCOPE}"

#called when access token is expired, to refresh it
def refresh_access_token(refresh_token):
    url = "https://www.strava.com/oauth/token"
    payload = {
        'client_id': os.getenv('STRAVA_CLIENT_ID'),
        'client_secret': os.getenv('STRAVA_CLIENT_SECRET'),
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        raise Exception(f"Failed to refresh token: {response.text}")
    return response.json()  # Returns new access_token, refresh_token, and expires_at

#exchange auth code for access token
def get_access_token(auth_code):
    response = requests.post(
        "https://www.strava.com/oauth/token",
        data={
            "client_id": STRAVA_CLIENT_ID,
            "client_secret": STRAVA_CLIENT_SECRET,
            "code": auth_code,
            "grant_type": "authorization_code"
        }
    )
    data = response.json()
    return data

#fetch all activities of user (could add pagination)
def fetch_activities(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/athlete/activities", headers=headers)
    data = response.json()
    if response.status_code == 200:
        desired_keys = ["name","id","distance","elapsed_time","average_speed","max_speed","moving_time","sport_type","average_speed","has_heartrate","max_heartrate","average_heartrate","kilojoules"]
        parsed_data = []
        for activity in data:
            filtered_activity = {key: activity[key] for key in desired_keys if key in activity}
            if "sport_type" in filtered_activity:
                sport_type = filtered_activity["sport_type"]  # For example: "MountainBiking"
                # Split CamelCase into separate words
                split_sport_type = re.findall(r'[A-Z][^A-Z]*', sport_type)
                # Join with spaces to make it user-friendly
                formatted_sport_type = ' '.join(split_sport_type)
                filtered_activity["sport_type"] = formatted_sport_type
            parsed_data.append(filtered_activity)
        return parsed_data
    else:
        if response.status_code == 404:
            raise APIException(f"Activity not found", 404)
        else:
            raise APIException(f"Internal server error: {response.text}", response.status_code)

#fetch activity stream heartrate data (only called if heartrate data is present)
def fetch_stream(access_token,activity_id):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/activities/{activity_id}/streams",params={"keys":"heartrate","key_by_type":True}, headers=headers)
    data = response.json()
    if response.status_code == 200:
        return data['heartrate'] if "heartrate" in data else []
    else:
        if response.status_code == 404:
            raise APIException(f"Activity not found", 404)
        else:
            raise APIException(f"Internal server error: {response.text}", response.status_code)

#fetch basic user details
def fetch_user(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/athlete", headers=headers)
    data = response.json()
    if response.status_code == 200:
        return data
    else:
        raise Exception(f"Error fetching user details: {response.text}")