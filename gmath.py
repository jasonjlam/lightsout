import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #       The fist index (LOCATION) represents the vector to the light.
  #       The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    normalize(normal)
    normalize(light[0])
    ambient_light = calculate_ambient(ambient, areflect)
    diffuse_light = calculate_diffuse(light, dreflect, normal)
    specular_light = calculate_specular(light, sreflect, view, normal)
    print("Ambient light:{}".format(ambient_light))
    print("Diffuse light:{}".format(diffuse_light))
    print("Specular light:{}".format(specular_light))
    lights = list_addition(ambient_light, list_addition(specular_light, diffuse_light))
    print(lights)
    limit_color(lights)
    return lights

def calculate_ambient(alight, areflect):
    return list_multi(alight, areflect)


def calculate_diffuse(light, dreflect, normal):
    nl = dot_product_pos(normal, light[0])
    new_light = []
    for i in range(3):
        new_light.append(nl * light[1][i])
        print(new_light[i], nl)
    return list_multi(dreflect, new_light)

def calculate_specular(light, sreflect, view, normal):
    nl = dot_product_pos(normal, light[0]) * 2
    specular = []
    for i in range(3):
        specular.append (nl * normal[i])
    specular = list_subtraction(specular, light[0])
    ms = dot_product_pos(specular, view)** 3
    temp = list_multi(light[1], sreflect)
    for i in range(3):
        temp[i] *= ms
    return temp

def limit_color(color):
    for i in range(3):
        if color[i] > 255:
            color[i] = 255
        elif color[i] < 0:
            color[i] = 0
        else:
            color[i] = int(color[i])

def list_multi(l0, l1):
    l2 = []
    for i in range(len(l1)):
        l2.append(l0[i] * l1[i])
    return l2

def list_subtraction(l0, l1):
    l2 = []
    for i in range(len(l1)):
        l2.append(l0[i] - l1[i])
    return l2

def list_addition(l0, l1):
    l2 = []
    for i in range(len(l1)):
        l2.append(l0[i] + l1[i])
    return l2

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

def dot_product_pos(a,b):
    dotproduct = dot_product(a,b)
    if dotproduct < 0:
        return 0
    else:
        return dotproduct
#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
