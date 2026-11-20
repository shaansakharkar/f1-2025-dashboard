import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="F1 ’25 Season", page_icon="🏁", layout="wide")

# Data is built into this file, so no separate json file is needed.
DATA_JSON = r'''{"drivers":[{"driver":"Max Verstappen","team":"Red Bull Racing","wins":8,"points":374.0,"cumulative":[18.0,30.0,55.0,63.0,81.0,93.0,118.0,130.0,131.0,149.0,149.0,159.0,171.0,173.0,191.0,216.0,241.0,259.0,284.0,299.0,299.0,324.0,349.0,374.0]},{"driver":"Oscar Piastri","team":"McLaren","wins":7,"points":371.0,"cumulative":[2.0,27.0,42.0,67.0,92.0,117.0,132.0,147.0,172.0,184.0,202.0,220.0,245.0,263.0,288.0,303.0,303.0,315.0,325.0,335.0,335.0,335.0,353.0,371.0]},{"driver":"Lando Norris","team":"McLaren","wins":6,"points":369.0,"cumulative":[25.0,43.0,61.0,76.0,88.0,106.0,124.0,149.0,167.0,167.0,192.0,217.0,235.0,260.0,260.0,278.0,284.0,299.0,317.0,342.0,342.0,342.0,354.0,369.0]},{"driver":"George Russell","team":"Mercedes","wins":2,"points":277.0,"cumulative":[15.0,30.0,40.0,58.0,68.0,83.0,89.0,89.0,101.0,126.0,136.0,137.0,147.0,162.0,174.0,184.0,202.0,227.0,235.0,241.0,241.0,259.0,267.0,277.0]},{"driver":"Charles Leclerc","team":"Ferrari","wins":0,"points":225.0,"cumulative":[4.0,4.0,16.0,28.0,43.0,49.0,57.0,75.0,90.0,100.0,115.0,115.0,130.0,142.0,142.0,154.0,156.0,164.0,179.0,197.0,197.0,209.0,213.0,225.0]},{"driver":"Lewis Hamilton","team":"Ferrari","wins":0,"points":135.0,"cumulative":[1.0,1.0,7.0,17.0,23.0,27.0,39.0,49.0,57.0,65.0,77.0,89.0,95.0,95.0,95.0,103.0,107.0,111.0,123.0,127.0,127.0,131.0,131.0,135.0]},{"driver":"Kimi Antonelli","team":"Mercedes","wins":0,"points":117.0,"cumulative":[12.0,20.0,28.0,28.0,36.0,44.0,44.0,44.0,44.0,59.0,59.0,59.0,59.0,60.0,60.0,62.0,74.0,84.0,84.0,92.0,92.0,107.0,117.0,117.0]},{"driver":"Alexander Albon","team":"Williams","wins":0,"points":70.0,"cumulative":[10.0,16.0,18.0,18.0,20.0,30.0,40.0,42.0,42.0,42.0,42.0,46.0,54.0,54.0,64.0,70.0,70.0,70.0,70.0,70.0,70.0,70.0,70.0,70.0]},{"driver":"Carlos Sainz","team":"Williams","wins":0,"points":54.0,"cumulative":[0.0,1.0,1.0,1.0,5.0,7.0,11.0,12.0,12.0,13.0,13.0,13.0,13.0,13.0,13.0,13.0,28.0,29.0,29.0,29.0,29.0,39.0,54.0,54.0]},{"driver":"Fernando Alonso","team":"Aston Martin","wins":0,"points":51.0,"cumulative":[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,2.0,8.0,14.0,16.0,16.0,26.0,30.0,30.0,30.0,36.0,37.0,37.0,37.0,37.0,43.0,51.0]}],"teams":[{"team":"McLaren","points":740.0},{"team":"Red Bull Racing","points":395.0},{"team":"Mercedes","points":394.0},{"team":"Ferrari","points":360.0},{"team":"Williams","points":124.0},{"team":"Aston Martin","points":80.0},{"team":"Racing Bulls","points":78.0},{"team":"Kick Sauber","points":68.0},{"team":"Haas F1 Team","points":65.0},{"team":"Alpine","points":19.0}],"rounds":[{"round":1,"name":"Australian Grand Prix","hasResults":true,"winner":"Lando Norris","team":"McLaren","winnerTime":"1:42:06.304","results":[{"pos":1,"driver":"Lando Norris","team":"McLaren","points":25.0},{"pos":2,"driver":"Max Verstappen","team":"Red Bull Racing","points":18.0},{"pos":3,"driver":"George Russell","team":"Mercedes","points":15.0},{"pos":4,"driver":"Kimi Antonelli","team":"Mercedes","points":12.0},{"pos":5,"driver":"Alexander Albon","team":"Williams","points":10.0},{"pos":6,"driver":"Lance Stroll","team":"Aston Martin","points":8.0},{"pos":7,"driver":"Nico Hulkenberg","team":"Kick Sauber","points":6.0},{"pos":8,"driver":"Charles Leclerc","team":"Ferrari","points":4.0},{"pos":9,"driver":"Oscar Piastri","team":"McLaren","points":2.0},{"pos":10,"driver":"Lewis Hamilton","team":"Ferrari","points":1.0}]},{"round":2,"name":"Chinese Grand Prix","hasResults":true,"winner":"Oscar Piastri","team":"McLaren","winnerTime":"1:30:55.026","results":[{"pos":1,"driver":"Oscar Piastri","team":"McLaren","points":25.0},{"pos":2,"driver":"Lando Norris","team":"McLaren","points":18.0},{"pos":3,"driver":"George Russell","team":"Mercedes","points":15.0},{"pos":4,"driver":"Max Verstappen","team":"Red Bull Racing","points":12.0},{"pos":5,"driver":"Esteban Ocon","team":"Haas F1 Team","points":10.0},{"pos":6,"driver":"Kimi Antonelli","team":"Mercedes","points":8.0},{"pos":7,"driver":"Alexander Albon","team":"Williams","points":6.0},{"pos":8,"driver":"Oliver Bearman","team":"Haas F1 Team","points":4.0},{"pos":9,"driver":"Lance Stroll","team":"Aston Martin","points":2.0},{"pos":10,"driver":"Carlos Sainz","team":"Williams","points":1.0}]},{"round":3,"name":"Japanese Grand Prix","hasResults":true,"winner":"Max Verstappen","team":"Red Bull Racing","winnerTime":"1:22:06.983","results":[{"pos":1,"driver":"Max Verstappen","team":"Red Bull Racing","points":25.0},{"pos":2,"driver":"Lando Norris","team":"McLaren","points":18.0},{"pos":3,"driver":"Oscar Piastri","team":"McLaren","points":15.0},{"pos":4,"driver":"Charles Leclerc","team":"Ferrari","points":12.0},{"pos":5,"driver":"George Russell","team":"Mercedes","points":10.0},{"pos":6,"driver":"Kimi Antonelli","team":"Mercedes","points":8.0},{"pos":7,"driver":"Lewis Hamilton","team":"Ferrari","points":6.0},{"pos":8,"driver":"Isack Hadjar","team":"Racing Bulls","points":4.0},{"pos":9,"driver":"Alexander Albon","team":"Williams","points":2.0},{"pos":10,"driver":"Oliver Bearman","team":"Haas F1 Team","points":1.0}]},{"round":4,"name":"Bahrain Grand Prix","hasResults":true,"winner":"Oscar Piastri","team":"McLaren","winnerTime":"1:35:39.435","results":[{"pos":1,"driver":"Oscar Piastri","team":"McLaren","points":25.0},{"pos":2,"driver":"George Russell","team":"Mercedes","points":18.0},{"pos":3,"driver":"Lando Norris","team":"McLaren","points":15.0},{"pos":4,"driver":"Charles Leclerc","team":"Ferrari","points":12.0},{"pos":5,"driver":"Lewis Hamilton","team":"Ferrari","points":10.0},{"pos":6,"driver":"Max Verstappen","team":"Red Bull Racing","points":8.0},{"pos":7,"driver":"Pierre Gasly","team":"Alpine","points":6.0},{"pos":8,"driver":"Esteban Ocon","team":"Haas F1 Team","points":4.0},{"pos":9,"driver":"Yuki Tsunoda","team":"Red Bull Racing","points":2.0},{"pos":10,"driver":"Oliver Bearman","team":"Haas F1 Team","points":1.0}]},{"round":5,"name":"Saudi Arabian Grand Prix","hasResults":true,"winner":"Oscar Piastri","team":"McLaren","winnerTime":"1:21:06.758","results":[{"pos":1,"driver":"Oscar Piastri","team":"McLaren","points":25.0},{"pos":2,"driver":"Max Verstappen","team":"Red Bull Racing","points":18.0},{"pos":3,"driver":"Charles Leclerc","team":"Ferrari","points":15.0},{"pos":4,"driver":"Lando Norris","team":"McLaren","points":12.0},{"pos":5,"driver":"George Russell","team":"Mercedes","points":10.0},{"pos":6,"driver":"Kimi Antonelli","team":"Mercedes","points":8.0},{"pos":7,"driver":"Lewis Hamilton","team":"Ferrari","points":6.0},{"pos":8,"driver":"Carlos Sainz","team":"Williams","points":4.0},{"pos":9,"driver":"Alexander Albon","team":"Williams","points":2.0},{"pos":10,"driver":"Isack Hadjar","team":"Racing Bulls","points":1.0}]},{"round":6,"name":"Miami Grand Prix","hasResults":true,"winner":"Oscar Piastri","team":"McLaren","winnerTime":"1:28:51.587","results":[{"pos":1,"driver":"Oscar Piastri","team":"McLaren","points":25.0},{"pos":2,"driver":"Lando Norris","team":"McLaren","points":18.0},{"pos":3,"driver":"George Russell","team":"Mercedes","points":15.0},{"pos":4,"driver":"Max Verstappen","team":"Red Bull Racing","points":12.0},{"pos":5,"driver":"Alexander Albon","team":"Williams","points":10.0},{"pos":6,"driver":"Kimi Antonelli","team":"Mercedes","points":8.0},{"pos":7,"driver":"Charles Leclerc","team":"Ferrari","points":6.0},{"pos":8,"driver":"Lewis Hamilton","team":"Ferrari","points":4.0},{"pos":9,"driver":"Carlos Sainz","team":"Williams","points":2.0},{"pos":10,"driver":"Yuki Tsunoda","team":"Red Bull Racing","points":1.0}]},{"round":7,"name":"Emilia Romagna Grand Prix","hasResults":true,"winner":"Max Verstappen","team":"Red Bull Racing","winnerTime":"1:31:33.199","results":[{"pos":1,"driver":"Max Verstappen","team":"Red Bull Racing","points":25.0},{"pos":2,"driver":"Lando Norris","team":"McLaren","points":18.0},{"pos":3,"driver":"Oscar Piastri","team":"McLaren","points":15.0},{"pos":4,"driver":"Lewis Hamilton","team":"Ferrari","points":12.0},{"pos":5,"driver":"Alexander Albon","team":"Williams","points":10.0},{"pos":6,"driver":"Charles Leclerc","team":"Ferrari","points":8.0},{"pos":7,"driver":"George Russell","team":"Mercedes","points":6.0},{"pos":8,"driver":"Carlos Sainz","team":"Williams","points":4.0},{"pos":9,"driver":"Isack Hadjar","team":"Racing Bulls","points":2.0},{"pos":10,"driver":"Yuki Tsunoda","team":"Red Bull Racing","points":1.0}]},{"round":8,"name":"Monaco Grand Prix","hasResults":true,"winner":"Lando Norris","team":"McLaren","winnerTime":"1:40:33.843","results":[{"pos":1,"driver":"Lando Norris","team":"McLaren","points":25.0},{"pos":2,"driver":"Charles Leclerc","team":"Ferrari","points":18.0},{"pos":3,"driver":"Oscar Piastri","team":"McLaren","points":15.0},{"pos":4,"driver":"Max Verstappen","team":"Red Bull Racing","points":12.0},{"pos":5,"driver":"Lewis Hamilton","team":"Ferrari","points":10.0},{"pos":6,"driver":"Isack Hadjar","team":"Racing Bulls","points":8.0},{"pos":7,"driver":"Esteban Ocon","team":"Haas F1 Team","points":6.0},{"pos":8,"driver":"Liam Lawson","team":"Racing Bulls","points":4.0},{"pos":9,"driver":"Alexander Albon","team":"Williams","points":2.0},{"pos":10,"driver":"Carlos Sainz","team":"Williams","points":1.0}]},{"round":9,"name":"Spanish Grand Prix","hasResults":true,"winner":"Oscar Piastri","team":"McLaren","winnerTime":"1:32:57.375","results":[{"pos":1,"driver":"Oscar Piastri","team":"McLaren","points":25.0},{"pos":2,"driver":"Lando Norris","team":"McLaren","points":18.0},{"pos":3,"driver":"Charles Leclerc","team":"Ferrari","points":15.0},{"pos":4,"driver":"George Russell","team":"Mercedes","points":12.0},{"pos":5,"driver":"Nico Hulkenberg","team":"Kick Sauber","points":10.0},{"pos":6,"driver":"Lewis Hamilton","team":"Ferrari","points":8.0},{"pos":7,"driver":"Isack Hadjar","team":"Racing Bulls","points":6.0},{"pos":8,"driver":"Pierre Gasly","team":"Alpine","points":4.0},{"pos":9,"driver":"Fernando Alonso","team":"Aston Martin","points":2.0},{"pos":10,"driver":"Max Verstappen","team":"Red Bull Racing","points":1.0}]},{"round":10,"name":"Canadian Grand Prix","hasResults":true,"winner":"George Russell","team":"Mercedes","winnerTime":"1:31:52.688","results":[{"pos":1,"driver":"George Russell","team":"Mercedes","points":25.0},{"pos":2,"driver":"Max Verstappen","team":"Red Bull Racing","points":18.0},{"pos":3,"driver":"Kimi Antonelli","team":"Mercedes","points":15.0},{"pos":4,"driver":"Oscar Piastri","team":"McLaren","points":12.0},{"pos":5,"driver":"Charles Leclerc","team":"Ferrari","points":10.0},{"pos":6,"driver":"Lewis Hamilton","team":"Ferrari","points":8.0},{"pos":7,"driver":"Fernando Alonso","team":"Aston Martin","points":6.0},{"pos":8,"driver":"Nico Hulkenberg","team":"Kick Sauber","points":4.0},{"pos":9,"driver":"Esteban Ocon","team":"Haas F1 Team","points":2.0},{"pos":10,"driver":"Carlos Sainz","team":"Williams","points":1.0}]},{"round":11,"name":"Austrian Grand Prix","hasResults":true,"winner":"Lando Norris","team":"McLaren","winnerTime":"1:23:47.693","results":[{"pos":1,"driver":"Lando Norris","team":"McLaren","points":25.0},{"pos":2,"driver":"Oscar Piastri","team":"McLaren","points":18.0},{"pos":3,"driver":"Charles Leclerc","team":"Ferrari","points":15.0},{"pos":4,"driver":"Lewis Hamilton","team":"Ferrari","points":12.0},{"pos":5,"driver":"George Russell","team":"Mercedes","points":10.0},{"pos":6,"driver":"Liam Lawson","team":"Racing Bulls","points":8.0},{"pos":7,"driver":"Fernando Alonso","team":"Aston Martin","points":6.0},{"pos":8,"driver":"Gabriel Bortoleto","team":"Kick Sauber","points":4.0},{"pos":9,"driver":"Nico Hulkenberg","team":"Kick Sauber","points":2.0},{"pos":10,"driver":"Esteban Ocon","team":"Haas F1 Team","points":1.0}]},{"round":12,"name":"British Grand Prix","hasResults":true,"winner":"Lando Norris","team":"McLaren","winnerTime":"1:37:15.735","results":[{"pos":1,"driver":"Lando Norris","team":"McLaren","points":25.0},{"pos":2,"driver":"Oscar Piastri","team":"McLaren","points":18.0},{"pos":3,"driver":"Nico Hulkenberg","team":"Kick Sauber","points":15.0},{"pos":4,"driver":"Lewis Hamilton","team":"Ferrari","points":12.0},{"pos":5,"driver":"Max Verstappen","team":"Red Bull Racing","points":10.0},{"pos":6,"driver":"Pierre Gasly","team":"Alpine","points":8.0},{"pos":7,"driver":"Lance Stroll","team":"Aston Martin","points":6.0},{"pos":8,"driver":"Alexander Albon","team":"Williams","points":4.0},{"pos":9,"driver":"Fernando Alonso","team":"Aston Martin","points":2.0},{"pos":10,"driver":"George Russell","team":"Mercedes","points":1.0}]},{"round":13,"name":"Belgian Grand Prix","hasResults":true,"winner":"Oscar Piastri","team":"McLaren","winnerTime":"1:25:22.601","results":[{"pos":1,"driver":"Oscar Piastri","team":"McLaren","points":25.0},{"pos":2,"driver":"Lando Norris","team":"McLaren","points":18.0},{"pos":3,"driver":"Charles Leclerc","team":"Ferrari","points":15.0},{"pos":4,"driver":"Max Verstappen","team":"Red Bull Racing","points":12.0},{"pos":5,"driver":"George Russell","team":"Mercedes","points":10.0},{"pos":6,"driver":"Alexander Albon","team":"Williams","points":8.0},{"pos":7,"driver":"Lewis Hamilton","team":"Ferrari","points":6.0},{"pos":8,"driver":"Liam Lawson","team":"Racing Bulls","points":4.0},{"pos":9,"driver":"Gabriel Bortoleto","team":"Kick Sauber","points":2.0},{"pos":10,"driver":"Pierre Gasly","team":"Alpine","points":1.0}]},{"round":14,"name":"Hungarian Grand Prix","hasResults":true,"winner":"Lando Norris","team":"McLaren","winnerTime":"1:35:21.231","results":[{"pos":1,"driver":"Lando Norris","team":"McLaren","points":25.0},{"pos":2,"driver":"Oscar Piastri","team":"McLaren","points":18.0},{"pos":3,"driver":"George Russell","team":"Mercedes","points":15.0},{"pos":4,"driver":"Charles Leclerc","team":"Ferrari","points":12.0},{"pos":5,"driver":"Fernando Alonso","team":"Aston Martin","points":10.0},{"pos":6,"driver":"Gabriel Bortoleto","team":"Kick Sauber","points":8.0},{"pos":7,"driver":"Lance Stroll","team":"Aston Martin","points":6.0},{"pos":8,"driver":"Liam Lawson","team":"Racing Bulls","points":4.0},{"pos":9,"driver":"Max Verstappen","team":"Red Bull Racing","points":2.0},{"pos":10,"driver":"Kimi Antonelli","team":"Mercedes","points":1.0}]},{"round":15,"name":"Dutch Grand Prix","hasResults":true,"winner":"Oscar Piastri","team":"McLaren","winnerTime":"1:38:29.849","results":[{"pos":1,"driver":"Oscar Piastri","team":"McLaren","points":25.0},{"pos":2,"driver":"Max Verstappen","team":"Red Bull Racing","points":18.0},{"pos":3,"driver":"Isack Hadjar","team":"Racing Bulls","points":15.0},{"pos":4,"driver":"George Russell","team":"Mercedes","points":12.0},{"pos":5,"driver":"Alexander Albon","team":"Williams","points":10.0},{"pos":6,"driver":"Oliver Bearman","team":"Haas F1 Team","points":8.0},{"pos":7,"driver":"Lance Stroll","team":"Aston Martin","points":6.0},{"pos":8,"driver":"Fernando Alonso","team":"Aston Martin","points":4.0},{"pos":9,"driver":"Yuki Tsunoda","team":"Red Bull Racing","points":2.0},{"pos":10,"driver":"Esteban Ocon","team":"Haas F1 Team","points":1.0}]},{"round":16,"name":"Italian Grand Prix","hasResults":true,"winner":"Max Verstappen","team":"Red Bull Racing","winnerTime":"1:13:24.325","results":[{"pos":1,"driver":"Max Verstappen","team":"Red Bull Racing","points":25.0},{"pos":2,"driver":"Lando Norris","team":"McLaren","points":18.0},{"pos":3,"driver":"Oscar Piastri","team":"McLaren","points":15.0},{"pos":4,"driver":"Charles Leclerc","team":"Ferrari","points":12.0},{"pos":5,"driver":"George Russell","team":"Mercedes","points":10.0},{"pos":6,"driver":"Lewis Hamilton","team":"Ferrari","points":8.0},{"pos":7,"driver":"Alexander Albon","team":"Williams","points":6.0},{"pos":8,"driver":"Gabriel Bortoleto","team":"Kick Sauber","points":4.0},{"pos":9,"driver":"Kimi Antonelli","team":"Mercedes","points":2.0},{"pos":10,"driver":"Isack Hadjar","team":"Racing Bulls","points":1.0}]},{"round":17,"name":"Azerbaijan Grand Prix","hasResults":true,"winner":"Max Verstappen","team":"Red Bull Racing","winnerTime":"1:33:26.408","results":[{"pos":1,"driver":"Max Verstappen","team":"Red Bull Racing","points":25.0},{"pos":2,"driver":"George Russell","team":"Mercedes","points":18.0},{"pos":3,"driver":"Carlos Sainz","team":"Williams","points":15.0},{"pos":4,"driver":"Kimi Antonelli","team":"Mercedes","points":12.0},{"pos":5,"driver":"Liam Lawson","team":"Racing Bulls","points":10.0},{"pos":6,"driver":"Yuki Tsunoda","team":"Red Bull Racing","points":8.0},{"pos":7,"driver":"Lando Norris","team":"McLaren","points":6.0},{"pos":8,"driver":"Lewis Hamilton","team":"Ferrari","points":4.0},{"pos":9,"driver":"Charles Leclerc","team":"Ferrari","points":2.0},{"pos":10,"driver":"Isack Hadjar","team":"Racing Bulls","points":1.0}]},{"round":18,"name":"Singapore Grand Prix","hasResults":true,"winner":"George Russell","team":"Mercedes","winnerTime":"1:40:22.367","results":[{"pos":1,"driver":"George Russell","team":"Mercedes","points":25.0},{"pos":2,"driver":"Max Verstappen","team":"Red Bull Racing","points":18.0},{"pos":3,"driver":"Lando Norris","team":"McLaren","points":15.0},{"pos":4,"driver":"Oscar Piastri","team":"McLaren","points":12.0},{"pos":5,"driver":"Kimi Antonelli","team":"Mercedes","points":10.0},{"pos":6,"driver":"Charles Leclerc","team":"Ferrari","points":8.0},{"pos":7,"driver":"Fernando Alonso","team":"Aston Martin","points":6.0},{"pos":8,"driver":"Lewis Hamilton","team":"Ferrari","points":4.0},{"pos":9,"driver":"Oliver Bearman","team":"Haas F1 Team","points":2.0},{"pos":10,"driver":"Carlos Sainz","team":"Williams","points":1.0}]},{"round":19,"name":"United States Grand Prix","hasResults":true,"winner":"Max Verstappen","team":"Red Bull Racing","winnerTime":"1:34:00.161","results":[{"pos":1,"driver":"Max Verstappen","team":"Red Bull Racing","points":25.0},{"pos":2,"driver":"Lando Norris","team":"McLaren","points":18.0},{"pos":3,"driver":"Charles Leclerc","team":"Ferrari","points":15.0},{"pos":4,"driver":"Lewis Hamilton","team":"Ferrari","points":12.0},{"pos":5,"driver":"Oscar Piastri","team":"McLaren","points":10.0},{"pos":6,"driver":"George Russell","team":"Mercedes","points":8.0},{"pos":7,"driver":"Yuki Tsunoda","team":"Red Bull Racing","points":6.0},{"pos":8,"driver":"Nico Hulkenberg","team":"Kick Sauber","points":4.0},{"pos":9,"driver":"Oliver Bearman","team":"Haas F1 Team","points":2.0},{"pos":10,"driver":"Fernando Alonso","team":"Aston Martin","points":1.0}]},{"round":20,"name":"Mexico City Grand Prix","hasResults":true,"winner":"Lando Norris","team":"McLaren","winnerTime":"1:37:58.574","results":[{"pos":1,"driver":"Lando Norris","team":"McLaren","points":25.0},{"pos":2,"driver":"Charles Leclerc","team":"Ferrari","points":18.0},{"pos":3,"driver":"Max Verstappen","team":"Red Bull Racing","points":15.0},{"pos":4,"driver":"Oliver Bearman","team":"Haas F1 Team","points":12.0},{"pos":5,"driver":"Oscar Piastri","team":"McLaren","points":10.0},{"pos":6,"driver":"Kimi Antonelli","team":"Mercedes","points":8.0},{"pos":7,"driver":"George Russell","team":"Mercedes","points":6.0},{"pos":8,"driver":"Lewis Hamilton","team":"Ferrari","points":4.0},{"pos":9,"driver":"Esteban Ocon","team":"Haas F1 Team","points":2.0},{"pos":10,"driver":"Gabriel Bortoleto","team":"Kick Sauber","points":1.0}]},{"round":21,"name":"S\u00e3o Paulo Grand Prix","hasResults":false},{"round":22,"name":"Las Vegas Grand Prix","hasResults":true,"winner":"Max Verstappen","team":"Red Bull Racing","winnerTime":"1:21:08.429","results":[{"pos":1,"driver":"Max Verstappen","team":"Red Bull Racing","points":25.0},{"pos":2,"driver":"George Russell","team":"Mercedes","points":18.0},{"pos":3,"driver":"Kimi Antonelli","team":"Mercedes","points":15.0},{"pos":4,"driver":"Charles Leclerc","team":"Ferrari","points":12.0},{"pos":5,"driver":"Carlos Sainz","team":"Williams","points":10.0},{"pos":6,"driver":"Isack Hadjar","team":"Racing Bulls","points":8.0},{"pos":7,"driver":"Nico Hulkenberg","team":"Kick Sauber","points":6.0},{"pos":8,"driver":"Lewis Hamilton","team":"Ferrari","points":4.0},{"pos":9,"driver":"Esteban Ocon","team":"Haas F1 Team","points":2.0},{"pos":10,"driver":"Oliver Bearman","team":"Haas F1 Team","points":1.0}]},{"round":23,"name":"Qatar Grand Prix","hasResults":true,"winner":"Max Verstappen","team":"Red Bull Racing","winnerTime":"1:24:38.241","results":[{"pos":1,"driver":"Max Verstappen","team":"Red Bull Racing","points":25.0},{"pos":2,"driver":"Oscar Piastri","team":"McLaren","points":18.0},{"pos":3,"driver":"Carlos Sainz","team":"Williams","points":15.0},{"pos":4,"driver":"Lando Norris","team":"McLaren","points":12.0},{"pos":5,"driver":"Kimi Antonelli","team":"Mercedes","points":10.0},{"pos":6,"driver":"George Russell","team":"Mercedes","points":8.0},{"pos":7,"driver":"Fernando Alonso","team":"Aston Martin","points":6.0},{"pos":8,"driver":"Charles Leclerc","team":"Ferrari","points":4.0},{"pos":9,"driver":"Liam Lawson","team":"Racing Bulls","points":2.0},{"pos":10,"driver":"Yuki Tsunoda","team":"Red Bull Racing","points":1.0}]},{"round":24,"name":"Abu Dhabi Grand Prix","hasResults":true,"winner":"Max Verstappen","team":"Red Bull Racing","winnerTime":"1:26:07.469","results":[{"pos":1,"driver":"Max Verstappen","team":"Red Bull Racing","points":25.0},{"pos":2,"driver":"Oscar Piastri","team":"McLaren","points":18.0},{"pos":3,"driver":"Lando Norris","team":"McLaren","points":15.0},{"pos":4,"driver":"Charles Leclerc","team":"Ferrari","points":12.0},{"pos":5,"driver":"George Russell","team":"Mercedes","points":10.0},{"pos":6,"driver":"Fernando Alonso","team":"Aston Martin","points":8.0},{"pos":7,"driver":"Esteban Ocon","team":"Haas F1 Team","points":6.0},{"pos":8,"driver":"Lewis Hamilton","team":"Ferrari","points":4.0},{"pos":9,"driver":"Nico Hulkenberg","team":"Kick Sauber","points":2.0},{"pos":10,"driver":"Lance Stroll","team":"Aston Martin","points":1.0}]}]}'''

