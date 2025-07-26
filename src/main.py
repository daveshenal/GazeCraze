import cv2
import mediapipe as mp

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    static_image_mode=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Indices for key landmarks on the iris and eye corners
left_iris_index = 468
left_eye_inner = 133
left_eye_outer = 33
left_eye_top = 159
left_eye_bottom = 145

right_iris_index = 473
right_eye_inner = 362
right_eye_outer = 263
right_eye_top = 386
right_eye_bottom = 374

# Function to display labeled landmarks
def display_landmarks(frame, face_landmarks, frame_width, frame_height):

    # Define key points with names
    key_points = (
        right_iris_index, # Right Iris Center
        left_iris_index,  # Left Iris Center
        right_eye_inner,  # Right Eye Inner
        right_eye_outer,  # Right Eye Outer
        left_eye_inner,   # Left Eye Inner
        left_eye_outer,   # Left Eye Outer
    )
    
    # Draw and label each key point
    for index in key_points:
        x = int(face_landmarks.landmark[index].x * frame_width)
        y = int(face_landmarks.landmark[index].y * frame_height)
        cv2.circle(frame, (x, y), 3, (0, 255, 255), -1)

# Start video capture
cap = cv2.VideoCapture(0)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Mirror effect for better visualization
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)

    # If landmarks are detected, calculate gaze and head position
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
     
            display_landmarks(frame, face_landmarks, frame_width, frame_height)

    # Show the frame
    cv2.imshow('Eyeball & Head Pose Detection', frame)

    # Exit on pressing 'q'
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
face_mesh.close()
cv2.destroyAllWindows()