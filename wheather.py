from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, urlencode, quote
from html import escape

INDIA = {
    "Andhra Pradesh": ["Visakhapatnam", "Tirupati", "Araku Valley", "Vijayawada", "Kakinada", "Amaravati", "Srisailam", "Horsley Hills"],
    "Arunachal Pradesh": ["Tawang", "Itanagar", "Ziro", "Bomdila", "Namdapha", "Sela Pass", "Dirang", "Mechuka"],
    "Assam": ["Guwahati", "Kaziranga", "Majuli", "Sivasagar", "Manas National Park", "Tezpur", "Haflong", "Kamakhya Temple"],
    "Bihar": ["Patna", "Bodh Gaya", "Nalanda", "Rajgir", "Vaishali", "Gaya", "Pawapuri", "Vikramshila"],
    "Chhattisgarh": ["Raipur", "Bastar", "Chitrakote Falls", "Jagdalpur", "Kanger Valley", "Tirathgarh Falls", "Sirpur", "Dongargarh"],
    "Goa": ["Panaji", "Baga Beach", "Dudhsagar Falls", "Palolem Beach", "Old Goa", "Anjuna Beach", "Candolim Beach", "Chapora Fort"],
    "Gujarat": ["Ahmedabad", "Dwarka", "Rann of Kutch", "Somnath", "Statue of Unity", "Gir National Park", "Saputara", "Modhera Sun Temple"],
    "Haryana": ["Gurugram", "Kurukshetra", "Sultanpur", "Morni Hills", "Panchkula", "Pinjore Gardens", "Badkhal Lake", "Surajkund"],
    "Himachal Pradesh": ["Manali", "Shimla", "Dharamshala", "Kasol", "Kullu", "Spiti Valley", "Dalhousie", "Bir Billing"],
    "Jharkhand": ["Ranchi", "Netarhat", "Deoghar", "Betla National Park", "Hundru Falls", "Dassam Falls", "Parasnath", "Jamshedpur"],
    "Karnataka": ["Bengaluru", "Coorg", "Hampi", "Mysuru", "Gokarna", "Chikmagalur", "Jog Falls", "Badami"],
    "Kerala": ["Munnar", "Alleppey", "Kochi", "Wayanad", "Thekkady", "Varkala", "Kumarakom", "Athirappilly Falls"],
    "Madhya Pradesh": ["Bhopal", "Khajuraho", "Pachmarhi", "Ujjain", "Kanha National Park", "Gwalior", "Orchha", "Bandhavgarh"],
    "Maharashtra": ["Mumbai", "Pune", "Lonavala", "Mahabaleshwar", "Nashik", "Aurangabad", "Shirdi", "Alibaug"],
    "Manipur": ["Imphal", "Loktak Lake", "Ukhrul", "Kangla Fort", "Keibul Lamjao", "Andro", "Moreh", "Shirui Hills"],
    "Meghalaya": ["Shillong", "Cherrapunji", "Dawki", "Mawlynnong", "Nohkalikai Falls", "Living Root Bridge", "Mawsynram", "Balpakram"],
    "Mizoram": ["Aizawl", "Reiek", "Vantawng Falls", "Champhai", "Phawngpui", "Tamdil Lake", "Lunglei", "Murlen National Park"],
    "Nagaland": ["Kohima", "Dimapur", "Dzukou Valley", "Mokokchung", "Mon", "Wokha", "Tuophema", "Intanki National Park"],
    "Odisha": ["Bhubaneswar", "Puri", "Konark", "Chilika Lake", "Cuttack", "Bhitarkanika", "Simlipal", "Udayagiri Caves"],
    "Punjab": ["Amritsar", "Chandigarh", "Ludhiana", "Jalandhar", "Anandpur Sahib", "Wagah Border", "Patiala", "Bathinda"],
    "Rajasthan": ["Jaipur", "Udaipur", "Jaisalmer", "Jodhpur", "Mount Abu", "Pushkar", "Ranthambore", "Chittorgarh"],
    "Sikkim": ["Gangtok", "Nathula Pass", "Tsomgo Lake", "Pelling", "Lachung", "Yumthang Valley", "Ravangla", "Rumtek Monastery"],
    "Tamil Nadu": ["Chennai", "Ooty", "Kodaikanal", "Madurai", "Mahabalipuram", "Rameswaram", "Kanyakumari", "Thanjavur"],
    "Telangana": ["Hyderabad", "Warangal", "Ramoji Film City", "Nagarjuna Sagar", "Golconda Fort", "Yadadri Temple", "Medak Fort", "Ananthagiri Hills"],
    "Tripura": ["Agartala", "Ujjayanta Palace", "Neermahal", "Jampui Hills", "Unakoti", "Sepahijala", "Pilak", "Dumboor Lake"],
    "Uttar Pradesh": ["Agra", "Varanasi", "Lucknow", "Mathura", "Ayodhya", "Prayagraj", "Jhansi", "Fatehpur Sikri"],
    "Uttarakhand": ["Nainital", "Mussoorie", "Rishikesh", "Auli", "Jim Corbett", "Haridwar", "Kedarnath", "Valley of Flowers"],
    "West Bengal": ["Kolkata", "Darjeeling", "Sundarbans", "Digha", "Kalimpong", "Shantiniketan", "Murshidabad", "Mirik"],

    "Andaman and Nicobar Islands": ["Port Blair", "Havelock Island", "Neil Island", "Baratang Island", "Ross Island"],
    "Chandigarh": ["Rock Garden", "Sukhna Lake", "Elante Mall", "Rose Garden", "Japanese Garden"],
    "Delhi": ["India Gate", "Red Fort", "Qutub Minar", "Lotus Temple", "Akshardham"],
    "Jammu and Kashmir": ["Srinagar", "Gulmarg", "Pahalgam", "Sonamarg", "Dal Lake"],
    "Ladakh": ["Leh", "Pangong Lake", "Nubra Valley", "Kargil", "Magnetic Hill"],
    "Lakshadweep": ["Kavaratti", "Agatti Island", "Bangaram Island", "Kadmat Island", "Minicoy Island"],
    "Puducherry": ["Pondicherry Beach", "Auroville", "Promenade Beach", "Paradise Beach", "French Quarter"]
}