ORANGE = "#FF630F"
TEAM_COLORS = {
    "McLaren": "#FF8000", "Red Bull": "#3671C6", "Mercedes": "#27F4D2",
    "Ferrari": "#E80020", "Williams": "#64C4FF", "Aston Martin": "#229971",
    "Racing Bulls": "#6692FF", "Kick Sauber": "#52E252", "Haas": "#B6BABD",
    "Alpine": "#FF87BC",
}
DRIVER_COLORS = {
    "Max Verstappen": "#3671C6", "Oscar Piastri": "#FF8000", "Lando Norris": "#FFD08A",
    "George Russell": "#27F4D2", "Charles Leclerc": "#E80020", "Lewis Hamilton": "#FF8A8A",
    "Kimi Antonelli": "#1AA890", "Alexander Albon": "#64C4FF", "Carlos Sainz": "#2A7FB8",
    "Fernando Alonso": "#229971",
}


def team_color(name: str) -> str:
    return next((c for k, c in TEAM_COLORS.items() if k in name), "#888888")


st.markdown(
    """
    <style>
      .stApp {background:#000; color:#fff;}
      h1, h2, h3 {letter-spacing:-0.03em;}
      div[data-testid="stMetricValue"] {font-size:2.4rem; letter-spacing:-0.03em;}
      .block-container {padding-top:2rem; max-width:1300px;}
    </style>
    """,
    unsafe_allow_html=True,
)


