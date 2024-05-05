from flask import Flask, render_template, request, jsonify
import folium
from shapely.wkb import loads as wkb_loads
import shapely
import DBHandler as db
import pandas as pd
import json

app = Flask(__name__)

def create_map():
    """Erstellt eine neue Folium-Karte ohne Marker oder andere Elemente."""
    start_coords = (47.3693996, 8.56948573846211)  # Beispielkoordinaten für Zürich
    folium_map = folium.Map(location=start_coords, zoom_start=13)
    return folium_map

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/map')
def map():
    folium_map = create_map()

    # HTML-Datei speichern
    folium_map.save('templates/map.html')
    return render_template('map.html')

# Funktion zur Anpassung der Style-Eigenschaften
def style_function_isochrones_hospitals(feature):
    return {
        'fillColor': 'blue',  # Farbe der Füllung
        'color': 'blue',  # Farbe der Linie
        'weight': 1,  # Dicke der Linie
        'fillOpacity': 0.08,  # Deckkraft der Füllung
        'opacity': 0.8,  # Deckkraft der Linien
    }

def add_oev_markers(folium_map):
    oev_data = db.retrieveOevDataFinalZH()

    for index, oev in oev_data.iterrows():
        folium.CircleMarker(
            location=[oev["Latitude"], oev["Longitude"]],
            radius=3,  # Größe des Markers
            color='brown',
            fill=True,
            fill_color='brown',
            popup=oev["Name"]
        ).add_to(folium_map)

    return folium_map

def get_map_isochrones_hospitals():

    folium_map = create_map()

    isochrones_hospitals_zh = db.retrieveIsochronesHospitalsZH()

    for index, isochrone in isochrones_hospitals_zh.iterrows():
        geom = isochrone["geom"]

        geom = wkb_loads(bytes.fromhex(geom))

        geom_geojson = json.loads(json.dumps(shapely.geometry.mapping(geom)))

        folium.GeoJson(geom_geojson, name=isochrone['Krankenhaus'], style_function=style_function_isochrones_hospitals).add_to(folium_map)

    hospitals_zh = db.retrieveHospitalDataFinalZH()

    for index, hospital in hospitals_zh.iterrows():
        folium.Marker([hospital["Latitude"], hospital["Longitude"]], popup=hospital["Krankenhaus"], icon=folium.Icon(color='blue', icon='hospital', prefix='fa')).add_to(folium_map)


    folium_map = add_oev_markers(folium_map)

    return folium_map

# Funktion zur Anpassung der Style-Eigenschaften
def style_function_isochrones_schools(feature):
    return {
        'fillColor': 'green',  # Farbe der Füllung
        'color': 'green',  # Farbe der Linie
        'weight': 1,  # Dicke der Linie
        'fillOpacity': 0.08,  # Deckkraft der Füllung
        'opacity': 0.8,  # Deckkraft der Linien
    }

def get_map_isochrones_schools():

    folium_map = create_map()

    isochrones_schools_zh = db.retrieveIsochronesSchoolsZH()

    for index, isochrone in isochrones_schools_zh.iterrows():
        geom = isochrone["geom"]

        geom = wkb_loads(bytes.fromhex(geom))

        geom_geojson = json.loads(json.dumps(shapely.geometry.mapping(geom)))

        folium.GeoJson(geom_geojson, name=isochrone['Schulname'], style_function=style_function_isochrones_schools).add_to(folium_map)

    schools_zh = db.retrieveSchoolDataFinalZH()

    for index, school in schools_zh.iterrows():
        folium.Marker([school["Latitude"], school["Longitude"]], popup=school["Schulname"], icon=folium.Icon(color='green', icon='school', prefix='fa')).add_to(folium_map)

    
    folium_map = add_oev_markers(folium_map)


    return folium_map


@app.route('/update_map', methods=['POST'])
def update_map():

    # Selected Value from dropdown
    selected_value=request.json['data'][0]
    print(selected_value)

    if selected_value == 'Krankenhäuser':
        folium_map= get_map_isochrones_hospitals()
    elif selected_value == 'Schulen':
        folium_map= get_map_isochrones_schools()
    else:
        folium_map = create_map()

    map_html = folium_map._repr_html_()
    return jsonify(map_html=map_html)


@app.route('/update_table', methods=['POST'])
def get_table():
    selected_value = request.json['data'][0]
    if selected_value == 'Krankenhäuser':
        df = db.retrieveOevInHospitalIsochronesZHEnriched()  # Angenommen, diese Funktion gibt einen DataFrame zurück
    elif selected_value == 'Schulen':
        df = db.retrieveOevInSchoolsIsochronesZHEnriched()
    else:
        df = pd.DataFrame()

    return jsonify(table_html=df.to_html(classes='table table-striped'))

if __name__ == '__main__':
    app.run(debug=True)
