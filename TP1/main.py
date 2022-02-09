#Dylan Tom
# andrew id: dtom
# before running this make sure to run mountainMaker.py so that the landscape is generated


# editted from the panda3D example RoamingRalph
# which was made by Ryan Myers, and models made by Jeff Styers, Reagan Heller

from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import CollisionHandlerQueue, CollisionRay
from panda3d.core import Filename, AmbientLight, DirectionalLight
from panda3d.core import PandaNode, NodePath, Camera, TextNode
from panda3d.core import CollideMask
from direct.gui.OnscreenText import OnscreenText
from direct.actor.Actor import Actor
import random
import sys
import os
import math

class FlyThroughAir(ShowBase):
    def __init__(self):
        # Set up the window, camera, etc.
        ShowBase.__init__(self)

        # Set the background color to black
        self.win.setClearColor((1, 1, 1, 1))

        # This is used to store which keys are currently pressed.
        self.keyMap = {
            "left": 0, "right": 0, "forward": 0, "cam-left": 0, "cam-right": 0,
            "backward": 0, "cam-up": 0, "cam-down": 0}

        # this is the egg that came with the module
        # environ = loader.loadModel("models/world")
        # this is the one I created using mountainMaker.py
        environ = loader.loadModel("TestMountain")
        environ.reparentTo(render)

        # Accept the control keys for movement and rotation

        #setting up keys for movement
        self.accept("escape", sys.exit)
        self.accept("arrow_left", self.setKey, ["left", True])
        self.accept("arrow_right", self.setKey, ["right", True])
        self.accept("arrow_up", self.setKey, ["forward", True])
        self.accept("arrow_down", self.setKey, ["backward", True])
        self.accept("arrow_left-up", self.setKey, ["left", False])
        self.accept("arrow_right-up", self.setKey, ["right", False])
        self.accept("arrow_up-up", self.setKey, ["forward", False])
        self.accept("arrow_down-up", self.setKey, ["backward", False])
        
        
        # setting up orientation of the camera
        self.accept("a", self.setKey, ["cam-left", True])
        self.accept("s", self.setKey, ["cam-down", True])
        self.accept("a-up", self.setKey, ["cam-left", False])
        self.accept("s-up", self.setKey, ["cam-down", False])
        self.accept("d", self.setKey, ["cam-right", True])
        self.accept("d-up", self.setKey, ["cam-right", False])
        self.accept("w", self.setKey, ["cam-up", True])
        self.accept("w-up", self.setKey, ["cam-up", False])

        taskMgr.add(self.move, "moveTask")

        # Game state variables
        self.isMoving = False

        self.cameraPositionX = 5
        self.cameraPositionY = 5
        self.cameraPositionZ = 8
        # note for rotating camera: from this website: 
        # https://www.panda3d.org/manual/index.php/Common_State_Changes
        # setHpr(Yaw, Pitch, Roll)
        
        # setting up initial conditions for which way camera is rotated
        self.cameraYaw = 0
        self.cameraPitch = 0
        
        # Set up the camera
        self.disableMouse()
        
        # should probably clean up these magic numbers
        self.camera.setPos(5, 5, 8)


        # Create some lighting
        # this is a part that is completely unchanged from demo
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor((.3, .3, .3, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection((-5, -5, -5))
        directionalLight.setColor((1, 1, 1, 1))
        directionalLight.setSpecularColor((1, 1, 1, 1))
        render.setLight(render.attachNewNode(ambientLight))
        render.setLight(render.attachNewNode(directionalLight))

    # Records the state of the arrow keys
    def setKey(self, key, value):
        self.keyMap[key] = value

    def move(self, task):

        # Get the time that elapsed since last frame.  We multiply this with
        # the desired speed in order to find out with which distance to move
        # in order to achieve that desired speed.
        dt = globalClock.getDt()

        # the angle is in degrees with 360 equal to full rotation
        angleAdjustment = 20
        if self.keyMap["cam-left"]:
            self.cameraYaw += angleAdjustment*dt
        if self.keyMap["cam-right"]:
            self.cameraYaw -= angleAdjustment*dt
        if self.keyMap["cam-up"]:
            self.cameraPitch += angleAdjustment*dt
        if self.keyMap["cam-down"]:
            self.cameraPitch -= angleAdjustment*dt
        
        positionAdjustment = 100
        # should switch rad and Deg in variable name
        radToDeg = math.pi/180
        # the x and y component of left and right moves, do not need to 
        # compensate in z axis because not doing any roll, so there should be 
        # no zComponent
        xComponent = math.cos(self.cameraYaw*radToDeg)
        yComponent = math.sin(self.cameraYaw*radToDeg)
        
        if self.keyMap["left"]:
            self.cameraPositionX -= positionAdjustment * dt *xComponent
            self.cameraPositionY -= positionAdjustment * dt *yComponent
        if self.keyMap["right"]:
            self.cameraPositionX += positionAdjustment * dt*xComponent
            self.cameraPositionY += positionAdjustment * dt*yComponent
            
        # for going forward, the orientation is rotated 90 degrees so need to 
        # change components
        xComponent = math.cos(self.cameraYaw*radToDeg+math.pi/2)*math.cos(
                                                      self.cameraPitch*radToDeg)
        yComponent = math.sin(self.cameraYaw*radToDeg+math.pi/2)*math.cos(
                                                      self.cameraPitch*radToDeg)
        zComponent = math.sin(self.cameraPitch*radToDeg)
        
        if self.keyMap["forward"]:
            self.cameraPositionX += positionAdjustment * dt*xComponent
            self.cameraPositionY += positionAdjustment * dt*yComponent
            self.cameraPositionZ += positionAdjustment * dt*zComponent
        if self.keyMap["backward"]:
            self.cameraPositionX -= positionAdjustment * dt*xComponent
            self.cameraPositionY -= positionAdjustment * dt*yComponent
            self.cameraPositionZ -= positionAdjustment * dt*zComponent
        
        self.camera.setX(self.cameraPositionX)
        self.camera.setY(self.cameraPositionY)
        self.camera.setZ(self.cameraPositionZ)
        self.camera.setHpr(self.cameraYaw, self.cameraPitch, 0)

        # when implementing the use of the mouse look here:
        # https://www.panda3d.org/manual/index.php/Clicking_on_3D_Objects

        return task.cont


demo = FlyThroughAir()
demo.run()
