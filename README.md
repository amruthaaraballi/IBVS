#  IBVS-Based Gate Navigation for ROV

##  Project Overview
This project implements **Image-Based Visual Servoing (IBVS)** for an underwater Remotely Operated Vehicle (ROV) to handle **sparse objects** such as gates.

Traditional depth sensors often fail with sparse structures (e.g., thin rods), so this system prioritizes **vision-based control** using a trained YOLOv8 model.

---

## Objectives
- Detect gates using computer vision
- Compute image-based error
- Generate control commands (vx, vy)
- Align and pass through the gate
- Avoid reliance on unreliable depth sensing

---

## Approach

1. Object Detection
- Model: YOLOv8 (Ultralytics)
- Trained on ~1600 images
- Output: Bounding boxes for gates

2. IBVS Control Logic
- Image center: (cx, cy)
- Gate center: (gx, gy)

Error calculation:
# IBVS-Based Gate Navigation for ROV

## Project Overview
This project implements **Image-Based Visual Servoing (IBVS)** for an underwater Remotely Operated Vehicle (ROV) to handle **sparse objects** such as gates.

Traditional depth sensors often fail with sparse structures (e.g., thin rods), so this system prioritizes **vision-based control** using a trained YOLOv8 model.

---

## Objectives
- Detect gates using computer vision
- Compute image-based error
- Generate control commands (vx, vy)
- Align and pass through the gate
- Avoid reliance on unreliable depth sensing

---

##  Approach

### 1. Object Detection
- Model: YOLOv8 (Ultralytics)
- Trained on ~1600 images
- Output: Bounding boxes for gates

### 2. IBVS Control Logic
- Image center: (cx, cy)
- Gate center: (gx, gy)

Error calculation:
#  IBVS-Based Gate Navigation for ROV

##  Project Overview
This project implements **Image-Based Visual Servoing (IBVS)** for an underwater Remotely Operated Vehicle (ROV) to handle **sparse objects** such as gates.

Traditional depth sensors often fail with sparse structures (e.g., thin rods), so this system prioritizes **vision-based control** using a trained YOLOv8 model.

---

##  Objectives
- Detect gates using computer vision
- Compute image-based error
- Generate control commands (vx, vy)
- Align and pass through the gate
- Avoid reliance on unreliable depth sensing

---

## Approach

### 1. Object Detection
- Model: YOLOv8 (Ultralytics)
- Trained on ~1600 images
- Output: Bounding boxes for gates

### 2. IBVS Control Logic
- Image center: (cx, cy)
- Gate center: (gx, gy)

Error calculation:
ex = gx - cx
ey = gy - cy

Control law:
vx = -k*ex
vy = -k*ey


### 3. Decision Logic
if gate_detected:
    align_to_gate()
    if aligned:
        move_forward()
else:
    search()

Tech Stack:
- Language: Python
- Framework: ROS 2 Humble
- Vision: OpenCV
- AI Model: Ultralytics YOLOv8n
- Backend: PyTorch

### Project Structure
rov_ws/
├── src/
│   ├── detect_gate.py
│   └── ibvs_controller/
├── output/            # Saved result images
├── yolov8n.pt         # Trained model
├── test_model.py
├── README.md

### How to Run:
1. Build workspace:
cd ~/rov_ws
colcon build
source install/setup.bash

2. Run IBVS node
ros2 run ibvs_controller ibvs_node

# Sample output Logs
frame865.jpg → 🎯 ALIGN | vx: -0.482, vy: -0.122
frame1060.jpg → 🚀 FORWARD (Aligned)
frame2604.jpg → 🔍 SEARCHING...

# Ouput Results:
~/rov_ws/output/
- Each image contains:
 - Bounding boxes (gate detection)
 - Center points (images & objects)
 - Alignment visualization

### Results
- High detection accuracy (mAP~0.99)
- Stable IBVS control behavior
- Coreect alignment with gate center
- Forward motion triggered when aligned

### Future Work
- Integrate with real-time camera feed
- Add MAVROS for real ROV control
- Combine depth + vision (sensor fusion)
- Improve performance in low visibility

### References
- Ultralytics YOLOv8 Documentation
- ROS 2 Documentation
- IBVS (Image-Based Visual Servoing) research papers

# AUTHOR
Amrutha S Araballi
