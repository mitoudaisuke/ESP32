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
#st.title("WHOLE GARMENT©")
st.markdown("# **WHOLE GARMENT©**")
st.markdown("### **MACHINE 01**")

# 平滑化（移動平均）
df["smoothed_value"] = df["value"].rolling(window=10, center=True).mean()

# 最新の10分間のデータのみ抽出
latest_time = df["timestamp"].max()
df_recent = df[df["timestamp"] >= latest_time - pd.Timedelta(minutes=10)]

# グラフ描画（2つのサブプロット）
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
fig.subplots_adjust(hspace=0.5)  # 2つのグラフの間隔を広げる（値を調整）

## **全体のトレンド**
ax1.scatter(df["timestamp"], df["value"], color="black", alpha=0.3, s=1, label="line A(raw)")
ax1.plot(df["timestamp"], df["smoothed_value"], linewidth=1, color="orange",label="line A(average)")
ax1.plot(0, linewidth=1, color="orange",label="line B(average)")
ax1.set_ylabel("gf", fontsize=14, fontweight="bold")
ax1.set_title("LONG TREND", fontsize=14, fontweight="bold")
ax1.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)
ax1.legend()

## **最新10分間の拡大版**
ax2.scatter(df_recent["timestamp"], df_recent["value"], color="black", alpha=0.3, s=2, label="line A(raw)")
ax2.plot(df_recent["timestamp"], df_recent["smoothed_value"], linewidth=1, color="orange",label="line A(average)")
ax2.set_ylabel("gf", fontsize=14, fontweight="bold")
ax2.set_title("SHORT TREND", fontsize=14, fontweight="bold")
ax2.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)
ax2.legend()

# JSTタイムゾーンを明示的に設定
jst = pytz.timezone('Asia/Tokyo')
date_form = DateFormatter("%-H:%M", tz=jst)
ax1.xaxis.set_major_formatter(date_form)
ax2.xaxis.set_major_formatter(date_form)

# Streamlit で表示
st.pyplot(fig)







st.markdown("### **MACHINE 02**")
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
fig.subplots_adjust(hspace=0.5)  # 2つのグラフの間隔を広げる（値を調整）
st.pyplot(fig)


st.markdown("### **MACHINE 03**")
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
fig.subplots_adjust(hspace=0.5)  # 2つのグラフの間隔を広げる（値を調整）
st.pyplot(fig)

st.markdown("### **MACHINE 04**")
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
fig.subplots_adjust(hspace=0.5)  # 2つのグラフの間隔を広げる（値を調整）
st.pyplot(fig)