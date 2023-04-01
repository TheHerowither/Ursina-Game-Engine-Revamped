from ursina import Shader

pixelation_shader = Shader(
fragment='''
#version 150

uniform sampler2D tex;
in vec2 window_size;
in vec2 uv;
out vec4 color;
uniform float pixels;

void main() {
    float Pixels = pixels;
    float dx = 9.0 * (1.0 / Pixels);
    float dy = 16.0 * (1.0 / Pixels);
    vec2 new_uv = vec2(dx * floor(uv.x / dx), dy * floor(uv.y / dy));
    color = texture(tex, new_uv);
}
''')
default_input=dict(
    pixels = 1600.0
)

if __name__ == '__main__':
    from ursina import *
    app = Ursina()

    e = Entity(model='sphere', color=color.orange)
    e = Entity(model='cube', y=-1)
    camera.shader = pixelation_shader
    EditorCamera()

    app.run()
