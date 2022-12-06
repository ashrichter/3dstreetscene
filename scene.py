# pygame is used to create a window with the operating system on which to draw.
import pygame

# import the camera class
from camera import Camera

# import the lightsource class
from lightSource import LightSource

# import the shader class
from shaders import *


class Scene:
    """
    This is the main class for drawing an OpenGL scene using the PyGame library
    """

    def __init__(self, width=800, height=600, shaders=None):
        """
        Initialises the scene
        """

        self.window_size = (width, height)

        # by default, wireframe mode is off
        self.wireframe = False

        # first two lines initialise the pygame window
        pygame.init()
        screen = pygame.display.set_mode(self.window_size, pygame.OPENGL | pygame.DOUBLEBUF, 24)

        # start initialising the window from the OpenGL side
        glViewport(0, 0, self.window_size[0], self.window_size[1])

        # selects the background color
        glClearColor(0.7, 0.7, 1.0, 1.0)

        # enable the vertex array capability
        glEnableClientState(GL_VERTEX_ARRAY)

        # enable depth test for clean output
        glEnable(GL_DEPTH_TEST)

        # set the default shader program
        self.shaders = 'flat'

        # initialise the projective transform
        near = 1.0
        far = 20.0
        left = -1.0
        right = 1.0
        top = -1.0
        bottom = 1.0

        # cycle through models
        self.show_model = -1

        # frustrum projection
        self.P = frustumMatrix(left, right, top, bottom, near, far)

        # initialises the camera object
        self.camera = Camera()

        # initialise the light source
        self.light = LightSource(self, position=[5., 5., 5.])

        # rendering mode for the shaders
        self.mode = 1  # initialise to full interpolated shading

        # This class will maintain a list of models to draw in the scene
        self.models = []

    def add_models_list(self, models_list):
        """
        This method adds a model to the list of models.
        :param model: The model object to add to the scene
        :return: None
        """
        for model in models_list:
            self.models.append(model)

    def draw(self, framebuffer=False):
        """
        Draw all models in the scene
        :return: None
        """

        # first clear the scene, also clear the depth buffer to handle occlusions
        if not framebuffer:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # ensure that the camera view matrix is up to date
            self.camera.update()

        # then loop over all models in the list and draw them
        for model in self.models:
            model.draw()

        # once done drawing, display the scene
        # use double buffering to avoid artefacts:
        # draw on a different buffer than the one to display,
        # and flip the two buffers once we are done drawing.
        if not framebuffer:
            pygame.display.flip()

    def keyboard(self, event):
        """
        Method to process keyboard events. Check Pygame documentation for a list of key events
        :param event: the event object that was raised
        """
        if event.key == pygame.K_q:
            self.running = False

    def pygameEvents(self):
        """
        Method to handle PyGame events for user interaction.
        """
        # check whether the window has been closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # keyboard events
            elif event.type == pygame.KEYDOWN:
                self.keyboard(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mods = pygame.key.get_mods()
                if event.button == 4:

                    if mods & pygame.KMOD_CTRL:
                        self.light.position *= 1.1
                        self.light.update()
                    else:
                        self.camera.distance = max(1, self.camera.distance - 1)

                elif event.button == 5:

                    if mods & pygame.KMOD_CTRL:
                        self.light.position *= 0.9
                        self.light.update()
                    else:
                        self.camera.distance += 1

            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    if self.mouse_mvt is not None:
                        self.mouse_mvt = pygame.mouse.get_rel()

                        self.camera.center[0] -= (float(self.mouse_mvt[0]) / self.window_size[0])
                        self.camera.center[1] -= (float(self.mouse_mvt[1]) / self.window_size[1])
                    else:
                        self.mouse_mvt = pygame.mouse.get_rel()

                elif pygame.mouse.get_pressed()[2]:
                    if self.mouse_mvt is not None:
                        self.mouse_mvt = pygame.mouse.get_rel()

                        self.camera.phi -= (float(self.mouse_mvt[0]) / self.window_size[0])
                        self.camera.psi -= (float(self.mouse_mvt[1]) / self.window_size[1])
                    else:
                        self.mouse_mvt = pygame.mouse.get_rel()
                else:
                    self.mouse_mvt = None

    def run(self):
        """
        Draws the scene in a loop until exit.
        """

        # classic program loop
        self.running = True
        while self.running:
            self.pygameEvents()

            # otherwise, continue drawing
            self.draw()
