# OpenGL Materials and Lighting Demo

A Python-based OpenGL application that demonstrates material properties, lighting, and texture mapping using 3D primitives.

## Features

- Three interactive 3D objects with different material properties:
  - Transparent cube with pulsating transparency (0.5-0.9)
  - Polished golden sphere with high shininess
  - Textured torus with diffuse reflection
- Dynamic point light source with adjustable:
  - Position (3D movement)
  - Intensity
  - Color (RGB components)
- Interactive camera controls
- Real-time parameter display

## Requirements

- Python 3.x
- PyOpenGL
- PyOpenGL-accelerate (optional, but recommended)
- Pillow (PIL)
- NumPy

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. Place a texture image named `texture.png` in the same directory
2. Run the application:

```bash
python main.py
```

### Controls

#### Light Control

- WASD: Move light horizontally
- Arrow Up/Down: Move light vertically
- Q/E: Increase/decrease light intensity
- RGB/rgb: Adjust RGB components of light color

#### Camera Control

- Left Mouse + Drag: Rotate camera
- Middle Mouse + Drag: Pan camera
- Mouse Wheel: Zoom in/out

#### Interface

- H: Toggle help display

## Implementation Details

- Transparent cube demonstrates alpha blending
- Golden sphere showcases specular highlights
- Textured torus shows UV mapping
- Real-time text rendering using GLUT bitmap fonts
- Proper depth handling for transparency
- Phong lighting model implementation

## Documentation

For detailed technical explanation (in Russian), see [detailed_explanation_ru.md](./docs/detailed_explanation_ru.md).