data = json.loads(DATA_JSON)
drivers = data["drivers"][:10]
teams = data["teams"]
rounds = data["rounds"]
n_rounds = len(rounds)
with_data = sum(1 for r in rounds if r["hasResults"])
winners = {r["winner"] for r in rounds if r.get("winner")}

# ---------- header ----------
st.markdown("# F1 ’25 Season")
st.caption("Race results, standings and round-by-round analysis. Race points only; sprint points are not included.")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Rounds", n_rounds)
c2.metric("Rounds with data", with_data)
c3.metric("Different winners", len(winners))
c4.metric(f"{teams[0]['team']} race points", int(teams[0]["points"]))

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Title race", "Standings", "Constructors & wins", "Points heatmap", "Race calendar"]
)

# ---------- 1. title race ----------
with tab1:
    st.subheader("The title race")
    names = [d["driver"] for d in drivers]
    picked = st.multiselect("Drivers", names, default=names[:6])
    fig = go.Figure()
    for d in drivers:
        if d["driver"] in picked:
            fig.add_trace(go.Scatter(
                x=[f"R{i}" for i in range(1, len(d["cumulative"]) + 1)], y=d["cumulative"],
                mode="lines", name=d["driver"].split()[-1],
                line=dict(width=3, color=DRIVER_COLORS.get(d["driver"], "#888")),
            ))
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      hovermode="x unified", height=480, yaxis_title="Cumulative race points",
                      legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig, width="stretch")
    gap = drivers[0]["points"] - drivers[2]["points"]
    st.write(f"**{drivers[0]['driver']}** finished on **{drivers[0]['points']}** race points, "
             f"only **{gap}** ahead of {drivers[2]['driver']} in third.")

