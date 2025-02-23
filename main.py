"""
OpenGL 3D Scene with Material Properties and Lighting

This program demonstrates various OpenGL features:
- Material properties (transparency, shininess, diffuse reflection)
- Texture mapping
- Dynamic lighting with controllable parameters
- Camera controls
- Text rendering

The scene contains three objects:
1. A transparent cube
2. A golden polished sphere
3. A textured torus

Controls are displayed on screen and can be toggled with 'H' key.
"""

import sys
import math

import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut
import numpy as np
from PIL import Image


def render_text(text, x, y):
    """
    Renders 2D text overlay on the scene.
    Uses GLUT bitmap fonts and temporarily switches to orthographic projection.

    Args:
        text (str): Text to render
        x, y (int): Screen coordinates for text position
    """
    # Disable 3D features
    gl.glDisable(gl.GL_LIGHTING)
    gl.glDisable(gl.GL_DEPTH_TEST)

    # Switch to 2D orthographic projection
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glPushMatrix()
    gl.glLoadIdentity()
    gl.glOrtho(0, 800, 0, 600, -1, 1)

    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glPushMatrix()
    gl.glLoadIdentity()

    # Render text
    gl.glColor3f(1, 1, 1)
    gl.glRasterPos2i(x, y)
    for ch in text:
        glut.glutBitmapCharacter(glut.GLUT_BITMAP_8_BY_13, ord(ch))

    # Restore previous state
    gl.glPopMatrix()
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glPopMatrix()
    gl.glMatrixMode(gl.GL_MODELVIEW)

    # Re-enable 3D features
    gl.glEnable(gl.GL_LIGHTING)
    gl.glEnable(gl.GL_DEPTH_TEST)


