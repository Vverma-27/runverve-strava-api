# **Strava Integration Flask App**

## **Overview**

This project is a Flask web application that integrates with the Strava API to:

- Authenticate users via OAuth.
- Fetch user details, activities, and activity streams.
- Automatically refresh the access token when it expires.

---

## **Features**

1. **OAuth Authentication**: Uses Strava OAuth to log in and manage access tokens.
2. **Access Token Management**: Automatically refreshes tokens when expired.
3. **Data Fetching**:
   - User profile details.
   - All activities of the user.
   - Heartrate data streams for specific activities.
4. **Error Handling**: Provides detailed error messages for API issues.

---

## **Prerequisites**

1. Python 3.7 or higher.
2. `pip` for managing dependencies.
3. A Strava Developer account:
   - Go to the [Strava Developer Portal](https://www.strava.com/settings/api).
   - Create an app to get your `STRAVA_CLIENT_ID` and `STRAVA_CLIENT_SECRET`.

---

## **Setup Instructions**

### 1. **Clone the Repository**

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

### 3. **Set ENV Variables**

```bash
export STRAVA_CLIENT_ID=<your-client-id>
export STRAVA_CLIENT_SECRET=<your-client-secret>
```

### 4. **Configure Redirect URI**

Set the redirect URI in the Strava developer portal to:
http://localhost:5000/callback

### 5. **Run the project**

```bash
python app.py
```
