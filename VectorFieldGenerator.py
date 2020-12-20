import bpy
from math import *

def polynomial(x,y):
    return x**2 + y**3 + 2*x + 4*x*y

def polyangle(x,y):
    try:
        return atan2(-10*sin(x/3) ,y) 
    except:
        return 0

def magfcn(x,y):
    return sqrt(pow(10*sin(x/3),2) + y**2)

def genVectorField():
    for x in range(-20,12):
        for y in range(-10,10):
            rot_z = polyangle(x,y)
            mag = abs(remap(polynomial(x,y),0,1000,0,1))
            print(mag)
            temp = arrow.copy()
            temp.location = [3*x,3*y,0]
            temp.rotation_euler = [0,0,rot_z]
            arrows.append(temp)
            bpy.data.collections['Stuff'].objects.link(temp)

def remap(val,min1,max1,min2,max2):
    return min2 + (val - min1) *(max2 - min2)/(max1 - min1)

index = 0
arrow = bpy.data.objects['Vector']
arrows = []

#genVectorField()

scene = bpy.context.scene
arrows = bpy.data.collections['Stuff'].objects 
sphere = bpy.data.objects['Bob']
pts = bpy.data.collections['Points'].objects 
dt = 0.1
dr = 0.01
affect = 1

for frame in range(0,800):
    for pt in pts:
        if('Vec' in pt.name):
            continue
        x,y,z = pt.location
        rot_z = affect*polyangle(x,y) 
        pt.location = [x + magfcn(x,y)*dr*cos(rot_z), y + magfcn(x,y)*dr*sin(rot_z),0]
        pt.children[0].data.shape_keys.key_blocks['magni'].value = remap(magfcn(x,y),0,100,0,2)
        pt.children[0].data.shape_keys.key_blocks['magni'].keyframe_insert(data_path="value")
        pt.rotation_euler = [0,0,rot_z]
        pt.keyframe_insert(data_path='location', frame=frame)
        pt.keyframe_insert(data_path='rotation_euler',index=2, frame=frame) 
    for arrowIndex in range(len(arrows)):
        
        x,y,z = arrows[arrowIndex].location
        z = remap(magfcn(x,y),0,50,-1,1)
        arrows[arrowIndex].location = [x,y,z]
        rot_z = affect*polyangle(x,y)
        arrows[arrowIndex].rotation_euler = [0,0,rot_z]
        arrows[arrowIndex].keyframe_insert(data_path='rotation_euler', index=2, frame=frame)
