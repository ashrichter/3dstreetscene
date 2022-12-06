import pygame
# import the scene class
from ShadowMapping import *
from blender import load_obj_file
from environmentMapping import *
from lightSource import LightSource
from scene import Scene
from skyBox import *
from sphereModel import Sphere


class Street(Scene):
    def __init__(self):
        Scene.__init__(self)

        self.light = LightSource(self, position=[-1., 6., -10.])

        self.shaders = 'phong'

        # for shadow map rendering
        self.shadows = ShadowMap(light=self.light)
        self.show_shadow_map = ShowTexture(self, self.shadows)

        road = load_obj_file('models/road.obj')
        self.add_models_list([DrawModelFromMesh(scene=self, M=np.matmul(
            np.matmul(translationMatrix([0, -4, 4]), rotationMatrixY(np.pi / 2.0)), scaleMatrix([0.02, 0.005, 0.005])),
                                                mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows),
                                                name='road') for mesh in road])

        building2 = load_obj_file('models/building2.obj')
        self.add_models_list([DrawModelFromMesh(scene=self, M=np.matmul(
            np.matmul(translationMatrix([7, -4, -12]), rotationMatrixY(np.pi)), scaleMatrix([0.7, 0.7, 0.7])),
                                                mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows),
                                                name='building2') for mesh in building2])

        building3 = load_obj_file('models/building3.obj')
        self.add_models_list([DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([-5.6, -4, -8.5]),
                                                                        scaleMatrix([0.3, 0.3, 0.3])),
                                                mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows),
                                                name='building3') for mesh in building3])

        building4 = load_obj_file('models/building3.obj')
        self.add_models_list([DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([-5.6, -4, -10.5]),
                                                                        scaleMatrix([0.3, 0.3, 0.3])),
                                                mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows),
                                                name='building4') for mesh in building4])

        building5 = load_obj_file('models/building3.obj')
        self.add_models_list([DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([-5.6, -4, -12.5]),
                                                                        scaleMatrix([0.3, 0.3, 0.3])),
                                                mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows),
                                                name='building5') for mesh in building5])

        apartment = load_obj_file('models/apartment.obj')
        self.add_models_list(
            [DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([-6, -4, -2]), scaleMatrix([0.2, 0.2, 0.2])),
                               mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='apartment') for
             mesh in apartment])

        bball = load_obj_file('models/bball.obj')
        self.add_models_list([DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([5.5, -3.95, -2]),
                                                                        scaleMatrix([0.0095, 0.0095, 0.0095])),
                                                mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows),
                                                name='bball') for mesh in bball])

        graffiti = load_obj_file('models/graffiti.obj')
        self.add_models_list([DrawModelFromMesh(scene=self, M=np.matmul(
            np.matmul(translationMatrix([-5, -4, -5.4]), rotationMatrixY(np.pi)), scaleMatrix([0.25, 0.25, 0.23])),
                                                mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows),
                                                name='graffiti') for mesh in graffiti])

        bus_stop = load_obj_file('models/stop.obj')
        self.add_models_list(
            [DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([-3, -4, -2]), scaleMatrix([0.1, 0.1, 0.1])),
                               mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='bus_stop') for mesh
             in bus_stop])

        pavement = load_obj_file('models/pavement.obj')
        self.add_models_list([DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([0, -4.05, -8]),
                                                                        scaleMatrix([0.04, 0.01, 0.071])),
                                                mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows),
                                                name='pavement') for mesh in pavement])

        court = load_obj_file('models/pavement.obj')
        self.add_models_list([DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([5.7, -4.05, -1.5]),
                                                                        scaleMatrix([0.02, 0.008, 0.008])),
                                                mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows),
                                                name='court') for mesh in court])

        grass = load_obj_file('models/grass.obj')
        self.add_models_list([DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([0, -4.1, -8]),
                                                                        scaleMatrix([0.17, 0.01, 0.071])),
                                                mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows),
                                                name='grass') for mesh in grass])

        hoop = load_obj_file('models/hoop.obj')
        self.add_models_list([DrawModelFromMesh(scene=self, M=np.matmul(
            np.matmul(translationMatrix([6.4, -4, -2.5]), rotationMatrixY(np.pi / -2.0)),
            scaleMatrix([0.15, 0.15, 0.15])),
                                                mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows),
                                                name='hoop') for mesh in hoop])

        walker = load_obj_file('models/walker.obj')
        self.add_models_list([DrawModelFromMesh(scene=self, M=np.matmul(
            np.matmul(translationMatrix([6, -4, -4]), rotationMatrixY([np.pi / 2])),
            scaleMatrix([0.006, 0.006, 0.006])),
                                                mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows),
                                                name='walker') for mesh in walker])

        skater = load_obj_file('models/skater.obj')
        self.add_models_list([DrawModelFromMesh(scene=self, M=np.matmul(
            np.matmul(translationMatrix([-2.2, -3.8, -2]), rotationMatrixY([np.pi / 2])),
            scaleMatrix([0.004, 0.004, 0.004])),
                                                mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows),
                                                name='skater') for mesh in skater])

        trash = load_obj_file('models/trash.obj')
        self.add_models_list([DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([4.9, -3.7, -3.2]),
                                                                        scaleMatrix([0.05, 0.05, 0.05])),
                                                mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows),
                                                name='trash') for mesh in trash])

        truck = load_obj_file('models/truck.obj')
        self.add_models_list([DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([1, -3.6, 0]),
                                                                        scaleMatrix([0.005, 0.005, 0.005])),
                                                mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows),
                                                name='truck') for mesh in truck])

        traffic_light1 = load_obj_file('models/traffic_light.obj')
        self.add_models_list([DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([-2.2, -4, -7.5]),
                                                                        scaleMatrix([0.007, 0.007, 0.007])),
                                                mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows),
                                                name='traffic_light') for mesh in traffic_light1])

        traffic_light2 = load_obj_file('models/traffic_light.obj')
        self.add_models_list([DrawModelFromMesh(scene=self, M=np.matmul(
            np.matmul(translationMatrix([2.1, -4, -7.5]), rotationMatrixY([np.pi])),
            scaleMatrix([0.007, 0.007, 0.007])),
                                                mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows),
                                                name='traffic_light') for mesh in traffic_light2])

        bench = load_obj_file('models/bench.obj')
        self.add_models_list([DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([6, -4, -5.5]),
                                                                        scaleMatrix([0.008, 0.008, 0.008])),
                                                mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows),
                                                name='bench') for mesh in bench])

        lamppost = load_obj_file('models/lamppost.obj')
        self.add_models_list([DrawModelFromMesh(scene=self, M=np.matmul(
            np.matmul(translationMatrix([-3, -4, 2]), rotationMatrixY(np.pi / 2)), scaleMatrix([0.004, 0.004, 0.004])),
                                                mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows),
                                                name='lamppost') for mesh in lamppost])

        lamppost2 = load_obj_file('models/lamppost.obj')
        self.add_models_list([DrawModelFromMesh(scene=self, M=np.matmul(
            np.matmul(translationMatrix([-3, -4, -4]), rotationMatrixY(np.pi / 2)), scaleMatrix([0.004, 0.004, 0.004])),
                                                mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows),
                                                name='lamppost2') for mesh in lamppost2])

        lamppost3 = load_obj_file('models/lamppost.obj')
        self.add_models_list([DrawModelFromMesh(scene=self, M=np.matmul(
            np.matmul(translationMatrix([-3, -4, -10]), rotationMatrixY(np.pi / 2)),
            scaleMatrix([0.004, 0.004, 0.004])),
                                                mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows),
                                                name='lamppost3') for mesh in lamppost3])

        lamppost4 = load_obj_file('models/lamppost.obj')
        self.add_models_list([DrawModelFromMesh(scene=self, M=np.matmul(
            np.matmul(translationMatrix([3, -4, 2]), rotationMatrixY(np.pi / -2)), scaleMatrix([0.004, 0.004, 0.004])),
                                                mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows),
                                                name='lamppost4') for mesh in lamppost4])

        lamppost5 = load_obj_file('models/lamppost.obj')
        self.add_models_list([DrawModelFromMesh(scene=self, M=np.matmul(
            np.matmul(translationMatrix([3, -4, -4]), rotationMatrixY(np.pi / -2)), scaleMatrix([0.004, 0.004, 0.004])),
                                                mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows),
                                                name='lamppost5') for mesh in lamppost5])

        lamppost6 = load_obj_file('models/lamppost.obj')
        self.add_models_list([DrawModelFromMesh(scene=self, M=np.matmul(
            np.matmul(translationMatrix([3, -4, -10]), rotationMatrixY(np.pi / -2)),
            scaleMatrix([0.004, 0.004, 0.004])),
                                                mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows),
                                                name='lamppost6') for mesh in lamppost6])

        sit_male = load_obj_file('models/sit_male.obj')
        self.add_models_list([DrawModelFromMesh(scene=self, M=np.matmul(
            np.matmul(translationMatrix([-1.1, -4.2, -1.8]), rotationMatrixY(np.pi)),
            scaleMatrix([0.006, 0.006, 0.006])),
                                                mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows),
                                                name='sit_male') for mesh in sit_male])

        tree = load_obj_file('models/tree.obj')
        self.add_models_list([DrawModelFromMesh(scene=self, M=np.matmul(
            np.matmul(translationMatrix([-6.4, -4, 0.9]), rotationMatrixY(np.pi / 2)),
            scaleMatrix([0.003, 0.003, 0.003])),
                                                mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows),
                                                name='tree') for mesh in tree])

        tree2 = load_obj_file('models/tree.obj')
        self.add_models_list([DrawModelFromMesh(scene=self, M=np.matmul(
            np.matmul(translationMatrix([5.5, -4, -7]), rotationMatrixY(np.pi / 2)),
            scaleMatrix([0.003, 0.003, 0.003])),
                                                mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows),
                                                name='tree2') for mesh in tree2])

        tree3 = load_obj_file('models/tree.obj')
        self.add_models_list([DrawModelFromMesh(scene=self, M=np.matmul(
            np.matmul(translationMatrix([5.5, -4, -9]), rotationMatrixY(np.pi / 2)),
            scaleMatrix([0.003, 0.003, 0.003])),
                                                mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows),
                                                name='tree3') for mesh in tree3])

        dog = load_obj_file('models/dog.obj')
        self.add_models_list([DrawModelFromMesh(scene=self, M=np.matmul(
            np.matmul(translationMatrix([7, -4.0, -4]), rotationMatrixY(np.pi / -2.0)),
            scaleMatrix([0.005, 0.005, 0.005])),
                                                mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows),
                                                name='dog') for mesh in dog])

        # draw a skybox for the horizon
        self.skybox = SkyBox(scene=self)

        self.show_light = DrawModelFromMesh(scene=self, M=poseMatrix(position=self.light.position, scale=0.2),
                                            mesh=Sphere(material=Material(Ka=[10, 10, 10])), shader=FlatShader())

        self.environment = EnvironmentMappingTexture(width=400, height=400)

        peugeot = load_obj_file('models/peugeot.obj')
        self.add_models_list([DrawModelFromMesh(scene=self, M=np.matmul(
            np.matmul(translationMatrix([-1, -3.6, -2]), rotationMatrixY(np.pi)), scaleMatrix([0.006, 0.006, 0.006])),
                                                mesh=mesh, shader=EnvironmentShader(map=self.environment),
                                                name='peugeot') for mesh in peugeot])

    def draw_shadow_map(self):
        # first clear the scene, also clear the depth buffer to handle occlusions
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for model in self.models:
            model.draw()

    def draw_reflections(self):
        self.skybox.draw()

        for model in self.models:
            model.draw()

    def draw(self, framebuffer=False):
        """
        Draw all models in the scene
        :return: None
        """

        # first clear the scene, also clear the depth buffer to handle occlusions
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # when using a framebuffer, do not update the camera to allow for arbitrary viewpoint.
        if not framebuffer:
            self.camera.update()

        # first, draw the skybox
        self.skybox.draw()

        # render the shadows
        self.shadows.render(self)

        # when rendering the framebuffer ignore the reflective object
        if not framebuffer:
            # glEnable(GL_BLEND)
            # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            # self.envbox.draw()
            # self.environment.update(self)
            # self.envbox.draw()

            self.environment.update(self)

            self.show_shadow_map.draw()

        for model in self.models:
            model.draw()

        self.show_light.draw()

        # once done drawing, display the scene
        # Note that here double buffering is used to avoid artefacts:
        # draw on a different buffer than the one displaying,
        # and flip the two buffers once done drawing.
        if not framebuffer:
            pygame.display.flip()


if __name__ == '__main__':
    # initialises the scene object
    scene = Street()

    # starts drawing the scene
    scene.run()
