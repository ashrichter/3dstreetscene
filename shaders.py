# imports all openGL functions
from OpenGL.GL import *
from OpenGL.GL import shaders
from matutils import *
# numpy to store data in arrays
import numpy as np


class Uniform:
    """
    Class to handle uniforms, this is not necessary,
    but allow to put all relevant code in one place
    """

    def __init__(self, name, value=None):
        '''
        Initialise the uniform parameter
        :param name: the name of the uniform, as stated in the GLSL code
        '''
        self.name = name
        self.value = value
        self.location = -1

    def link(self, program):
        """
        This function needs to be called after compiling the GLSL program to fetch the location of the uniform
        in the program from its name
        :param program: the GLSL program where the uniform is used
        """
        self.location = glGetUniformLocation(program=program, name=self.name)
        if self.location == -1:
            print('(E) Warning, no uniform {}'.format(self.name))

    def bind_matrix(self, M=None, number=1, transpose=True):
        """
        Call this before rendering to bind the Python matrix to the GLSL uniform mat4.
        You will need different methods for different types of uniform, but for now this will
        do for the PVM matrix
        :param number: the number of matrices sent
        :param transpose: Whether the matrix should be transposed
        """
        if M is not None:
            self.value = M
        if self.value.shape[0] == 4 and self.value.shape[1] == 4:
            glUniformMatrix4fv(self.location, number, transpose, self.value)
        elif self.value.shape[0] == 3 and self.value.shape[1] == 3:
            glUniformMatrix3fv(self.location, number, transpose, self.value)
        else:
            print('(E) Error: Trying to bind as uniform a matrix of shape {}'.format(self.value.shape))

    def bind(self, value):
        if value is not None:
            self.value = value

        if isinstance(self.value, int):
            self.bind_int()
        elif isinstance(self.value, float):
            self.bind_float()
        elif isinstance(self.value, np.ndarray):
            if self.value.ndim == 1:
                self.bind_vector()
            elif self.value.ndim == 2:
                self.bind_matrix()
        else:
            print('Wrong value bound: {}'.format(type(self.value)))

    def bind_int(self, value=None):
        if value is not None:
            self.value = value
        glUniform1i(self.location, self.value)

    def bind_float(self, value=None):
        if value is not None:
            self.value = value
        glUniform1f(self.location, self.value)

    def bind_vector(self, value=None):
        if value is not None:
            self.value = value
        if value.shape[0] == 2:
            glUniform2fv(self.location, 1, value)
        elif value.shape[0] == 3:
            glUniform3fv(self.location, 1, value)
        elif value.shape[0] == 4:
            glUniform4fv(self.location, 1, value)
        else:
            print('(E) Error in Uniform.bind_vector(): Vector should be of dimension 2,3 or 4, found {}'.format(
                value.shape[0]))

    def set(self, value):
        """
        function to set the uniform value
        """
        self.value = value


class BaseShaderProgram:
    """
    This is the base class for loading and compiling the GLSL shaders.
    """

    def __init__(self, name=None, vertex_shader=None, fragment_shader=None):
        """
        Initialises the shaders
        :param vertex_shader: the name of the file containing the vertex shader GLSL code
        :param fragment_shader: the name of the file containing the fragment shader GLSL code
        """

        self.name = name
        print('Creating shader program: {}'.format(name))

        if name is not None:
            vertex_shader = 'shaders/{}/vertex_shader.glsl'.format(name)
            fragment_shader = 'shaders/{}/fragment_shader.glsl'.format(name)

        # load the vertex shader GLSL code
        if vertex_shader is None:
            self.vertex_shader_source = '''
                #version 130

                in vec3 position;   // vertex position
                uniform mat4 PVM; // the Perspective-View-Model matrix is received as a Uniform

                // main function of the shader
                void main() {
                    gl_Position = PVM * vec4(position, 1.0f);  // first we transform the position using PVM matrix
                }
            '''
        else:
            print('Load vertex shader from file: {}'.format(vertex_shader))
            with open(vertex_shader, 'r') as file:
                self.vertex_shader_source = file.read()

        # load the fragment shader GLSL code
        if fragment_shader is None:
            self.fragment_shader_source = '''
                #version 130
                void main() {                   
                      gl_FragColor = vec4(1.0f);      // for now, we just apply the colour uniformly
                }
            '''
        else:
            print('Load fragment shader from file: {}'.format(fragment_shader))
            with open(fragment_shader, 'r') as file:
                self.fragment_shader_source = file.read()

        # storing uniforms in a dictionary.
        self.uniforms = {
            'PVM': Uniform('PVM'),  # project view model matrix
        }

    def add_uniform(self, name):
        self.uniforms[name] = Uniform(name)

    def compile(self, attributes):
        """
        Call this function to compile the GLSL codes for both shaders.
        :return:
        """
        print('Compiling GLSL shaders [{}]...'.format(self.name))
        try:
            self.program = glCreateProgram()
            glAttachShader(self.program, shaders.compileShader(self.vertex_shader_source, shaders.GL_VERTEX_SHADER))
            glAttachShader(self.program, shaders.compileShader(self.fragment_shader_source, shaders.GL_FRAGMENT_SHADER))

        except RuntimeError as error:
            print('(E) An error occured while compiling {} shader:\n {}\n... forwarding exception...'.format(self.name,
                                                                                                             error)),
            raise error

        self.bindAttributes(attributes)

        glLinkProgram(self.program)

        # tell OpenGL to use this shader program for rendering
        glUseProgram(self.program)

        # link all uniforms
        for uniform in self.uniforms:
            self.uniforms[uniform].link(self.program)

    def bindAttributes(self, attributes):
        # bind all shader attributes to the correct locations in the VAO
        for name, location in attributes.items():
            glBindAttribLocation(self.program, location, name)
            print('Binding attribute {} to location {}'.format(name, location))

    def bind(self, model, M):
        """
        Call this function to enable this GLSL Program
        """

        # tell OpenGL to use this shader program for rendering
        glUseProgram(self.program)

        P = model.scene.P
        V = model.scene.camera.V

        # set the PVM matrix uniform
        self.uniforms['PVM'].bind(np.matmul(P, np.matmul(V, M)))