PLACE_DETAILS = {
    "Munnar": ("19&deg;C", "Misty and light rain", "Tea gardens, beautiful hills and waterfalls."),
    "Alleppey": ("29&deg;C", "Cloudy", "Backwaters, beaches and houseboat rides."),
    "Kochi": ("30&deg;C", "Partly cloudy", "Heritage streets, Fort Kochi and waterfront views."),
    "Wayanad": ("23&deg;C", "Misty", "Forests, waterfalls and trekking trails."),
    "Thekkady": ("24&deg;C", "Cloudy", "Periyar wildlife sanctuary and boating."),
    "Manali": ("16&deg;C", "Cool and cloudy", "Mountain scenery and adventure activities."),
    "Shimla": ("18&deg;C", "Cloudy", "Hill views, colonial buildings and Mall Road."),
    "Darjeeling": ("17&deg;C", "Cool and misty", "Tea gardens and Himalayan views."),
    "Ooty": ("20&deg;C", "Cloudy", "Botanical gardens and green hills."),
    "Jaipur": ("34&deg;C", "Sunny", "Forts, palaces and colourful local markets."),
    "Udaipur": ("32&deg;C", "Sunny", "Lakes, palaces and royal architecture."),
    "Jaisalmer": ("36&deg;C", "Sunny", "Golden Fort and desert safari experiences."),
    "Mumbai": ("29&deg;C", "Humid and cloudy", "Marine Drive, city culture and beaches."),
    "Rishikesh": ("27&deg;C", "Sunny", "River rafting, yoga and Ganga views."),
    "Agra": ("33&deg;C", "Sunny", "The Taj Mahal and historic Mughal monuments."),
    "Srinagar": ("20&deg;C", "Pleasant", "Dal Lake, gardens and houseboats."),
    "Leh": ("15&deg;C", "Clear sky", "Mountain landscapes and Buddhist monasteries."),
    "Pangong Lake": ("10&deg;C", "Clear and cold", "A famous high-altitude lake."),
    "Chennai": ("32&deg;C", "Sunny", "Marina Beach, temples and city attractions."),
    "Hyderabad": ("30&deg;C", "Partly cloudy", "Charminar, forts and local food.")
}

IMAGES = [
    "https://images.unsplash.com/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=1000&q=80",
    "https://images.unsplash.com/photo-1593693397690-362cb9666fc2?auto=format&fit=crop&w=1000&q=80",
    "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=1000&q=80",
    "https://images.unsplash.com/photo-1602643163983-ed0babc39797?auto=format&fit=crop&w=1000&q=80",
    "https://images.unsplash.com/photo-1514222134-b57cbb8ce073?auto=format&fit=crop&w=1000&q=80"
]

