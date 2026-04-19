![GitHub stars](https://img.shields.io/github/stars/smeshar/LapTimeAnalysis?style=flat-square)
![GitHub all releases](https://img.shields.io/github/downloads/smeshar/LapTimeAnalysis/total?style=flat-square)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight PyQt application designed for simracers to analyze and visualize lap time telemetry from `.consumption` files. The tool filters out invalid or excessively slow laps, tracks Personal Best (PB) evolution, and maps out overall pace trends.

<p align="center">
  <img src="assets/Autodromo Enzo e Dino Ferrari - Hyper.png" width="1000">
</p>

## Features

* Minimalistic UI without unnecessary clutter.
* Dynamic threshold filtering to ignore in-lap/out-lap or crash data.
* Polynomial trend lines for overall pace and PB improvement.
* Automatic graph generation and PNG export to local directory.

## Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/lap-time-analysis.git](https://github.com/yourusername/lap-time-analysis.git)
   cd lap-time-analysis
   ```

## Usage

1. Run the application:

   ```bash
   python main.py
   ```
2. Click **Upload .consumption** file and select your telemetry data.
3. Enter your desired maximum lap time in the **Threshold time** field (e.g., `96.0`).
4. Click **Generate**. The plot will be displayed on screen and automatically saved to the `\plots` folder inside the app directory.

## Contributing

Contributions are welcome. If you find a bug or have a feature request, please open an issue or submit a pull request.

1. Fork the Project

2. Create your Feature Branch (git checkout -b feature/AmazingFeature)

3. Commit your Changes (git commit -m 'Add some AmazingFeature')

4. Push to the Branch (git push origin feature/AmazingFeature)

5. Open a Pull Request

## License

Distributed under the MIT License. See LICENSE for more information.