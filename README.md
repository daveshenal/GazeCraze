# 🧠 GazeCraze - Real-Time Concentration Detection Using Face Landmarks

**GazeCraze** is a modular Python application that uses computer vision and facial landmark detection to analyze user concentration in real time. It leverages MediaPipe Face Mesh, OpenCV, and head/eye tracking techniques to infer gaze alignment and focus level from a webcam feed, or from image and video files.

## 🚀 Features

- 🔍 **Face Mesh Tracking** via MediaPipe
- 👁️ **Gaze and Iris Alignment** for focus estimation
- 🧠 **Head Pose Analysis** to determine attention direction
- 🖼️ **Image & Video Labeling** - batch-annotate files with concentration status
- 📐 **Resolution-aware Overlays** - label size and position scale with frame dimensions
- 🧪 **Modular Testable Architecture**
- 📈 **Real-time Visualization & Display**

## 🏷️ Detection Labels

Each frame gets a top-level verdict plus a reason in parentheses.

| Verdict              | Color | Description                  |
| -------------------- | ----- | ---------------------------- |
| **Concentrated**     | Green | User is considered focused   |
| **Not Concentrated** | Red   | User is considered unfocused |
| **No Face Detected** | Red   | No face found in the frame   |

**Concentrated reasons:** `Eyes on screen`, `Head: Left Turn`, `Head: Right Turn`

**Not concentrated reasons:** `Eyes Closed`, `Face Tilted`, `Looking Left`, `Looking Right`, `Eyes on left`, `Eyes on right`, `Invalid Eye Measurements`, `Detection Error`

A confidence score is shown when available (not for `Eyes Closed`, `Invalid Eye Measurements`, or `No Face Detected`).

## 📸 Sample Dataset

Labeled examples below were generated with [`src/process_media.py`](src/process_media.py). Direction labels use the **subject's perspective** - e.g. `Looking Right` means the person looked to their own right.

<table>
  <tr>
    <th colspan="2">✅ Concentrated - Eyes on screen</th>
  </tr>
  <tr>
    <td width="50%"><img src="dataset/image_samples_labeled/concentrated_eyes_on_screen_1_labeled.jpg" width="100%" style="object-fit: cover;"/></td>
    <td width="50%"><img src="dataset/image_samples_labeled/concentrated_eyes_on_screen_2_labeled.jpg" width="100%"  style="object-fit: cover;"/></td>
  </tr>

  <tr>
    <th colspan="2">✅ Concentrated - Head: Left Turn</th>
  </tr>
  <tr>
    <td width="50%"><img src="dataset/image_samples_labeled/concentrated_head_left_turn_1_labeled.jpg" width="100%"  style="object-fit: cover;"/></td>
    <td width="50%"><img src="dataset/image_samples_labeled/concentrated_head_left_turn_2_labeled.jpg" width="100%"  style="object-fit: cover;"/></td>
  </tr>

  <tr>
    <th colspan="2">✅ Concentrated - Head: Right Turn</th>
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

> 📷 Sample images sourced from [Unsplash](https://unsplash.com/) for demonstration purposes only. Not used for model training.

## 📂 Project Structure

```
GazeCraze/
├── dataset/                          # Sample images and labeled outputs
├── notebooks/
├── src/
│   ├── main.py                       # Live webcam entry point
│   ├── process_media.py              # Image/video labeling script
│   ├── concentration_detector.py
│   └── modules/
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
│   └── test_*.py
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

### Live webcam

```bash
python -m src.main
```

Make sure your webcam is connected. A window opens with real-time concentration detection. Press **`q`** to quit or **`r`** to reset the smoothing history.

### Image or video labeling

Annotate a file and save the result with status labels burned in:

```bash
# Image (output: photo_labeled.jpg in the same folder)
python -m src.process_media path/to/photo.jpg

# Video with custom output path
python -m src.process_media path/to/video.mp4 -o path/to/output.mp4

# Mirror output like the live webcam view
python -m src.process_media path/to/video.mp4 --mirror
```

Supported formats: `.jpg`, `.png`, `.bmp`, `.webp`, `.tif`, `.mp4`, `.avi`, `.mov`, `.mkv`, and others.

### Tests

```bash
python tests/run_tests.py
```

## 📊 Notebooks

Explore the logic and debugging tools via Jupyter notebooks in the `notebooks/` directory:

- [`face_mesh.ipynb`](notebooks/face_mesh.ipynb) – Debug and understand MediaPipe's face mesh outputs.
- [`eye_indexes.ipynb`](notebooks/eye_indexes.ipynb) – Visualize eye region indices and landmark positions.

These notebooks help visualize facial landmarks and debug model behavior effectively.