class PhongShader(BaseShaderProgram):
    """
    This is the base class for loading and compiling the GLSL shaders.
    """

    def __init__(self, name='phong'):
        """
        Initialises the shaders
        :param vertex_shader: the name of the file containing the vertex shader GLSL code
        :param fragment_shader: the name of the file containing the fragment shader GLSL code
        """

        BaseShaderProgram.__init__(self, name=name)

        # storing uniforms in a dictionary.
        self.uniforms = {
            'PVM': Uniform('PVM'),  # project view model matrix
            'VM': Uniform('VM'),  # view model matrix (necessary for light computations)
            'VMiT': Uniform('VMiT'),  # inverse-transpose of the view model matrix (for normal transformation)
            'mode': Uniform('mode', 0),
            # rendering mode (only for illustration, in general want one shader program per mode)
            'alpha': Uniform('alpha', 1.0),
            # rendering mode (only for illustration, in general want one shader program per mode)
            'Ka': Uniform('Ka'),  # ambient component
            'Kd': Uniform('Kd'),  # diffuse component
            'Ks': Uniform('Ks'),  # specular component
            'Ns': Uniform('Ns'),  # specular highlights
            'light': Uniform('light', np.array([0., 0., 0.], 'f')),
            'Ia': Uniform('Ia'),  # ambient illumination
            'Id': Uniform('Id'),  # diffuse illumination
            'Is': Uniform('Is'),  # specular illumination
            'has_texture': Uniform('has_texture'),
            'textureObject': Uniform('textureObject')

        }

    def bind(self, model, M):
        """
        Call this function to enable this GLSL Program (you can have multiple GLSL programs used during rendering!)
        """

        P = model.scene.P
        V = model.scene.camera.V

        # tell OpenGL to use this shader program for rendering
        glUseProgram(self.program)

        # set the PVM matrix uniform
        self.uniforms['PVM'].bind(np.matmul(P, np.matmul(V, M)))

        # set the PVM matrix uniform
        self.uniforms['VM'].bind(np.matmul(V, M))

        # set the PVM matrix uniform
        self.uniforms['VMiT'].bind(np.linalg.inv(np.matmul(V, M))[:3, :3].transpose())

        # bind the mode to the program
        self.uniforms['mode'].bind(model.scene.mode)

        self.uniforms['alpha'].bind(model.mesh.material.alpha)

        if len(model.mesh.textures) > 0:
            # bind the texture(s)
            self.uniforms['textureObject'].bind(0)
            self.uniforms['has_texture'].bind(1)
        else:
            self.uniforms['has_texture'].bind(0)

        # bind material properties
        self.bind_material_uniforms(model.mesh.material)

        # bind the light properties
        self.bind_light_uniforms(model.scene.light, V)

    def bind_light_uniforms(self, light, V):
        self.uniforms['light'].bind_vector(unhomog(np.dot(V, homog(light.position))))
        self.uniforms['Ia'].bind_vector(np.array(light.Ia, 'f'))
        self.uniforms['Id'].bind_vector(np.array(light.Id, 'f'))
        self.uniforms['Is'].bind_vector(np.array(light.Is, 'f'))

    def bind_material_uniforms(self, material):
        self.uniforms['Ka'].bind_vector(np.array(material.Ka, 'f'))
        self.uniforms['Kd'].bind_vector(np.array(material.Kd, 'f'))
        self.uniforms['Ks'].bind_vector(np.array(material.Ks, 'f'))
        self.uniforms['Ns'].bind_float(material.Ns)

    def add_uniform(self, name):
        if name in self.uniforms:
            print('(W) Warning re-defining already existing uniform %s' % name)
        self.uniforms[name] = Uniform(name)

    def unbind(self):
        glUseProgram(0)


class FlatShader(PhongShader):
    def __init__(self):
        PhongShader.__init__(self, name='flat')