class Scene:
    """
    Manages the 3D scene including objects, lighting, camera and interaction.
    """

    def __init__(self):
        """Initialize scene parameters and state."""
        # Object properties
        self.alpha = 0.9  # Cube transparency
        self.alpha_direction = -0.001  # Rate of transparency change

        # Lighting properties
        self.light_pos = [0.0, 2.0, 2.0, 1.0]  # Point light position
        self.light_intensity = 1.0
        self.light_color = [1.0, 1.0, 1.0]  # White light

        # Camera properties
        self.camera_distance = 5.0
        self.camera_rot_x = 30.0
        self.camera_rot_y = 0.0
        self.camera_pos = [0.0, 0.0, 0.0]

        # UI state
        self.mouse_button = None
        self.mouse_prev_pos = None
        self.show_help = True
        self.texture = None

    # === Initialization Methods ===

    def init(self):
        """Initialize OpenGL state and load resources."""
        # Enable required OpenGL features
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_LIGHT0)
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        self.texture = self.load_texture()

    def load_texture(self, path="texture.png"):
        """
        Load texture from file or create fallback checkerboard pattern.

        Args:
            path (str): Path to texture image file

        Returns:
            int: OpenGL texture ID
        """
        try:
            image = Image.open(path).convert("RGB")
            img_data = np.array(list(image.getdata()), np.uint8)
        except Exception as e:
            print(f"Failed to load texture {path}: {e}")
            # Create fallback checkerboard texture
            size = 64
            img_data = np.zeros((size * size, 3), dtype=np.uint8)
            for i in range(size):
                for j in range(size):
                    c = 255 if (i + j) % 2 == 0 else 0
                    img_data[i * size + j] = [c, c, c]
            image = Image.frombytes("RGB", (size, size), img_data.tobytes())

        texture = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
        gl.glTexImage2D(
            gl.GL_TEXTURE_2D,
            0,
            gl.GL_RGB,
            image.size[0],
            image.size[1],
            0,
            gl.GL_RGB,
            gl.GL_UNSIGNED_BYTE,
            img_data,
        )
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        return texture

    # === Drawing Methods ===

    def draw_cube(self):
        """Draw a transparent cube with animated transparency."""
        gl.glPushMatrix()
        gl.glTranslatef(-2.0, 0.0, 0.0)

        # Material settings for the transparent cube
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_AMBIENT, [0.2, 0.2, 0.2, self.alpha])
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_DIFFUSE, [0.8, 0.8, 0.8, self.alpha])
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_SPECULAR, [1.0, 1.0, 1.0, self.alpha])
        gl.glMaterialf(gl.GL_FRONT, gl.GL_SHININESS, 50.0)

        glut.glutSolidCube(1.0)
        gl.glPopMatrix()

    def draw_sphere(self):
        """Draw a polished golden sphere with high specular reflection."""
        gl.glPushMatrix()
        gl.glTranslatef(0.0, 0.0, 0.0)

        # Gold material properties
        gold_ambient = [0.24725, 0.1995, 0.0745, 1.0]
        gold_diffuse = [0.75164, 0.60648, 0.22648, 1.0]
        gold_specular = [0.628281, 0.555802, 0.366065, 1.0]
        gold_shininess = 128

        # Material settings for gold sphere
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_AMBIENT, gold_ambient)
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_DIFFUSE, gold_diffuse)
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_SPECULAR, gold_specular)
        gl.glMaterialf(gl.GL_FRONT, gl.GL_SHININESS, gold_shininess)

        glut.glutSolidSphere(0.5, 32, 32)
        gl.glPopMatrix()

    def draw_torus(self):
        """Draw a textured torus using custom texture coordinates."""
        gl.glPushMatrix()
        gl.glTranslatef(2.0, 0.0, 0.0)

        # Custom texture coordinates for torus
        def torus_tex_coord(u, v):
            return u, v

        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture)

        # Draw torus with explicit texture coordinates
        majorR = 0.5
        minorR = 0.2
        majorSegs = 32
        minorSegs = 32

        for i in range(majorSegs):
            gl.glBegin(gl.GL_QUAD_STRIP)
            for j in range(minorSegs + 1):
                for k in range(2):
                    theta = (i + k) * 2.0 * math.pi / majorSegs
                    phi = j * 2.0 * math.pi / minorSegs

                    u = (i + k) / float(majorSegs)
                    v = j / float(minorSegs)
                    gl.glTexCoord2f(*torus_tex_coord(u, v))

                    x = (majorR + minorR * math.cos(phi)) * math.cos(theta)
                    y = (majorR + minorR * math.cos(phi)) * math.sin(theta)
                    z = minorR * math.sin(phi)

                    normal = [
                        math.cos(theta) * math.cos(phi),
                        math.sin(theta) * math.cos(phi),
                        math.sin(phi),
                    ]
                    gl.glNormal3f(*normal)
                    gl.glVertex3f(x, y, z)
            gl.glEnd()

        gl.glDisable(gl.GL_TEXTURE_2D)
        gl.glPopMatrix()

    def draw_light_source(self):
        """Visualize light source position as a small sphere."""
        gl.glPushMatrix()
        gl.glTranslatef(*self.light_pos[:3])
        gl.glDisable(gl.GL_LIGHTING)
        gl.glColor3f(*self.light_color)
        glut.glutSolidSphere(0.1, 8, 8)
        gl.glEnable(gl.GL_LIGHTING)
        gl.glPopMatrix()

    # === Scene Update Methods ===

    def update_light(self):
        """Update light source parameters in OpenGL state."""
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, self.light_pos)
        gl.glLightfv(
            gl.GL_LIGHT0,
            gl.GL_DIFFUSE,
            [c * self.light_intensity for c in self.light_color],
        )
        gl.glLightfv(
            gl.GL_LIGHT0,
            gl.GL_SPECULAR,
            [c * self.light_intensity for c in self.light_color],
        )

    def get_status_text(self):
        """Generate list of text lines showing controls and current state."""
        return [
            "Controls:",
            "H - Toggle help",
            "WASD - Move light horizontally",
            "QE - Light intensity",
            "RGB/rgb - Light color",
            "Arrow keys - Move light vertically",
            "Mouse drag - Rotate camera",
            "Mouse wheel - Zoom",
            "Middle mouse - Pan camera",
            "",
            f"Light position: ({self.light_pos[0]:.1f}, {self.light_pos[1]:.1f}, {self.light_pos[2]:.1f})",
            f"Light intensity: {self.light_intensity:.2f}",
            f"Light color: ({self.light_color[0]:.2f}, {self.light_color[1]:.2f}, {self.light_color[2]:.2f})",
            f"Camera distance: {self.camera_distance:.1f}",
            f"Cube alpha: {self.alpha:.2f}",
        ]

    def display(self):
        """Main display callback - render the entire scene."""
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()

        # Apply camera transformations
        gl.glTranslatef(self.camera_pos[0], self.camera_pos[1], -self.camera_distance)
        gl.glRotatef(self.camera_rot_x, 1, 0, 0)
        gl.glRotatef(self.camera_rot_y, 0, 1, 0)

        self.update_light()
        self.draw_light_source()

        # Drawing objects
        self.draw_sphere()
        self.draw_torus()

        # Draw transparent cube last
        gl.glDepthMask(gl.GL_FALSE)
        self.draw_cube()
        gl.glDepthMask(gl.GL_TRUE)

        # Update cube transparency
        self.alpha += self.alpha_direction
        if self.alpha <= 0.5 or self.alpha >= 0.9:
            self.alpha_direction *= -1

        # Render help text if enabled
        if self.show_help:
            y = 580
            for line in self.get_status_text():
                render_text(line, 10, y)
                y -= 20

        glut.glutSwapBuffers()

    # === Input Handling Methods ===

    def keyboard(self, key, x, y):
        """
        Handle keyboard input for light control.

        WASD: Move light horizontally
        QE: Adjust light intensity
        RGB/rgb: Adjust light color
        H: Toggle help display
        """
        movement_step = 0.5
        color_step = 0.1

        # To force redisplay if any key is pressed
        changed = True

        if key == b"w":
            self.light_pos[2] -= movement_step
        elif key == b"s":
            self.light_pos[2] += movement_step
        elif key == b"a":
            self.light_pos[0] -= movement_step
        elif key == b"d":
            self.light_pos[0] += movement_step
        elif key == b"q":
            self.light_intensity = min(1.0, self.light_intensity + color_step)
        elif key == b"e":
            self.light_intensity = max(0.0, self.light_intensity - color_step)
        # Управление цветом света
        elif key == b"r":
            self.light_color[0] = min(1.0, self.light_color[0] + color_step)
        elif key == b"R":
            self.light_color[0] = max(0.0, self.light_color[0] - color_step)
        elif key == b"g":
            self.light_color[1] = min(1.0, self.light_color[1] + color_step)
        elif key == b"G":
            self.light_color[1] = max(0.0, self.light_color[1] - color_step)
        elif key == b"b":
            self.light_color[2] = min(1.0, self.light_color[2] + color_step)
        elif key == b"B":
            self.light_color[2] = max(0.0, self.light_color[2] - color_step)
        elif key == b"h":
            self.show_help = not self.show_help
            changed = True
        else:
            changed = False

        if changed:
            self.update_light()
            glut.glutPostRedisplay()

    def special(self, key, x, y):
        """Handle special keys for vertical light movement."""
        if key == glut.GLUT_KEY_UP:
            self.light_pos[1] += 0.5
        elif key == glut.GLUT_KEY_DOWN:
            self.light_pos[1] -= 0.5
        glut.glutPostRedisplay()

    def mouse(self, button, state, x, y):
        """Handle mouse button events for camera control."""
        if state == glut.GLUT_DOWN:
            self.mouse_button = button
            self.mouse_prev_pos = (x, y)
        else:
            self.mouse_button = None

    def motion(self, x, y):
        """Handle mouse motion for camera rotation and panning."""
        if self.mouse_prev_pos is None:
            self.mouse_prev_pos = (x, y)
            return

        dx = x - self.mouse_prev_pos[0]
        dy = y - self.mouse_prev_pos[1]

        if self.mouse_button == glut.GLUT_LEFT_BUTTON:
            self.camera_rot_y += dx * 0.5
            self.camera_rot_x += dy * 0.5
        elif self.mouse_button == glut.GLUT_MIDDLE_BUTTON:
            self.camera_pos[0] += dx * 0.01
            self.camera_pos[1] -= dy * 0.01

        self.mouse_prev_pos = (x, y)
        glut.glutPostRedisplay()

    def mouse_wheel(self, wheel, direction, x, y):
        """Handle mouse wheel for camera zoom."""
        self.camera_distance -= direction
        self.camera_distance = max(2.0, min(20.0, self.camera_distance))
        glut.glutPostRedisplay()


def main():
    """Initialize GLUT and start the application."""
    glut.glutInit(sys.argv)
    glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGB | glut.GLUT_DEPTH)
    glut.glutInitWindowSize(800, 600)
    glut.glutInitWindowPosition(100, 100)
    window = glut.glutCreateWindow(b"3D Scene with OpenGL")
    glut.glutSetWindow(window)  # Force window focus

    scene = Scene()
    scene.init()

    glut.glutDisplayFunc(scene.display)
    glut.glutIdleFunc(scene.display)
    glut.glutKeyboardFunc(scene.keyboard)
    glut.glutSpecialFunc(scene.special)
    glut.glutMouseFunc(scene.mouse)
    glut.glutMotionFunc(scene.motion)
    glut.glutMouseWheelFunc(scene.mouse_wheel)
    glut.glutKeyboardUpFunc(lambda *args: glut.glutPostRedisplay())

    gl.glClearColor(0.0, 0.0, 0.0, 1.0)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    glu.gluPerspective(45, 800.0 / 600.0, 0.1, 100.0)
    gl.glMatrixMode(gl.GL_MODELVIEW)

    glut.glutMainLoop()


if __name__ == "__main__":
    main()