# ---------- 2. standings ----------
with tab2:
    st.subheader("Driver standings (race points)")
    df = pd.DataFrame(drivers)[["driver", "team", "wins", "points"]]
    df.insert(0, "Pos", range(1, len(df) + 1))
    df.columns = ["Pos", "Driver", "Team", "Wins", "Points"]
    st.dataframe(
        df, hide_index=True, width="stretch",
        column_config={"Points": st.column_config.ProgressColumn(
            "Points", min_value=0, max_value=int(df["Points"].max()), format="%d")},
    )

# ---------- 3. constructors & wins ----------
with tab3:
    st.subheader("Who scored the points")
    left, right = st.columns([1.4, 1])
    tdf = pd.DataFrame(teams).sort_values("points")
    bar = px.bar(tdf, x="points", y="team", orientation="h", text="points",
                 color="team", color_discrete_map={t: team_color(t) for t in tdf["team"]})
    bar.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      showlegend=False, height=460, yaxis_title=None, xaxis_title="Constructor points")
    left.plotly_chart(bar, width="stretch")
    wins = pd.DataFrame([d for d in drivers if d["wins"] > 0])
    pie = px.pie(wins, names="driver", values="wins", hole=0.55,
                 color="driver", color_discrete_map=DRIVER_COLORS)
    pie.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", height=460,
                      title="Race wins by driver")
    right.plotly_chart(pie, width="stretch")
    total = sum(t["points"] for t in teams)
    st.write(f"**{teams[0]['team']}** scored **{round(teams[0]['points'] / total * 100)}%** of all constructor points.")

