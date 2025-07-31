# 🧠 GazeCraze - Real-Time Concentration Detection Using Face Landmarks

**GazeCraze** is a modular Python application that uses computer vision and facial landmark detection to analyze user concentration in real-time. It leverages MediaPipe Face Mesh, OpenCV, and head/eye tracking techniques to infer gaze alignment and focus level from webcam video streams.


## 🚀 Features

- 🔍 **Face Mesh Tracking** via MediaPipe
- 👁️ **Gaze and Iris Alignment** for focus estimation
- 🧠 **Head Pose Analysis** to determine attention direction
- 🧪 **Modular Testable Architecture**
- 📈 **Real-time Visualization & Display**


## 📂 Project Structure

```
GazeCraze/
├── notebooks/
├── src/ # Source code
│   ├── main.py # Entry point
│   ├── concentration_detector.py
│   └── modules/ # Modular components
│       ├── face_mesh_processor.py
│       ├── eye_analyzer.py
│       ├── head_pose_analyzer.py
│       ├── concentration_analyzer.py
│       ├── result_smoother.py
│       ├── performance_tracker.py
│       ├── camera_manager.py
│       └── display_manager.py
├── tests/
│   ├── run_tests.py
│   └── test_*.py # Tests for each module
├── utils/
├── requirements.txt
├── .gitignore
└── README.md
```


## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/daveshenal/GazeCraze.git
cd GazeCraze
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 🧪 Running the Application

```bash
python -m src.main
```

Make sure your webcam is connected. A window will open showing real-time concentration detection based on face and gaze tracking.



## 📊 Notebooks

Explore the logic and debugging tools via Jupyter notebooks in the `notebooks/` directory:

- [`face_mesh.ipynb`](notebooks/face_mesh.ipynb) – Debug and understand MediaPipe's face mesh outputs.
- [`eye_indexes.ipynb`](notebooks/eye_indexes.ipynb) – Visualize eye region indices and landmark positions.

These notebooks help visualize facial landmarks and debug model behavior effectively.


## 👤 Author

**Dave Perera**  
_Machine Learning Engineer_

- [🔗 LinkedIn](https://www.linkedin.com/in/davesperera)
- [🔗 Email](daveshenal281@gmail.com)


## 🙏 Acknowledgements

This project is made possible by the following technologies:

- [MediaPipe](https://mediapipe.dev/)
- [OpenCV](https://opencv.org/)
