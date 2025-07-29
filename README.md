# 🧠 GazeCraze - Real-Time Concentration Detection Using Face Landmarks

**GazeCraze** is a modular Python application that uses computer vision and facial landmark detection to analyze user concentration in real-time. It leverages MediaPipe Face Mesh, OpenCV, and head/eye tracking techniques to infer gaze alignment and focus level from webcam video streams.

---

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
│   └── test_*.py # Tests for each module
├── utils/
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Features

- 🔍 **Face Mesh Tracking** via MediaPipe
- 👁️ **Gaze and Iris Alignment** for focus estimation
- 🧠 **Head Pose Analysis** to determine attention direction
- 🧪 **Modular Testable Architecture**
- 📈 **Real-time Visualization & Display**

---

## 📊 Notebooks

Explore the logic and debugging tools via Jupyter notebooks in the `notebooks/` directory:

- [`face_mesh.ipynb`](notebooks/face_mesh.ipynb) – Debug and understand MediaPipe's face mesh outputs.
- [`eye_indexes.ipynb`](notebooks/eye_indexes.ipynb) – Visualize eye region indices and landmark positions.

These notebooks help visualize facial landmarks and debug model behavior effectively.

---
