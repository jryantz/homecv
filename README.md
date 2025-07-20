# 🏠 HomeCV - Computer Vision for Home Automation

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-red?logo=opencv&logoColor=white)](https://opencv.org)
[![YOLO](https://img.shields.io/badge/YOLO-v11-yellow?logo=yolo&logoColor=white)](https://ultralytics.com)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Integration-blue?logo=homeassistant&logoColor=white)](https://home-assistant.io)

*AI-powered person detection for smart home security and automation*

</div>

## 🎯 Overview

HomeCV is an intelligent computer vision service that integrates with Home Assistant to provide real-time person
detection at your front door. Using advanced YOLO object detection models, it analyzes camera snapshots to determine if
someone is present in a predefined zone, enabling smart home automations based on visitor presence.

## ✨ Features

- 🤖 **AI-Powered Detection**: Uses YOLO v11 for accurate person detection
- 🏠 **Home Assistant Integration**: Seamless integration with Home Assistant camera entities
- 🎯 **Zone-Based Detection**: Configurable detection zones for precise monitoring
- 🖼️ **Snapshot Storage**: Optional debug mode saves original and analyzed images
- 🚀 **RESTful API**: Simple HTTP API for easy integration
- ⚡ **Fast Processing**: Optimized for real-time detection with minimal latency
- 🔧 **Configurable**: Environment-based configuration for easy deployment

## 🏗️ Architecture

```
homecv/
├── 📁 api/                   # Flask API layer
│   ├── __init__.py           # App factory
│   └── routes/               # API endpoints
│       ├── __init__.py       # Route registration
│       └── check.py          # Detection endpoints
├── 📁 homecv/                # Core application logic
│   ├── analyzers/            # Computer vision analyzers
│   │   ├── base.py           # Base analyzer with YOLO integration
│   │   └── front_door.py     # Front door specific detection logic
│   ├── integrations/         # External service integrations
│   │   └── hass/             # Home Assistant integration
│   │       └── client.py     # HA API client
│   ├── models/               # YOLO model files
│   │   ├── yolo11n.pt        # YOLO v11 nano model
│   │   └── yolov8n.pt        # YOLO v8 nano model (backup)
│   ├── snapshots/            # Image storage utilities
│   │   └── storage.py        # Snapshot saving functionality
│   └── config.py             # Configuration management
├── 📁 images/                # Stored images (debug mode)
│   ├── originals/            # Original camera snapshots
│   └── snapshots/            # Processed images with detections
└── run.py                    # Application entry point
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Home Assistant instance with camera integration
- Camera entity that provides snapshots

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/homecv.git
   cd homecv
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your settings:
   ```env
   HOMEASSISTANT_URL=https://your-ha-instance.com
   HOMEASSISTANT_TOKEN=your_long_lived_access_token
   
   MODEL_PATH=./homecv/models/yolo11n.pt
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

The service will start on `http://localhost:9000`

## 🔧 Configuration

### Environment Variables

| Variable              | Description                      | Default                      | Required |
|-----------------------|----------------------------------|------------------------------|----------|
| `HOMEASSISTANT_URL`   | Your Home Assistant instance URL | -                            | ✅        |
| `HOMEASSISTANT_TOKEN` | Long-lived access token          | `default-token`              | ✅        |
| `MODEL_PATH`          | Path to YOLO model file          | `./homecv/models/yolo11n.pt` | ❌        |

### Detection Zone Configuration

HomeCV uses a predefined detection zone for the front door camera. This zone can be adjusted in the code to fit your specific camera view and area of interest.

Modify and or add detection zones in the `homecv/analyzers`.

## 📡 API Reference

### Check Front Door

Analyzes the front door camera for person detection.

**Endpoint:** `GET /check/front_door`

**Parameters:**

- `debug` (optional): When present, saves original and processed images to `images/` directory

**Response:**

```json
{
  "detected": true,
  "message": "Person detected at the door!"
}
```

**Example Requests:**

```bash
# Basic detection
curl http://localhost:9000/check/front_door

# With debug mode (saves images)
curl http://localhost:9000/check/front_door?debug=true
```

## 🏠 Home Assistant Integration

### Setup Steps

1. **Create a Long-Lived Access Token**
    - Go to Home Assistant → Profile → Long-Lived Access Tokens
    - Click "Create Token"
    - Copy the token to your `.env` file

2. **Identify Your Camera Entity**
    - Find your camera entity ID (e.g., `camera.front_yard_snapshots_fluent`)
    - Update `homecv/analyzers/front_door.py:21` if needed

3. **Create Automation**
   ```yaml
   # Example automation in Home Assistant
   automation:
     - alias: "Person at Front Door"
       trigger:
         - platform: time_pattern
           seconds: "/30"  # Check every 30 seconds
       action:
         - service: rest_command.check_front_door
         - condition: template
           value_template: "{{ trigger.json.detected }}"
         - service: notify.mobile_app
           data:
             message: "Someone is at the front door!"
   
   # Add to configuration.yaml
   rest_command:
     check_front_door:
       url: "http://your-homecv-server:9000/check/front_door"
       method: GET
   ```

## 🤖 Computer Vision Details

### YOLO Model Integration

HomeCV uses the Ultralytics YOLO implementation with the following features:

- **Model**: YOLO v11 nano (`yolo11n.pt`) for optimal speed/accuracy balance
- **Object Classes**: Focuses on person detection (class 0 in COCO dataset)
- **Processing**: Real-time inference with bounding box visualization
- **Zone Detection**: Intersection calculation between detected persons and predefined zones

### Detection Process

1. **Snapshot Acquisition**: Fetches image from Home Assistant camera entity
2. **Object Detection**: YOLO model processes image to identify persons
3. **Zone Analysis**: Checks if detected persons intersect with the defined zone
4. **Visualization**: Draws detection boxes (green) and zone boundaries (blue)
5. **Result**: Returns boolean detection status with descriptive message

## 🛠️ Development

### Project Structure

- **`api/`**: Flask web framework and REST API endpoints
- **`homecv/analyzers/`**: Computer vision processing logic
- **`homecv/integrations/`**: External service integrations
- **`homecv/snapshots/`**: Image storage and management
- **`tests/`**: Unit tests and integration tests

### Adding New Analyzers

1. Create new analyzer in `homecv/analyzers/`
2. Inherit from base analyzer functions
3. Define detection zones and logic
4. Add API endpoint in `api/routes/`

## 🙏 Acknowledgments

- [Ultralytics YOLO](https://ultralytics.com) for the object detection models
- [Home Assistant](https://home-assistant.io) for the smart home platform
- [OpenCV](https://opencv.org) for computer vision utilities
- [Flask](https://flask.palletsprojects.com/) for the web framework

## 🐛 Troubleshooting

### Common Issues

**1. Connection to Home Assistant fails**

- Verify `HOMEASSISTANT_URL` and `HOMEASSISTANT_TOKEN` in `.env`
- Check that the token has proper permissions
- Ensure Home Assistant is accessible from the HomeCV server

**2. Camera entity not found**

- Verify camera entity ID in `front_door.py:21`
- Check that camera provides snapshots via `/api/camera_proxy/`

**3. YOLO model not loading**

- Ensure model file exists at specified `MODEL_PATH`
- Check that ultralytics package is properly installed

**4. No persons detected**

- Review detection zone coordinates
- Test with debug mode to see processed images
- Adjust zone boundaries based on camera view

---

<div align="center">

**Made with ❤️ for the Home Assistant community**

[Report Bug](https://github.com/jryantz/homecv/issues) | [Request Feature](https://github.com/jryantz/homecv/issues)

</div>