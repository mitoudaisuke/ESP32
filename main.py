import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from matplotlib.dates import DateFormatter
import pytz

SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1LxsDjDerM2rNYm0UzBRfFCi-izwvLhiOOs457Oj3NCo/gviz/tq?tqx=out:csv"
plt.rcParams['font.family'] = 'Noto Sans JP'

def load_data():
    df = pd.read_csv(SPREADSHEET_URL, header=None)
    
    # 1列目のUNIXタイムを datetime に変換（UTCのまま）
    df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0], unit='s')
    times = df.iloc[:, 0].values.astype('datetime64[ns]')  # datetime64 に変換
    num_measurements = df.shape[1] - 1  # 測定値の個数（最初の列以外の列数）
    
    # 0.1秒刻みのオフセットを作成
    offsets = np.arange(num_measurements) * np.timedelta64(100, 'ms')
    
    # 各行の開始時刻にオフセットを加算（ブロードキャスト）
    all_times = times[:, None] + offsets  # shape: (num_rows, num_measurements)
    timestamps = all_times.flatten()  # 2次元配列を1次元に変換

    # 測定値も同様に flatten
    values = df.iloc[:, 1:].to_numpy().flatten()

    # 連続時系列の DataFrame を作成（この時点では UTC）
    new_timeseries_df = pd.DataFrame({'timestamp': timestamps, 'value': values})
    return new_timeseries_df

df = load_data()
st.title("ESP32C6 LOADCELL PLOT")

# グラフ作成
st.subheader("MACHINE 01")

# JST に変換（プロット時のみ）
df["timestamp"] = df["timestamp"].dt.tz_localize('UTC').dt.tz_convert('Asia/Tokyo')

# 平滑化（移動平均）
df["smoothed_value"] = df["value"].rolling(window=10, center=True).mean()

# グラフ描画
fig, ax = plt.subplots()

# ラベルを "test 01" に統一
ax.plot(df["timestamp"], df["smoothed_value"], label="string 01", linewidth=1, alpha=0.75, color="black")

# X軸・Y軸のグリッドを追加
ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)

# 軸ラベルとタイトル
ax.set_ylabel("gf (estimated)", fontsize=12, fontweight="bold")
ax.set_title("TENSION TREND", fontsize=14, fontweight="bold")

# JSTタイムゾーンを明示的に設定
jst = pytz.timezone('Asia/Tokyo')
date_form = DateFormatter("%-H:%M", tz=jst)
ax.xaxis.set_major_formatter(date_form)

# 凡例追加
ax.legend()

st.pyplot(fig)