# 🌦️ Weather App

An interactive **Weather App** built using **HTML**, **CSS**, **JavaScript**, and **OpenWeatherMap API**. The application provides real-time weather data and a 5-day forecast with a user-friendly interface and responsive design. The app also includes a Streamlit version created in **Python**, offering an alternative interactive experience.

---

## 🌟 Features
- **Real-Time Weather Data**: Displays temperature, humidity, pressure, wind speed, and direction.
- **5-Day Forecast**: Provides daily weather predictions with dynamic updates.
- **Responsive Design**: Fully responsive interface for all devices, including mobiles, tablets, and desktops.
- **Geolocation Support**: Automatically detects user location for weather updates.
- **Interactive Streamlit Version**: Allows users to search and view weather details through an interactive Python-based interface.
- **Light/Dark Mode Support**: Custom CSS for enhanced visual appeal in both light and dark themes.

---

## 🚀 Technologies Used
### Frontend (HTML/CSS/JavaScript Version)
- **HTML5**: For the structure of the app.
- **CSS3**: For styling and responsiveness.
- **JavaScript**: For API integration and dynamic updates.
- **OpenWeatherMap API**: For fetching real-time weather data.

### Backend (Python/Streamlit Version)
- **Streamlit**: For creating an interactive Python-based app.
- **Python**: For API integration and data processing.
- **OpenWeatherMap API**: For weather data retrieval.

---

## 🎨 Screenshot
### **Streamlit Version**
![Streamlit Weather App Screenshot](https://drive.google.com/uc?export=view&id=15zhjDYnTRWejr7WZAPQ3U1mKJ2jQVWO8)


---

## 🛠️ Installation and Setup
### Frontend Version
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/weather-app.git
   cd weather-app
   ```
2. Open `index.html` in any web browser.

### Streamlit Version
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/weather-app.git
   cd weather-app
   ```
2. Install the dependencies:
   ```bash
   pip install streamlit requests
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run wr.py
   ```

---

## ⚙️ Usage
1. **HTML/CSS/JavaScript Version**:
   - Open the app in your browser.
   - The app will fetch and display weather data for your current location.
   - View detailed weather metrics and a 5-day forecast.

2. **Streamlit Version**:
   - Select a country and city from the sidebar dropdown.
   - Click on "Get Weather Details" to view the weather information.
   - Explore detailed weather metrics and short-term forecasts.

---

## 🌐 API Configuration
- Obtain your API key from the [OpenWeatherMap](https://openweathermap.org/api).
- Replace the placeholder API key in the code with your key:
  - For HTML/JavaScript: Update the `API_KEY` in `script.js`.
  - For Streamlit: Update the `API_KEY` in `wr.py`.

---

## 📜 License
This project is licensed under the [MIT License](LICENSE).

---

## 🙌 Acknowledgments
- [OpenWeatherMap](https://openweathermap.org) for providing weather data.
- [Streamlit](https://streamlit.io) for the interactive Python-based framework.

---

Feel free to customize this README as per your project! Let me know if you need additional sections or edits.
