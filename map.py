# --------------------------------------------------------------------------------------------------------------------------
# Python web application which will be built and deployed in Docker to demonstrate building and deploying from Jenkins using pipeline and terraform
# See README.md and see repository mabrahamdevops/jenkins-docker-container/README.md for additonal details on deploying Jenkins and Docker in Linux contair hosted
# on an AWS EC2 cluster as well as creating this application in a docker container and deploying via Terraform.
#
# (C) 2020 Mark Abraham, Brandon, FL
# Email: markabraham3232@gmail.com
#  
# The majority of comments will be placed in this block for readablility. Any additional comments needed for clarity are placed 
# next to the code statement
#
# Folium is used to visualize python data.  Here it is used with Stamen Terrain to render our map
# https://python-visualization.github.io/folium/
# Using pandas method pandas.core.frame.DataFrame to call data from txt or csv file
#
# Using Flask to host static html via rendure_template
# Flask documentation: https://flask.palletsprojects.com/en/1.1.x/
#
# Using variables for data lists "latitude", "longitude", and "elevation". For each variable in column python will extract the first
# value.  Python will iterate through all values. Ref line 35.
#
# Added python functions to divide elevation data by color.  Ref line 35.
#
# Using the Marker class allows Python to convert code to java script code using Leaflet to display pop up markers on 
# the map. Ref line 36
# --------------------------------------------------------------------------------------------------------------------------
 
import folium
import pandas                       
from folium import IFrame
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('Map_html_popup.html')

if __name__ == '__main__':
    app.run(debug=True)


data = pandas.read_csv("volcanoes.csv")
lat = list(data["LAT"])
lon = list(data["LON"])
nm  = list(data["NAME"])
elev = list(data["ELEV"])

# HTML formatting is used to create a link to Google in order to search based on volcano name.
html = """
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

def elev_color_function(elevation):
    if elevation < 1500:
        return 'orange'
    elif 1500 <= elevation < 2500:
        return 'blue'
    else:
        return 'red'

map = folium.Map(                                       # Layer one: base map
    location=[35.9311, -84.3100], 
    zoom_started=8, 
    tiles="Stamen Terrain",
)

map.add_child(folium.CircleMarker(
    location=[35.9311, -84.3100], 
    radius = 6,
    popup="Zoom out to view Volcanoes: western US", 
    color='black',
    fill_opacity=0.7))

fg = folium.FeatureGroup(name="Volcanoes west coast")    # Use feature group object variable to add multiple features to map to better organize code and for controlling layer control features such as turning layers on and off
for lt, ln, nm, el in zip(lat, lon, nm, elev):           # Layer two: point layer for volcano data     
    fg.add_child(folium.CircleMarker(
        location=[lt, ln],
        radius = 5,
        popup=str(nm)+ " volcano    " + str(el)+" meters", 
        fill_color=elev_color_function(el),
        color = 'grey',
        fill_opacity=0.7))

map.add_child(fg)

map.save("templates/Map_html_popup.html")