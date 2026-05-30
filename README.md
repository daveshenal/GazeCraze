# 🧠 GazeCraze - Real-Time Concentration Detection Using Face Landmarks

**GazeCraze** is a modular Python application that uses computer vision and facial landmark detection to analyze user concentration in real-time. It leverages MediaPipe Face Mesh, OpenCV, and head/eye tracking techniques to infer gaze alignment and focus level from webcam video streams.

## 📸 Sample Dataset

<table>
  <tr>
    <th colspan="2">✅ Concentrated - Eyes on screen</th>
  </tr>
  <tr>
    <td width="50%"><img src="dataset/image_samples_labeled/concentrated_eyes_on_screen_1_labeled.jpg" width="100%" style="object-fit: cover;"/></td>
    <td width="50%"><img src="dataset/image_samples_labeled/concentrated_eyes_on_screen_2_labeled.jpg" width="100%"  style="object-fit: cover;"/></td>
  </tr>

  <tr>
    <th colspan="2">✅ Concentrated - Head Left Turn</th>
  </tr>
  <tr>
    <td width="50%"><img src="dataset/image_samples_labeled/concentrated_head_left_turn_1_labeled.jpg" width="100%"  style="object-fit: cover;"/></td>
    <td width="50%"><img src="dataset/image_samples_labeled/concentrated_head_left_turn_2_labeled.jpg" width="100%"  style="object-fit: cover;"/></td>
  </tr>

  <tr>
    <th colspan="2">✅ Concentrated - Head Right Turn</th>
  </tr>
  <tr>
    <td width="50%"><img src="dataset/image_samples_labeled/concentrated_head_right_turn_1_labeled.jpg" width="100%"  style="object-fit: cover;"/></td>
    <td width="50%"><img src="dataset/image_samples_labeled/concentrated_head_right_turn_2_labeled.jpg" width="100%"  style="object-fit: cover;"/></td>
  </tr>

  <tr>
    <th colspan="2">❌ Not Concentrated - Eyes on left</th>
  </tr>
  <tr>
    <td width="50%"><img src="dataset/image_samples_labeled/not_concentrated_eyes_on_left_1_labeled.jpg" width="100%"  style="object-fit: cover;"/></td>
    <td width="50%"><img src="dataset/image_samples_labeled/not_concentrated_eyes_on_left_2_labeled.jpg" width="100%"  style="object-fit: cover;"/></td>
  </tr>

  <tr>
    <th colspan="2">❌ Not Concentrated - Eyes on right</th>
  </tr>
  <tr>
    <td width="50%"><img src="dataset/image_samples_labeled/not_concentrated_eyes_on_right_1_labeled.jpg" width="100%"  style="object-fit: cover;"/></td>
    <td width="50%"><img src="dataset/image_samples_labeled/not_concentrated_eyes_on_right_2_labeled.jpg" width="100%"  style="object-fit: cover;"/></td>
  </tr>

  <tr>
    <th colspan="2">❌ Not Concentrated - Looking Left</th>
  </tr>
  <tr>
    <td width="50%"><img src="dataset/image_samples_labeled/not_concentrated_looking_left_1_labeled.jpg" width="100%"  style="object-fit: cover;"/></td>
    <td width="50%"><img src="dataset/image_samples_labeled/not_concentrated_looking_left_2_labeled.jpg" width="100%"  style="object-fit: cover;"/></td>
  </tr>

  <tr>
    <th colspan="2">❌ Not Concentrated - Looking Right</th>
  </tr>
  <tr>
    <td width="50%"><img src="dataset/image_samples_labeled/not_concentrated_looking_right_1_labeled.jpg" width="100%"  style="object-fit: cover;"/></td>
    <td width="50%"><img src="dataset/image_samples_labeled/not_concentrated_looking_right_2_labeled.jpg" width="100%"  style="object-fit: cover;"/></td>
  </tr>

  <tr>
    <th colspan="2">❌ Not Concentrated - Eyes Closed</th>
  </tr>
  <tr>
    <td width="50%"><img src="dataset/image_samples_labeled/not_concentrated_eyes_closed_1_labeled.jpg" width="100%"  style="object-fit: cover;"/></td>
    <td width="50%"><img src="dataset/image_samples_labeled/not_concentrated_eyes_closed_2_labeled.jpg" width="100%"  style="object-fit: cover;"/></td>
  </tr>

  <tr>
    <th colspan="2">❌ Not Concentrated - Face Tilted</th>
  </tr>
  <tr>
    <td width="50%"><img src="dataset/image_samples_labeled/not_concentrated_face_tilted_1_labeled.jpg" width="100%"  style="object-fit: cover;"/></td>
    <td width="50%"><img src="dataset/image_samples_labeled/not_concentrated_face_tilted_2_labeled.jpg" width="100%"  style="object-fit: cover;"/></td>
  </tr>

  <tr>
    <th colspan="2">🚫 No Face Detected</th>
  </tr>
  <tr>
    <td width="50%"><img src="dataset/image_samples_labeled/no_face_detected_1_labeled.jpg" width="100%"  style="object-fit: cover;"/></td>
    <td width="50%"><img src="dataset/image_samples_labeled/no_face_detected_2_labeled.jpg" width="100%"  style="object-fit: cover;"/></td>
  </tr>
</table>

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