STYLE = """
<style>
* { box-sizing: border-box; }

body {
    margin: 0;
    min-height: 100vh;
    color: #17384b;
    font-family: Arial, sans-serif;
    background: #f2f9fb;
}

.hero {
    min-height: 100vh;
    display: grid;
    place-items: center;
    padding: 35px 20px;
    color: white;
    background:
        linear-gradient(90deg, rgba(4, 30, 47, .9), rgba(4, 30, 47, .25)),
        url("https://images.unsplash.com/photo-1593693397690-362cb9666fc2?auto=format&fit=crop&w=1800&q=85")
        center/cover;
}

.hero-content { width: min(100%, 850px); }

.logo { font-weight: bold; letter-spacing: 2px; }

.tag {
    display: inline-block;
    margin-top: 95px;
    padding: 9px 14px;
    border-radius: 30px;
    background: #ffffff35;
    font-size: 12px;
    letter-spacing: 1px;
}

.hero h1 {
    max-width: 700px;
    margin: 18px 0 12px;
    font-size: clamp(44px, 8vw, 84px);
    line-height: 1;
}

.hero p {
    max-width: 580px;
    font-size: 18px;
    line-height: 1.6;
    color: #e4f5ff;
}

.search-card, .box {
    max-width: 980px;
    border-radius: 20px;
    padding: 30px;
    background: white;
    box-shadow: 0 14px 40px #0a263322;
}

.search-card {
    width: min(100%, 600px);
    margin-top: 32px;
}

select, button {
    width: 100%;
    padding: 15px;
    border-radius: 10px;
    font-size: 16px;
}

select {
    margin-bottom: 12px;
    border: 1px solid #c9d9e0;
    color: #17384b;
}

button {
    border: 0;
    background: #ef6c3b;
    color: white;
    font-weight: bold;
    cursor: pointer;
}

.page-header {
    padding: 60px 20px 100px;
    color: white;
    background: linear-gradient(135deg, #0c6d84, #173b67);
}

.page-header h1, .page-header p {
    max-width: 980px;
    margin-left: auto;
    margin-right: auto;
}

.page-header h1 { font-size: 46px; margin-top: 15px; margin-bottom: 6px; }
.page-header p { color: #d8f1f7; }

.content {
    max-width: 980px;
    margin: -48px auto 50px;
    padding: 0 20px;
}

.card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
    gap: 20px;
}

.place-card {
    overflow: hidden;
    border-radius: 18px;
    background: white;
    box-shadow: 0 10px 25px #17384b19;
}

.place-card img {
    width: 100%;
    height: 175px;
    display: block;
    object-fit: cover;
}

.place-card-content { padding: 18px; }
.place-card h3 { margin: 0 0 8px; }
.place-card p { color: #69808d; line-height: 1.5; }

.card-link, .back {
    color: #087eaf;
    font-weight: bold;
    text-decoration: none;
}

.weather {
    padding: 28px;
    border-radius: 18px;
    color: white;
    background: linear-gradient(135deg, #087eaf, #235c8b);
}

.temperature {
    margin: 8px 0;
    font-size: 62px;
    font-weight: bold;
}

.details-image {
    width: 100%;
    height: 300px;
    margin: 22px 0;
    border-radius: 18px;
    object-fit: cover;
}

.visit-info {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px;
    margin: 25px 0;
}

.info-card {
    display: flex;
    gap: 14px;
    padding: 18px;
    border-radius: 14px;
    background: #edf8fb;
}

.info-card span { font-size: 28px; }
.info-card h3 { margin: 0 0 7px; color: #0d6680; }
.info-card p { margin: 0; color: #5d7480; }

.map {
    width: 100%;
    height: 350px;
    border: 0;
    border-radius: 16px;
}

.map-button {
    display: inline-block;
    padding: 13px 18px;
    border-radius: 10px;
    background: #087eaf;
    color: white;
    font-weight: bold;
    text-decoration: none;
}

.note { color: #71838d; }

@media (max-width: 600px) {
    .box { padding: 22px; }
    .page-header h1 { font-size: 36px; }
}
</style>
"""

def page(content):
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RoamWeather India</title>
    {STYLE}
