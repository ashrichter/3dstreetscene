from mesh import Mesh

from shaders import *


class BaseModel:
    """
    Base class for all models, implementing the basic draw function for triangular meshes.
    Inherit from this to create new models.
    """

    def __init__(self, scene, M=poseMatrix(), mesh=Mesh(), color=[1., 1., 1.], primitive=GL_TRIANGLES, visible=True):
        """
        Initialises the model data
        """

        print('+ Initializing {}'.format(self.__class__.__name__))

        # if flag set to False, model is not rendered
        self.visible = visible

        # store the scene reference
        self.scene = scene

        # store the type of primitive to draw
        self.primitive = primitive

        # store the object's colour (deprecated now that we have per-vertex colours)
        self.color = color

        # store the shader program for rendering model
        self.shader = None

        # mesh data
        self.mesh = mesh

        self.name = self.mesh.name

        # dict of vertex buffer objects
        self.vbos = {}

        # dict of attributes
        self.attributes = {}

        # store the position of the model in the scene
        self.M = M

        # Vertex Array Object to pack all buffers for rendering in the GPU
        self.vao = glGenVertexArrays(1)

        # buffer to store indices using shared vertex representation
        self.index_buffer = None

    def initialise_vbo(self, name, data):
        print('Initialising VBO for attribute {}'.format(name))

        if data is None:
            print('(W) Warning in {}.bind_attribute(): Data array for attribute {} is None!'.format(
                self.__class__.__name__, name))
            return

        # bind the location of the attribute in the GLSL program to the next index
        # the name of the location must correspond to an 'in' variable in the GLSL vertex shader code
        self.attributes[name] = len(self.vbos)

        # create a buffer object
        self.vbos[name] = glGenBuffers(1)
        # and bind it
        glBindBuffer(GL_ARRAY_BUFFER, self.vbos[name])

        # enable the attribute
        glEnableVertexAttribArray(self.attributes[name])

        # Associate the bound buffer to the corresponding input location in the shader
        # Each instance of the vertex shader will get one row of the array for parallel processing
        glVertexAttribPointer(index=self.attributes[name], size=data.shape[1], type=GL_FLOAT, normalized=False,
                              stride=0, pointer=None)

        # set the data in the buffer as the vertex array
        glBufferData(GL_ARRAY_BUFFER, data, GL_STATIC_DRAW)

    def bind_shader(self, shader):
        """
        If a new shader is bound, re-link it to ensure attributes are correctly linked.
        """
        if self.shader is None or self.shader.name is not shader:
            if isinstance(shader, str):
                self.shader = PhongShader(shader)
            else:
                self.shader = shader

            # bind all attributes and compile the shader
            self.shader.compile(self.attributes)

    def bind(self):
        """
        This method stores the vertex data in a Vertex Buffer Object (VBO) that can be uploaded
        to the GPU at render time.
        """

        # bind the Vertex Array Object to retrieve all buffers and rendering context
        glBindVertexArray(self.vao)

        if self.mesh.vertices is None:
            print('(W) Warning in {}.bind(): No vertex array!'.format(self.__class__.__name__))

        # initialise vertex position VBO and link to shader program attribute
        self.initialise_vbo('position', self.mesh.vertices)
        self.initialise_vbo('normal', self.mesh.normals)
        self.initialise_vbo('color', self.mesh.colors)
        self.initialise_vbo('texCoord', self.mesh.textureCoords)
        self.initialise_vbo('tangent', self.mesh.tangents)
        self.initialise_vbo('binormal', self.mesh.binormals)

        # if indices are provided, put them in a buffer too
        if self.mesh.faces is not None:
            self.index_buffer = glGenBuffers(1)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.index_buffer)
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.mesh.faces, GL_STATIC_DRAW)

        # finally we unbind the VAO and VBO when we're done to avoid side effects
        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def draw(self, Mp=poseMatrix()):
        """
        Draws the model using OpenGL functions.
        :param Mp: The model matrix of the parent object, for composite objects.
        :param shaders: the shader program to use for drawing
        """

        if self.visible:

            if self.mesh.vertices is None:
                print('(W) Warning in {}.draw(): No vertex array!'.format(self.__class__.__name__))

            # bind the Vertex Array Object so that all buffers are bound correctly and following operations affect them
            glBindVertexArray(self.vao)

            # setup the shader program and provide it the Model, View and Projection matrices to use
            # for rendering this model
            self.shader.bind(
                model=self,
                M=np.matmul(Mp, self.M)
            )

            # bind all textures, shader needs to handle each one with a sampler object.
            for unit, tex in enumerate(self.mesh.textures):
                glActiveTexture(GL_TEXTURE0 + unit)
                tex.bind()

            # check whether the data is stored as vertex array or index array
            if self.mesh.faces is not None:
                # draw the data in the buffer using the index array
                glDrawElements(self.primitive, self.mesh.faces.flatten().shape[0], GL_UNSIGNED_INT, None)
            else:
                # draw the data in the buffer using the vertex array ordering only.
                glDrawArrays(self.primitive, 0, self.mesh.vertices.shape[0])

            # unbind the shader to avoid side effects
            glBindVertexArray(0)

    def vbo__del__(self):
        """
        Release all VBO objects when finished.
        """
        for vbo in self.vbos.items():
            glDeleteBuffers(1, vbo)

        glDeleteVertexArrays(1, self.vao.tolist())


class DrawModelFromMesh(BaseModel):
    """
    Base class for all models, inherit from this to create new models
    """

    def __init__(self, scene, M, mesh, name=None, shader=None, visible=True):
        """
        Initialises the model data
        """

        BaseModel.__init__(self, scene=scene, M=M, mesh=mesh, visible=visible)

        if name is not None:
            self.name = name

        # and we check which primitives we need to use for drawing
        if self.mesh.faces.shape[1] == 3:
            self.primitive = GL_TRIANGLES

        elif self.mesh.faces.shape[1] == 4:
            self.primitive = GL_QUADS

        else:
            print(
                '(E) Error in DrawModelFromObjFile.__init__(): index array must have 3 (triangles) or 4 (quads) '
                'columns, found {}!'.format(
                    self.indices.shape[1]))

        self.bind()

        if shader is not None:
            self.bind_shader(shader)
