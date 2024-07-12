import streamlit as st
import base64
import datetime
import requests

img_taxi_path = 'img/taxi.jpeg'
url_predict = 'https://taxifare.lewagon.ai/predict'


def get_location(address:str)->tuple:
    url = "https://nominatim.openstreetmap.org/search"
    params= {"q":address, "format":"json"}
    response = requests.get(url, params = params)
    print(response.content)
    return response.json()[0]["lat"], response.json()[0]["lon"]


#latlon = get_location("13, Rue de la glacière, 75013, paris, france")
#print(latlon)


def load_image(path):
    with open(path, 'rb') as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    return encoded

def image_tag(path):
    encoded = load_image(path)
    tag = f'<img src="data:image/png;base64,{encoded}" style="width:150px">'
    return tag

st.title('Taxifare')
st.write(image_tag(img_taxi_path), unsafe_allow_html=True)
st.title('The best fare estimator in NY')




passenger_count = st.slider('Number of passenger', 1, 8, 1)

st.markdown('## Pick-up')
pickup_date = st.date_input( "Date",  datetime.datetime.now())
pickup_time = st.time_input( "Time",  datetime.datetime.now())
pickup_lat = st.number_input("Lat", key="pickup_lat")
pickup_lon = st.number_input("Lon", key="pickup_lon")

st.markdown('## Drop-off')
dropoff_lat = st.number_input("Lat", key="dropoff_lat")
dropoff_lon = st.number_input("Lon", key="dropoff_lon")


pickup_dt =pickup_date.strftime("%Y-%m-%d")  + " " +  pickup_time.strftime("%H:%M:%S")



params = {'pickup_datetime':pickup_dt,
'pickup_longitude':pickup_lon,
'pickup_latitude':pickup_lat,
'dropoff_longitude':dropoff_lon,
'dropoff_latitude':dropoff_lat,
'passenger_count': passenger_count}


if st.button("Calculer"):
    response = requests.get(url_predict, params=params).json()


    r = round(response['fare'], 2)
    st.markdown(f"## Prix : ${r}")