</head>
<body>{content}</body>
</html>"""

def image_for(place):
    return IMAGES[sum(ord(letter) for letter in place) % len(IMAGES)]

def place_details(state, place):
    if place in PLACE_DETAILS:
        return PLACE_DETAILS[place]

    return (
        "28&deg;C",
        "Partly cloudy",
        f"A popular destination in {state}, perfect for sightseeing and local experiences."
    )

def visiting_hours(place):
    if any(word in place for word in ["Beach", "Lake", "Falls", "Valley", "Hills", "Island"]):
        return "Open all day"
    if any(word in place for word in ["Temple", "Monastery", "Church"]):
        return "6:00 AM - 8:00 PM"
    if any(word in place for word in ["Fort", "Palace", "Museum", "Caves"]):
        return "9:00 AM - 5:30 PM"
    if any(word in place for word in ["National Park", "Sanctuary", "Wildlife"]):
        return "6:00 AM - 5:00 PM"
    return "9:00 AM - 6:00 PM"

def home_page():
    options = "<option value='' disabled selected>Choose your destination state</option>"

    for state in INDIA:
        options += f"<option value='{escape(state)}'>{escape(state)}</option>"

    return page(f"""
<section class="hero">
    <div class="hero-content">
        <div class="logo">ROAMWEATHER INDIA</div>
        <div class="tag">WEATHER + TRAVEL GUIDE</div>
        <h1>Find your next beautiful escape.</h1>
        <p>Choose an Indian state, explore destinations, and check weather before you travel.</p>

        <form class="search-card" method="get">
            <select name="state" required>{options}</select>
            <button type="submit">Explore places</button>
        </form>
    </div>
</section>
""")

def state_page(state):
    cards = ""

    for place in INDIA[state]:
        link = "/?" + urlencode({"state": state, "place": place})
        weather = place_details(state, place)

        cards += f"""
<article class="place-card">
    <img src="{image_for(place)}" alt="{escape(place)}">
    <div class="place-card-content">
        <h3>{escape(place)}</h3>
        <p>{weather[2]}</p>
        <a class="card-link" href="{link}">View details &rarr;</a>
    </div>
</article>
"""

    return page(f"""
<section class="page-header">
    <p><a class="back" style="color:white" href="/">&larr; Change state</a></p>
    <h1>{escape(state)}</h1>
    <p>Explore popular nearby places and travel information.</p>
</section>

<main class="content">
    <div class="card-grid">{cards}</div>
</main>
""")

def place_page(state, place):
    temperature, condition, description = place_details(state, place)
    hours = visiting_hours(place)
    back_link = "/?" + urlencode({"state": state})
    location = place + ", " + state + ", India"
    map_query = quote(location)
    map_link = "https://www.google.com/maps/search/?api=1&query=" + map_query
    map_embed = "https://www.google.com/maps?q=" + map_query + "&output=embed"

    return page(f"""
<section class="page-header">
    <p><a class="back" style="color:white" href="{back_link}">&larr; Back to {escape(state)}</a></p>
    <h1>{escape(place)}</h1>
    <p>{escape(state)}, India</p>
</section>

<main class="content">
    <div class="box">
        <div class="weather">
            <p>WEATHER AT THIS DESTINATION</p>
            <p class="temperature">{temperature}</p>
            <h2>{condition}</h2>
        </div>

        <img class="details-image" src="{image_for(place)}" alt="{escape(place)}">

        <h2>Why visit {escape(place)}?</h2>
        <p>{description}</p>

        <div class="visit-info">
            <div class="info-card">
                <span>🕒</span>
                <div>
                    <h3>Typical visiting hours</h3>
                    <p>{hours}</p>
                </div>
            </div>

            <div class="info-card">
                <span>📍</span>
                <div>
                    <h3>Location</h3>
                    <p>{escape(place)}, {escape(state)}</p>
                </div>
            </div>
        </div>

        <h2>Map location</h2>
        <iframe class="map" src="{map_embed}" loading="lazy"></iframe>

        <p>
            <a class="map-button" href="{map_link}" target="_blank">
                Open in Google Maps &rarr;
            </a>
        </p>

        <p class="note">
            Weather and visiting hours are sample information. Check official sources before travelling.
        </p>
    </div>
</main>
""")

class WeatherHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        state = query.get("state", [None])[0]
        place = query.get("place", [None])[0]

        if state in INDIA and place in INDIA[state]:
            html = place_page(state, place)
        elif state in INDIA:
            html = state_page(state)
        else:
            html = home_page()

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

print("Open http://localhost:8000 in your browser")
HTTPServer(("localhost", 8000), WeatherHandler).serve_forever()