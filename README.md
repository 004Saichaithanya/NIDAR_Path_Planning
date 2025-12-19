# 🛰️ Step 3 – Coverage Path Planning (Lawn-Mower Waypoints)

## Mission 1 – Disaster Management

**Scout Drone Autonomous Path Planning**

---

## 📌 Overview

This repository contains the **implementation of Step 3** in the disaster-management drone pipeline.

**Step 3 converts a mission Area of Interest (AOI) into executable flight waypoints** that allow a scout drone to autonomously scan a flooded region and support real-time human detection.

---

## 🎯 Purpose of Step 3

The goal of Step 3 is to generate a **complete coverage flight path** for the scout drone.

Specifically, this step:

* Takes an **irregular AOI polygon** provided as a **KML file**
* Computes **camera-based coverage parameters** (swath & pass spacing)
* Generates a **lawn-mower (boustrophedon) scan pattern**
* Outputs an **ordered list of GPS waypoints**
* Ensures **no blind spots** during aerial scanning

These waypoints are later uploaded to the drone’s flight controller for **fully autonomous execution**.

---

## 🧾 Inputs

| Input                  | Description                      |
| ---------------------- | -------------------------------- |
| `area_of_interest.kml` | AOI polygon (challenge provided) |
| Flight altitude        | 50 feet (15.24 m)                |
| Camera FOV             | 57°                              |
| Overlap                | 25% (recommended)                |

---

## 📤 Output

### Waypoint List (Scout Mission Path)

```text
WP1: (lat, lon, altitude)
WP2: (lat, lon, altitude)
WP3: (lat, lon, altitude)
...
```

### Output Data Structure

```json
[
  { "lat": 17.3828, "lon": 78.4866, "alt": 15.24 },
  { "lat": 17.3828, "lon": 78.4910, "alt": 15.24 }
]
```

### What This Output Is Used For

✅ Uploaded to **Pixhawk / Mission Planner**
✅ Executed in **AUTO mode**
✅ Drives the drone’s **search motion**
❌ Not survivor locations
❌ Not delivery points

---

## 🧠 How Step 3 Fits in the Overall System

### 🔄 Path Planning Pipeline Architecture

```
KML AOI (Challenge Input)
        ↓
STEP 1: Extract Boundary Coordinates
        ↓
STEP 2: Camera Coverage Calculation
        ↓
STEP 3: Lawn-Mower Waypoint Generation  ← (This Repo)
        ↓
Pixhawk / Mission Planner
        ↓
Autonomous Scout Drone Flight
        ↓
STEP 4: Human Detection & GPS Geo-Tagging
        ↓
STEP 5–7: Survivor Clustering & Delivery Path Planning
```

---

## 🏗️ Algorithm Used

### Lawn-Mower (Boustrophedon) Coverage Path Planning

* Parallel scan lines across AOI
* Alternate direction after each pass
* Constant altitude for stable vision inference
* Bounding-box coverage to guarantee full scan

This approach is:

* Deterministic
* Energy-efficient
* Widely used in real UAV survey missions

---

## 📦 Required Libraries

```bash
pip install lxml
```

Other dependencies (`math`) are part of Python’s standard library.

---

## 🚀 Next Steps (Beyond This Repo)

After Step 3, the system moves to:

### ▶ Step 4 – Human Detection Integration

* Run YOLO-based detection during waypoint traversal
* Read real-time GPS from flight controller
* Geo-tag detected survivors

### ▶ Step 5–7 – Delivery Planning

* Cluster detections
* Prioritize survivors
* Generate optimized delivery routes

---

## 📚 Project Context

This work is part of **Mission 1 – Disaster Management**, where autonomous drones are deployed to:

* Scan flooded regions
* Locate stranded survivors
* Enable rapid relief delivery

---

## ✅ Status

✔ Step 3 – **Complete & Verified**
✔ Tested with irregular AOI KML
✔ Ready for integration with Step 4
