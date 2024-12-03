import streamlit as st
import requests
import json
from datetime import datetime

# OpenWeatherMap API configuration
API_KEY = '0d912a814f4b9f29ff8d74efcb4abb7c'
BASE_WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'
BASE_FORECAST_URL = 'https://api.openweathermap.org/data/2.5/forecast'

# Custom CSS for enhanced styling with theme compatibility
def local_css():
    st.markdown("""
    <style>
    /* Base App Styling */
    .stApp {
        background-color: var(--background-color);
        color: var(--text-color);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Dark Mode Compatibility */
    [data-theme="dark"] {
        --background-color: #1e1e1e;
        --text-color: #ffffff;
        --card-background: #2c2c2c;
        --metric-background: #3a3a3a;
        --gradient-start: #4a4a4a;
        --gradient-end: #2c2c2c;
    }

    [data-theme="light"] {
        --background-color: #f0f2f6;
        --text-color: #2c3e50;
        --card-background: #ffffff;
        --metric-background: #e6f2ff;
        --gradient-start: #6190E8;
        --gradient-end: #A7BFE8;
    }

    /* Card Styling */
    .stCard {
        background-color: var(--card-background);
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        padding: 20px;
        margin-bottom: 20px;
        color: var(--text-color);
    }

    /* Metric Styling */
    .stMetric {
        background-color: var(--metric-background);
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        color: var(--text-color);
    }

    .stMetric > div {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .stMetric-value {
        font-size: 1.5em;
        color: var(--text-color);
    }

    .stMetric-label {
        color: var(--text-color);
        opacity: 0.7;
        margin-bottom: 5px;
    }

    /* Gradient Header */
    .gradient-header {
        background: linear-gradient(to right, var(--gradient-start), var(--gradient-end));
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }

    /* Forecast Card */
    .forecast-card {
        background-color: var(--card-background);
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        transition: transform 0.3s ease;
        color: var(--text-color);
        border: 1px solid rgba(128,128,128,0.2);
    }

    .forecast-card:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* Ensure text visibility */
    h1, h2, h3, p, span, div {
        color: var(--text-color) !important;
    }
    </style>
    """, unsafe_allow_html=True)

def load_cities_by_country():
    """
    Load an extensive list of countries and their major cities
    
    Returns:
        dict: Dictionary of countries and their top cities
    """
    return {
        "United States": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"],
        "United Kingdom": ["London", "Manchester", "Birmingham", "Glasgow", "Liverpool", "Edinburgh", "Leeds", "Bristol", "Sheffield", "Belfast"],
        "Canada": ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa", "Edmonton", "Quebec City", "Winnipeg", "Hamilton", "Halifax"],
        "Australia": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Gold Coast", "Newcastle", "Canberra", "Wollongong", "Hobart"],
        "India": ["Mumbai", "Delhi", "Bangalore", "Kolkata", "Chennai", "Hyderabad", "Pune", "Ahmedabad", "Surat", "Jaipur"],
        "Brazil": ["Sao Paulo", "Rio de Janeiro", "Salvador", "Brasilia", "Fortaleza", "Belo Horizonte", "Manaus", "Curitiba", "Recife", "Porto Alegre"],
        "Russia": ["Moscow", "Saint Petersburg", "Novosibirsk", "Yekaterinburg", "Nizhny Novgorod", "Kazan", "Chelyabinsk", "Omsk", "Samara", "Rostov-on-Don"],
        "China": ["Shanghai", "Beijing", "Guangzhou", "Shenzhen", "Chengdu", "Nanjing", "Wuhan", "Xi'an", "Hangzhou", "Suzhou"],
        "Japan": ["Tokyo", "Yokohama", "Osaka", "Nagoya", "Sapporo", "Fukuoka", "Kawasaki", "Kobe", "Kyoto", "Saitama"],
        "Germany": ["Berlin", "Hamburg", "Munich", "Cologne", "Frankfurt", "Stuttgart", "Düsseldorf", "Leipzig", "Dortmund", "Essen"],
        "France": ["Paris", "Marseille", "Lyon", "Toulouse", "Nice", "Nantes", "Montpellier", "Strasbourg", "Bordeaux", "Lille"],
        "Italy": ["Rome", "Milan", "Naples", "Turin", "Palermo", "Genoa", "Bologna", "Florence", "Bari", "Catania"],
        "Spain": ["Madrid", "Barcelona", "Valencia", "Seville", "Zaragoza", "Málaga", "Murcia", "Palma", "Las Palmas", "Bilbao"],
        "Mexico": ["Mexico City", "Guadalajara", "Monterrey", "Puebla", "Tijuana", "Cancún", "Mérida", "Tampico", "León", "Querétaro"],
        "South Africa": ["Johannesburg", "Cape Town", "Durban", "Pretoria", "Port Elizabeth", "Bloemfontein", "Nelspruit", "Polokwane", "Kimberley", "Rustenburg"],
        "South Korea": ["Seoul", "Busan", "Incheon", "Daegu", "Daejeon", "Gwangju", "Suwon", "Ulsan", "Changwon", "Seongnam"],
        "Argentina": ["Buenos Aires", "Córdoba", "Rosario", "Mendoza", "La Plata", "San Miguel de Tucumán", "Mar del Plata", "Salta", "Santa Fe", "Resistencia"],
        "Turkey": ["Istanbul", "Ankara", "Izmir", "Bursa", "Adana", "Gaziantep", "Konya", "Antalya", "Mersin", "Diyarbakır"],
        "Egypt": ["Cairo", "Alexandria", "Giza", "Shubra El Kheima", "Port Said", "Suez", "Luxor", "Mansoura", "El-Mahalla El-Kubra", "Tanta"]
    }

