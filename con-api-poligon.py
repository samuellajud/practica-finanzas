"""
instalo 
pip install polygon-api-client
pip install plotly
pip install pandas 
pip install datetime
"""

from polygon import RESTClient  
import datetime as dt 
import pandas as pd 
import plotly.graph_objects as go 
from plotly.offline import plot
 
# para configurar la api 
polygonAPIkey= "6RWDj6INb9qHfV9n0dCetOQKb568pHCq"
from polygonAPIkey import polygonAPIkey
#polygonAPIkey= "6RWDj6INb9qHfV9n0dCetOQKb568pHCq"

#crear el cliente y autenticar la api key 
cliente = RESTClient(polygonAPIkey)