#version 130

//=== in attributes are read from the vertex array, one row per instance of the shader
in vec3 position;	// the position attribute contains the vertex position
in vec2 texCoord;	// the texture coordinates

//=== out attributes are interpolated on the face, and passed on to the fragment shader
out vec2 fragment_texCoord;

void main(void)
{
	gl_Position = vec4(position,1); // just display on the screen, no projection
	fragment_texCoord = texCoord;	// pass the texture coordinates on
}
