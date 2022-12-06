from BaseModel import DrawModelFromMesh
from cubeMap import CubeMap
from mesh import *
from shaders import *


class SkyBoxShader(BaseShaderProgram):
    def __init__(self, name='skybox'):
        BaseShaderProgram.__init__(self, name=name)
        self.add_uniform('sampler_cube')

    def bind(self, model, M):
        BaseShaderProgram.bind(self, model, M)
        P = model.scene.P  # get projection matrix from the scene
        V = model.scene.camera.V  # get view matrix from the camera
        Vr = np.identity(4)
        Vr[:3, :3] = V[:3, :3]

        self.uniforms['PVM'].bind(np.matmul(P, np.matmul(V, M)))
        

class SkyBox(DrawModelFromMesh):
    def __init__(self, scene):
        DrawModelFromMesh.__init__(self, scene=scene, M=poseMatrix(scale=10.0),
                                   mesh=CubeMesh(texture=CubeMap(name='skybox'), inside=True),
                                   shader=SkyBoxShader(), name='skybox')

    def draw(self):
        glDepthMask(GL_FALSE)
        DrawModelFromMesh.draw(self)
        glDepthMask(GL_TRUE)