def get_weather_data(city, country):
    """Fetch comprehensive weather data for a given city"""
    try:
        location = f"{city},{country}"
        current_params = {
            'q': location,
            'appid': API_KEY,
            'units': 'metric'
        }
        
        forecast_params = current_params.copy()
        forecast_params['cnt'] = 5
        
        current_response = requests.get(BASE_WEATHER_URL, params=current_params)
        forecast_response = requests.get(BASE_FORECAST_URL, params=forecast_params)
        
        current_response.raise_for_status()
        forecast_response.raise_for_status()
        
        return (current_response.json(), forecast_response.json())
    
    except requests.RequestException as e:
        st.error(f"Error fetching weather data: {e}")
        return None, None

def get_wind_direction(degrees):
    """Convert wind degrees to cardinal direction"""
    directions = [
        "N", "NNE", "NE", "ENE", 
        "E", "ESE", "SE", "SSE", 
        "S", "SSW", "SW", "WSW", 
        "W", "WNW", "NW", "NNW"
    ]
    index = round(degrees / (360 / len(directions))) % len(directions)
    return directions[index]

def display_weather_details(current_data, forecast_data):
    """Comprehensive weather information display"""
    if not current_data or not forecast_data:
        st.warning("Unable to retrieve complete weather information.")
        return

    # Extracting data
    city_name = current_data['name']
    country = current_data['sys']['country']
    temp = current_data['main']['temp']
    feels_like = current_data['main']['feels_like']
    temp_min = current_data['main']['temp_min']
    temp_max = current_data['main']['temp_max']
    
    weather_desc = current_data['weather'][0]['description'].capitalize()
    weather_icon = current_data['weather'][0]['icon']
    
    humidity = current_data['main']['humidity']
    pressure = current_data['main']['pressure']
    wind_speed = current_data['wind']['speed']
    wind_direction = get_wind_direction(current_data['wind']['deg'])

    # Title with gradient background
    st.markdown("""
    <div style="background: linear-gradient(to right, #6190E8, #A7BFE8); 
                padding: 20px; 
                border-radius: 10px; 
                color: white; 
                text-align: center;">
        <h1>🌦️ Weather in {}, {}</h1>
    </div>
    """.format(city_name, country), unsafe_allow_html=True)
    
    # Main weather display
    st.markdown('<div class="stCard">', unsafe_allow_html=True)
    
    # Columns for current weather
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image(f"http://openweathermap.org/img/wn/{weather_icon}@2x.png")
        st.metric("Current Temperature", f"{temp:.1f}°C")
        st.metric("Feels Like", f"{feels_like:.1f}°C")
    
    with col2:
        st.markdown(f'<div class="stMetric"><h3>{weather_desc}</h3></div>', unsafe_allow_html=True)
        st.metric("Humidity", f"{humidity}%")
        st.metric("Pressure", f"{pressure} hPa")
    
    with col3:
        st.metric("Wind Speed", f"{wind_speed} m/s")
        st.metric("Wind Direction", wind_direction)
        st.metric("Temp Range", f"{temp_min:.1f}°C - {temp_max:.1f}°C")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Forecast section
    st.markdown("## 📅 Short Forecast")
    forecast_cols = st.columns(3)
    
    for i, forecast in enumerate(forecast_data['list'][:3]):
        with forecast_cols[i]:
            st.markdown('<div class="forecast-card">', unsafe_allow_html=True)
            
            forecast_time = datetime.strptime(forecast['dt_txt'], '%Y-%m-%d %H:%M:%S')
            formatted_time = forecast_time.strftime('%I:%M %p')
            
            forecast_temp = forecast['main']['temp']
            forecast_desc = forecast['weather'][0]['description'].capitalize()
            forecast_icon = forecast['weather'][0]['icon']
            
            st.image(f"http://openweathermap.org/img/wn/{forecast_icon}@2x.png", width=100)
            st.markdown(f"**{formatted_time}**")
            st.markdown(f"**{forecast_temp:.1f}°C**")
            st.markdown(f"*{forecast_desc}*")
            
            st.markdown('</div>', unsafe_allow_html=True)

def main():
    # Page configuration and custom CSS
    st.set_page_config(page_title="Global Weather App", page_icon="🌦️", layout="wide")
    local_css()  # Apply custom styling
    
    # Load countries and cities
    countries_cities = load_cities_by_country()
    
    # Sidebar with gradient
    st.sidebar.markdown("""
    <div style="background: linear-gradient(to bottom, #6190E8, #A7BFE8); 
                padding: 20px; 
                border-radius: 10px; 
                color: white;">
        <h2>🌍 Weather Selector</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Country selection
    selected_country = st.sidebar.selectbox(
        "Select Country", 
        sorted(list(countries_cities.keys())),
        index=0
    )
    
    # City selection based on country
    selected_city = st.sidebar.selectbox(
        "Select City", 
        sorted(countries_cities[selected_country]),
        index=0
    )
    
    # Search and display weather
    if st.sidebar.button("Get Weather Details", type="primary"):
        if selected_city and selected_country:
            with st.spinner('Fetching weather data...'):
                current_data, forecast_data = get_weather_data(selected_city, selected_country)
                
                if current_data and forecast_data:
                    display_weather_details(current_data, forecast_data)
                else:
                    st.error("Failed to retrieve weather information. Please try again.")

    # Footer with gradient
    st.markdown("""
    <div style="background: linear-gradient(to right, #6190E8, #A7BFE8); 
                padding: 10px; 
                border-radius: 10px; 
                color: white; 
                text-align: center;">
        Powered by OpenWeatherMap | Data may be limited due to free API tier
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()