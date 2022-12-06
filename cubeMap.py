from texture import *


class CubeMap(Texture):
    """
    Class for handling a cube map texture.
    """
    def __init__(self, name=None, files=None, wrap=GL_CLAMP_TO_EDGE, sample=GL_LINEAR, format=GL_RGBA, type=GL_UNSIGNED_BYTE):
        """
        Initialise the cube map texture object
        :param name: If a name is provided, the function will load the faces of the cube from files on the disk in a
        folder of this name
        :param files: If provided, a dictionary containing for each cube face ID the file name to load the texture from
        :param wrap: Which texture wrapping method to use. Default is GL_CLAMP_TO_EDGE which is best for cube maps
        :param sample: Which sampling to use, default is GL_LINEAR
        :param format: The pixel format of the image and texture (GL_RGBA)
        :param type: The data format for the texture. Default is GL_UNSIGNED_BYTE
        """
        self.name = name
        self.format = format
        self.type = type
        self.wrap = wrap
        self.sample = sample
        self.target = GL_TEXTURE_CUBE_MAP # set the texture target as a cube map

        # This dictionary contains the file name for each face
        self.files = {
            GL_TEXTURE_CUBE_MAP_NEGATIVE_X: 'left.bmp',
            GL_TEXTURE_CUBE_MAP_POSITIVE_Z: 'back.bmp',
            GL_TEXTURE_CUBE_MAP_POSITIVE_X: 'right.bmp',
            GL_TEXTURE_CUBE_MAP_NEGATIVE_Z: 'front.bmp',
            GL_TEXTURE_CUBE_MAP_POSITIVE_Y: 'bottom.bmp',
            GL_TEXTURE_CUBE_MAP_NEGATIVE_Y: 'top.bmp',
        }

        # generate the texture.
        self.textureid = glGenTextures(1)

        # bind the texture
        self.bind()

        # if name is provided, load cube faces from images on disk
        if name is not None:
            self.set(name, files)

        # set what happens for texture coordinates outside [0,1]
        glTexParameteri(self.target, GL_TEXTURE_WRAP_S, wrap)
        glTexParameteri(self.target, GL_TEXTURE_WRAP_T, wrap)

        # set how sampling from the texture is done.
        glTexParameteri(self.target, GL_TEXTURE_MAG_FILTER, sample)
        glTexParameteri(self.target, GL_TEXTURE_MIN_FILTER, sample)

        # unbind the texture
        self.unbind()

    def set(self, name, files=None):
        """
        Load the cube's faces from images on the disk
        :param name: The folder in which the images are.
        :param files: A dictionary containing the file name for each face.
        """

        if files is not None:
            self.files = files

        for (key, value) in self.files.items():
            print('Loading texture: texture/{}/{}'.format(name, value))
            img = ImageWrapper('{}/{}'.format(name, value))

            # convert the python image object to a plain byte array for passing to OpenGL
            glTexImage2D(key, 0, self.format, img.width(), img.height(), 0, self.format, self.type, img.data(self.format))