# ---------- 4. heatmap ----------
with tab4:
    st.subheader("Points scored, round by round")
    top = [d["driver"] for d in drivers]
    z = []
    for name in top:
        row = []
        for r in rounds:
            if not r["hasResults"]:
                row.append(None)
            else:
                row.append(next((int(x["points"]) for x in r["results"] if x["driver"] == name), 0))
        z.append(row)
    hm = px.imshow(z, x=[f"R{r['round']}" for r in rounds], y=[n.split()[-1] for n in top],
                   color_continuous_scale=["#141414", ORANGE], zmin=0, zmax=25, aspect="auto", text_auto=True)
    hm.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", height=460, coloraxis_showscale=False)
    st.plotly_chart(hm, width="stretch")
    st.caption("Blank squares are rounds with no data.")

# ---------- 5. calendar ----------
with tab5:
    st.subheader("Race calendar")
    pick = st.selectbox("Filter by race winner", ["All"] + sorted(winners))
    rows = [
        {"Round": r["round"], "Grand Prix": r["name"], "Winner": r.get("winner", "No data"),
         "Team": r.get("team", "—"), "Time": r.get("winnerTime", "")}
        for r in rounds if pick == "All" or r.get("winner") == pick
    ]
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
    chosen = st.selectbox("Open a round's top 10", [r["name"] for r in rounds if r["hasResults"]])
    r = next(x for x in rounds if x["name"] == chosen)
    st.dataframe(
        pd.DataFrame([{"Pos": x["pos"], "Driver": x["driver"], "Team": x["team"], "Points": int(x["points"])}
                      for x in r["results"][:10]]),
        hide_index=True, width="stretch",
    )

st.caption("Source: f1-2025.json (race points only). The São Paulo Grand Prix has no data in the file.")
