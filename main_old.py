import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

# 1. Load Data
file_name = "Autodromo Enzo e Dino Ferrari - Hyper.consumption"
df = pd.read_csv(file_name)
df = df.iloc[::-1].reset_index(drop=True)

# 2. Filtering (Valid laps & Faster than 96s)
threshold = 96.0
valid_fast_laps = df[(df["isValidLap"] == 1) & (df["lapTimeLast"] <= threshold)].copy()
valid_fast_laps["session_lap"] = range(1, len(valid_fast_laps) + 1)

x = valid_fast_laps["session_lap"].values
y = valid_fast_laps["lapTimeLast"].values

# --- CALCULATING PB EVOLUTION ---
pb_evolution = valid_fast_laps["lapTimeLast"].cummin().values

# 3. TRENDS
z_all = np.polyfit(x, y, 2)
p_all = np.poly1d(z_all)

z_pb = np.polyfit(x, pb_evolution, 2)
p_pb = np.poly1d(z_pb)

# 4. Plotting
# Увеличили размер фигуры (16x9) и разрешение (dpi)
plt.figure(figsize=(16, 9), dpi=100)

# All Laps
plt.plot(
    x, y, color="#1f77b4", alpha=0.3, linewidth=1, label="All Laps (Pace)", zorder=2
)
plt.scatter(x, y, color="#1f77b4", alpha=0.3, s=25, zorder=2)

# Step-wise PB (Green dashed)
plt.plot(
    x,
    pb_evolution,
    color="green",
    linewidth=1.5,
    linestyle="--",
    label="PB Evolution (Steps)",
    zorder=4,
    drawstyle="steps-post",
)

# Overall Trend (Red dotted)
plt.plot(
    x, p_all(x), color="red", lw=1.5, ls=":", alpha=0.6, label="Overall Pace Trend"
)

# BOLD PURPLE PB TREND
plt.plot(
    x, p_pb(x), color="#9400D3", linewidth=4, label="PB Improvement Trend", zorder=5
)

# --- AXIS SCALING ---
ax = plt.gca()
# Устанавливаем шаг сетки по X равным 2
ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
# Добавляем второстепенную сетку с шагом 1 (тонкие линии без цифр)
ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))

# Formatting
plt.title("Detailed Lap Time Analysis: Imola", fontsize=18, fontweight="bold", pad=20)
plt.xlabel("Lap Sequence Number", fontsize=14)
plt.ylabel("Lap Time (seconds)", fontsize=14)

# Limits
plt.ylim(pb_evolution.min() - 0.4, threshold + 0.1)
plt.xlim(0.5, x.max() + 0.5)

# Grid - делаем её более детальной
plt.grid(True, which="major", linestyle="-", alpha=0.3, zorder=1)
plt.grid(True, which="minor", linestyle=":", alpha=0.15, zorder=1)

plt.legend(loc="upper right", frameon=True, shadow=True, fontsize=12)

plt.tight_layout()
plt.show()

print(f"Session Best Lap: {pb_evolution[-1]:.3f}s")
