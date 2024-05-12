import requests
from datetime import datetime as dt
import smtplib

LATITUDE = 49.133730
LONGITUDE = -16.285950


def get_sunrise_sunset_hour():
    parameters = {
        "lat": LATITUDE,
        "lng": LONGITUDE,
        "formatted": 0
    }

    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    data = response.json()

    # get the sunset hour
    sunrise_hour = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset_hour = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    return sunrise_hour, sunset_hour


# is position within -5 and +5 degrees of the ISS position
def is_iss_near_my_location():
    return LATITUDE -5 <= iss_latitude <= LATITUDE + 5 and LONGITUDE -5 <= iss_longitude <= LONGITUDE


def send_email():
    my_email = "your email @gmail.com"
    password = "your app password"
    to_email = "email address receiver"

    with smtplib.SMTP("smtp.gmail.com") as my_connection:
        my_connection.starttls()
        my_connection.login(user=my_email, password=password)
        my_connection.sendmail(from_addr=my_email, to_addrs=to_email, msg="Subject: ISS is near you!\n\nISS is in the zone!")


iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
if iss_response.status_code != 200:
    iss_response.raise_for_status()

iss_latitude = float(iss_response.json()["iss_position"]["latitude"])
iss_longitude = float(iss_response.json()["iss_position"]["longitude"])

# when it is dark at my location
time_now = dt.now()
if get_sunrise_sunset_hour()[0] <= time_now.hour <= get_sunrise_sunset_hour()[1] and is_iss_near_my_location():
    send_email()
else:
    print("ISS is not near you")