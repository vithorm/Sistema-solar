import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Função para carregar a textura
def load_texture(file_name):
    texture_surface = pygame.image.load(file_name)
    texture_data = pygame.image.tostring(texture_surface, "RGB", 1)
    width, height = texture_surface.get_size()

    glEnable(GL_TEXTURE_2D)
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return texture

# Função para desenhar uma esfera com textura
def draw_textured_sphere(texture, radius=1, slices=16, stacks=16):
    glBindTexture(GL_TEXTURE_2D, texture)

    for i in range(stacks):
        lat0 = math.pi * (-0.5 + float(i) / stacks)      # Latitude 1
        lat1 = math.pi * (-0.5 + float(i + 1) / stacks)  # Latitude 2

        z0 = math.sin(lat0)  # Z-coord da latitude 1
        zr0 = math.cos(lat0) # Radius in the x-y plane

        z1 = math.sin(lat1)  # Z-coord da latitude 2
        zr1 = math.cos(lat1) # Radius in the x-y plane

        glBegin(GL_QUAD_STRIP)
        for j in range(slices + 1):
            lng = 2 * math.pi * float(j) / slices   # Longitude

            x = math.cos(lng)  # X-coord da longitude
            y = math.sin(lng)  # Y-coord da longitude

            # Coordenadas de textura
            u = float(j) / slices
            v0 = float(i) / stacks
            v1 = float(i + 1) / stacks

            # Vértice e coordenadas de textura para cada ponto
            glTexCoord2f(u, v0)
            glVertex3f(x * zr0 * radius, y * zr0 * radius, z0 * radius)
            glTexCoord2f(u, v1)
            glVertex3f(x * zr1 * radius, y * zr1 * radius, z1 * radius)
        glEnd()

# Função para desenhar um anel com textura
def draw_textured_ring(texture, inner_radius, outer_radius, slices=50):
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUAD_STRIP)
    for i in range(slices + 1):
        theta = 2 * math.pi * i / slices
        x = math.cos(theta)
        y = math.sin(theta)
        
        # Coordenadas de textura e vértices
        glTexCoord2f(0.5 + 0.5 * x, 0.5 + 0.5 * y)
        glVertex3f(inner_radius * x, 0, inner_radius * y)
        glTexCoord2f(0.5 + x, 0.5 + y)
        glVertex3f(outer_radius * x, 0, outer_radius * y)
    glEnd()

# Inicialização do Pygame e OpenGL
def init():
    pygame.init()
    pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)

    glEnable(GL_DEPTH_TEST)  # Habilitar o teste de profundidade
    glEnable(GL_TEXTURE_2D)  # Habilitar texturas

    # Definir a perspectiva da câmera
    gluPerspective(30, (800 / 600), 0.1, 100.0)

    # Mover a câmera para uma vista de cima inclinada
    glRotatef(60, 1, 0, 0)  # Inclinação para a horizontal
    glTranslatef(0.0, -65.0, -40.0)  # Ajuste da posição da câmera

# Loop principal
def main():
    init()

    # Carregar texturas
    textures = {
        "sol": load_texture("sol.png"),
        "mercurio": load_texture("mercurio.png"),
        "venus": load_texture("venus.png"),
        "terra": load_texture("terra.png"),
        "marte": load_texture("marte.png"),
        "jupiter": load_texture("jupiter.png"),
        "saturno": load_texture("saturno.png"),
        "urano": load_texture("uranus.png"),
        "netuno": load_texture("netuno.png"),
        "anel": load_texture("anel.png"),  # Nova textura para o anel
    }

    # Raio das órbitas
    orbits = {
        "mercurio": 3,
        "venus": 5,
        "terra": 7,
        "marte": 9,
        "jupiter": 12,
        "saturno": 15,
        "urano": 18,
        "netuno": 21,
    }

    # Tamanhos dos planetas
    sizes = {
        "sol": 2.5,
        "mercurio": 0.4,
        "venus": 0.6,
        "terra": 0.7,
        "marte": 0.5,
        "jupiter": 1.2,
        "saturno": 1.0,
        "urano": 0.8,
        "netuno": 0.8,
    }

    rotation_angles = {planet: 0 for planet in textures.keys()}  # Ângulos de rotação
    orbit_speeds = {
        "mercurio": 4.8,
        "venus": 3.5,
        "terra": 2.9,
        "marte": 2.4,
        "jupiter": 1.3,
        "saturno": 1.0,
        "urano": 0.7,
        "netuno": 0.5,
    }

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Limpar a tela e o buffer de profundidade
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Desenhar o Sol
        glPushMatrix()
        draw_textured_sphere(textures["sol"], sizes["sol"])
        glPopMatrix()

        # Desenhar os planetas
        for planet, orbit_radius in orbits.items():
            rotation_angles[planet] += orbit_speeds[planet]  # Atualizar ângulo de órbita

            glPushMatrix()
            # Translação para a órbita do planeta
            glRotatef(rotation_angles[planet], 0, 1, 0)
            glTranslatef(orbit_radius, 0, 0)

            # Rotação do planeta em torno de seu próprio eixo
            glRotatef(rotation_angles[planet] * 5, 0, 1, 0)

            # Desenhar o planeta
            draw_textured_sphere(textures[planet], sizes[planet])

            # Desenhar o anel de Saturno
            if planet == "saturno":
                glPushMatrix()
                glRotatef(30, 1, 0, 0)  # Inclinar o anel
                draw_textured_ring(textures["anel"], sizes[planet] * 1.5, sizes[planet] * 2.5)
                glPopMatrix()

            glPopMatrix()

        # Atualizar a tela
        pygame.display.flip()
        pygame.time.wait(1)

    # Encerrar o Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
