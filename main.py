import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from matplotlib.dates import DateFormatter
import pytz

SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1LxsDjDerM2rNYm0UzBRfFCi-izwvLhiOOs457Oj3NCo/gviz/tq?tqx=out:csv"
plt.rcParams['font.family'] = 'Noto Sans JP'
minutes=5#拡大バージョンで何分間を表示するか

import requests

response = requests.get(SPREADSHEET_URL)
csv_data = response.text
print(csv_data)  # CSVの生データを確認