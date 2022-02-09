#Dylan Tom
# andrew id: dtom

# editted from the panda3D example RoamingRalph
# which was made by Ryan Myers, and models made by Jeff Styers, Reagan Heller

from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import CollisionHandlerQueue, CollisionRay
from panda3d.core import Filename, AmbientLight, DirectionalLight
from panda3d.core import PandaNode, NodePath, Camera, TextNode, GeomNode
from panda3d.core import CollideMask
from direct.gui.OnscreenText import OnscreenText
from direct.actor.Actor import Actor
import random
import sys
import os
import math

class FlyThroughAir(ShowBase):
    # method completely taken from RoamingRalph demo:
    def addInstructions(self, pos, msg):
        return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1), scale=.05,
                            shadow=(0, 0, 0, 1), parent=base.a2dTopLeft,
                            pos=(0.08, -pos - 0.04), align=TextNode.ALeft)

    def setUpFlyingInstructions(self):
        self.inst[0] = self.addInstructions(.06, "Arrow Keys to move around")
        self.inst[1] = self.addInstructions(.12, "w and s to control pitch")
        self.inst[2] = self.addInstructions(.18, "a and d to control yaw")
        self.inst[3] = self.addInstructions(.24, "h to switch to driving mode")
        self.inst[4] = self.addInstructions(.3, "mouse click to add object")

    def destroyInstructions(self):
        # got way to destroy text from:
        # https://www.panda3d.org/manual/index.php/OnscreenText
        for element in self.inst:
            element.destroy()

    def setUpTreeButton(self):
        pass

    def setUpDrivingInstructions(self):
        self.inst[0] = self.addInstructions(.06, "Right arrow and left arrow to turn")
        self.inst[1] = self.addInstructions(.12, "Forward and Backward arrow to go forward and backward")
        self.inst[2] = self.addInstructions(.18, "h to switch to add object mode")

    def __init__(self):
        # Set up the window, camera, etc.
        ShowBase.__init__(self)

        # Set the background color to black
        self.win.setClearColor((0, 1, 1, 1))

        # This is used to store which keys are currently pressed.
        self.keyMap = {
            "left": 0, "right": 0, "forward": 0, "cam-left": 0, "cam-right": 0,
            "backward": 0, "cam-up": 0, "cam-down": 0, "add-car": 0,
            "switch-mode":0, "mouse-click":0}

        # this is the egg that came with the module
        # environ = loader.loadModel("models/world")
        # this is the one I created using mountainMaker.py
        self.environ = loader.loadModel("TestMountain1")
        self.environ.reparentTo(render)

        self.car = loader.loadModel("TestCar")
        #self.car = loader.loadModel("testModel/ball")
        self.car.reparentTo(render)

        #instructions
        self.inst = [""]*5
        self.setUpFlyingInstructions()

        # for adjusting so that the position is the center of the car
        self.adjustedXForCenter = 10/2
        self.adjustedYForCenter = 20/2

        # important for setting the size relative to everything else
        # found it here : https://www.panda3d.org/manual/index.php/Common_State_Changes
        # set the mode that the player is currently in
        self.mode = 0
        self.modeFly = 0
        self.modeRace = 1

        # to ensure that when pressing h it only switches once each press
        self.hasSwitched = False

        self.carPositionX = 10
        self.carPositionY = 10
        self.carPositionZ = 100
        # note for rotating camera: from this website: 
        # https://www.panda3d.org/manual/index.php/Common_State_Changes
        # setHpr(Yaw, Pitch, Roll)

        # setting up initial conditions for which way camera is rotated
        self.carYaw = 0
        self.carPitch = 0

        self.setUpCarCollider()
        self.setUpMouseCollider()

        # make the rocks and other stuff that will show up
        self.objects = []

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

        # adding car
        self.accept("mouse1", self.setKey, ["mouse-click", True])
        self.accept("mouse1-up", self.setKey, ["mouse-click", False])

        # setting up orientation of the camera
        self.accept("a", self.setKey, ["cam-left", True])
        self.accept("s", self.setKey, ["cam-down", True])
        self.accept("a-up", self.setKey, ["cam-left", False])
        self.accept("s-up", self.setKey, ["cam-down", False])
        self.accept("d", self.setKey, ["cam-right", True])
        self.accept("d-up", self.setKey, ["cam-right", False])
        self.accept("w", self.setKey, ["cam-up", True])
        self.accept("w-up", self.setKey, ["cam-up", False])


        # to switch between tasks
        self.accept("h", self.setKey, ["switch-mode", True])
        self.accept("h-up", self.setKey, ["switch-mode", False])

        taskMgr.add(self.move, "moveTask")

        # Game state variables
        self.isMoving = False

        self.cameraPositionX = 0
        self.cameraPositionY = 0
        self.cameraPositionZ = 0
        # note for rotating camera: from this website: 
        # https://www.panda3d.org/manual/index.php/Common_State_Changes
        # setHpr(Yaw, Pitch, Roll)
        
        # setting up initial conditions for which way camera is rotated
        self.cameraYaw = 0
        self.cameraPitch = 0
        
        # Set up the camera
        self.disableMouse()
        
        # should probably clean up these magic numbers
        self.camera.setPos(20, 20, 20)


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

    def setUpCarCollider(self):
        self.carCollideTrav = CollisionTraverser()
        base.cTrav = self.carCollideTrav
        self.handler = CollisionHandlerQueue()
        self.carRay = CollisionRay(self.carPositionX, self.carPositionY, 
                                   self.carPositionZ, 0, 0, -1)
        self.carCollision = CollisionNode("groundCollision")
        self.carCollision.addSolid(self.carRay)
        # add to .egg <Scalar> collide-mask { 0x0 }
        #self.carCollision.setFromCollideMask(CollideMask.bit(0))
        #self.carCollision.setIntoCollideMask(CollideMask.allOff())
        self.carCollisionNode = self.car.attachNewNode(self.carCollision)
        self.carCollideTrav.addCollider(self.carCollisionNode, self.handler)
        self.carCollisionNode.show()

    def setUpMouseCollider(self):
        # clicking on objects stuff came from here:
        # https://www.panda3d.org/manual/index.php/Collision_Traversers
        # https://www.panda3d.org/manual/index.php/Collision_Handlers
        # will not use the traverser set up by car because slow
        # instead we will render each time clicked
        self.mouseCollideTrav = CollisionTraverser("mouseTraverse")
        self.mousehandler = CollisionHandlerQueue()
        # edit this so that from Object is the camera
        # self.mouseCollideTrav.addCollider(fromObject, queue)
        # self.mouseCollideTrav.traverse(render)
        # this next part came from:
        # https://www.panda3d.org/manual/index.php/Clicking_on_3D_Objects
        pickerNode = CollisionNode("mouseRay")
        pickerNp = camera.attachNewNode(pickerNode)
        pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.pickerRay = CollisionRay()
        pickerNode.addSolid(self.pickerRay)
        self.mouseCollideTrav.addCollider(pickerNp, self.mousehandler)
        

    # Records the state of the arrow keys
    def setKey(self, key, value):
        self.keyMap[key] = value

    def move(self, task):
        if(self.mode==self.modeFly):
            # Get the time that elapsed since last frame.  We multiply this with
            # the desired speed in order to find out with which distance to move
            # in order to achieve that desired speed.
            dt = globalClock.getDt()

            if self.keyMap["switch-mode"] and not self.hasSwitched:
                self.mode = (self.mode+1)%2
                self.destroyInstructions()
                self.setUpDrivingInstructions()
                self.hasSwitched = True
            elif not self.keyMap["switch-mode"]:
                self.hasSwitched = False

            # the angle is in degrees with 360 equal to full rotation
            angleAdjustment = 100
            if self.keyMap["cam-left"]:
                self.cameraYaw += angleAdjustment*dt
            if self.keyMap["cam-right"]:
                self.cameraYaw -= angleAdjustment*dt
            if self.keyMap["cam-up"]:
                self.cameraPitch += angleAdjustment*dt
            if self.keyMap["cam-down"]:
                self.cameraPitch -= angleAdjustment*dt

            positionAdjustment = 500
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

    
            # clicking on 3D objects comes from here:
            # https://www.panda3d.org/manual/index.php/Clicking_on_3D_Objects
            # checks if it needs to add any objects:
            if(self.keyMap["mouse-click"]):
                # found way to speed this up by only doing collision check
                # when mouse clicked by not using cTrav like in this method
                # the way I did it I found here:
                # https://www.panda3d.org/manual/index.php/Clicking_on_3D_Objects
                self.mouseCollideTrav.traverse(render)
                if(base.mouseWatcherNode.hasMouse()):
                    mousePos = base.mouseWatcherNode.getMouse()
                    self.pickerRay.setFromLens(base.camNode, mousePos.getX(), mousePos.getY())
                    if(self.mousehandler.getNumEntries()>0):
                        entries = list(self.mousehandler.getEntries())
                        # pathagorean formula for sorting
                        entries.sort(key=lambda x: ((x.getSurfacePoint(render).getX(
                                    )-self.cameraPositionX)**2 + 
                                    (x.getSurfacePoint(render).getY()-
                                    self.cameraPositionY)**2)**.5)
                        newX = entries[0].getSurfacePoint(render).getX()
                        newY = entries[0].getSurfacePoint(render).getY()
                        newZ = entries[0].getSurfacePoint(render).getZ()
                        self.objects.append(loader.loadModel("TestCar.egg"))
                        self.objects[len(self.objects)-1].reparentTo(render)
                        self.objects[len(self.objects)-1].setPos(newX, newY, newZ)
            return task.cont
        elif(self.mode == self.modeRace):
            # Get the time that elapsed since last frame.  We multiply this with
            # the desired speed in order to find out with which distance to move
            # in order to achieve that desired speed.
            dt = globalClock.getDt()

            degreeAdjustment = 60
            positionAdjustment = 100
            # should switch rad and Deg in variable name
            radToDeg = math.pi/180
            # the x and y component of left and right moves, do not need to 
            # compensate in z axis because not doing any roll, so there should be 
            # no zComponent

            xComponent = math.sin(self.carYaw*radToDeg)
            yComponent = math.cos(self.carYaw*radToDeg)

            if self.keyMap["switch-mode"] and not self.hasSwitched:
                self.mode = (self.mode+1)%2
                self.destroyInstructions()
                self.setUpFlyingInstructions()
                self.hasSwitched = True
            elif not self.keyMap["switch-mode"]:
                self.hasSwitched = False

            if self.keyMap["left"]:
                self.carYaw += degreeAdjustment * dt
            if self.keyMap["right"]:
                self.carYaw -= degreeAdjustment * dt
            if self.keyMap["forward"]:
                self.carPositionX -= positionAdjustment * dt*xComponent
                self.carPositionY += positionAdjustment * dt*yComponent
            if self.keyMap["backward"]:
                self.carPositionX += positionAdjustment * dt*xComponent
                self.carPositionY -= positionAdjustment * dt*yComponent

            # need to consider both the x and y component of offset for both
            # because x slowly changes to y as it turns

            actualXPos = (self.carPositionX+self.adjustedXForCenter*
                          math.cos(radToDeg*self.carYaw)+self.adjustedYForCenter
                          *math.sin(radToDeg*self.carYaw))
            actualYPos = (self.carPositionY+self.adjustedYForCenter*
                          math.cos(radToDeg*self.carYaw)+self.adjustedXForCenter
                          *math.sin(radToDeg*self.carYaw))
            self.car.setX(actualXPos)
            self.car.setY(actualYPos)
            self.car.setZ(self.carPositionZ)
            self.car.setHpr(self.carYaw, self.carPitch, 0)

            # when implementing the use of the mouse look here:
            # https://www.panda3d.org/manual/index.php/Clicking_on_3D_Objects
            
            # almost directly taken from ralph example
            entries = list(self.handler.getEntries())
            entries.sort(key=lambda x: x.getSurfacePoint(render).getZ())
            # worry about which thing it collides with later
            if (len(entries) > 0):
                # and entries[0].getIntoNode().getName() == "mountainCollide":
                self.carPositionZ = (entries[0].getSurfacePoint(render).getZ())
            else:
                # because at 100 everything should be below car and do not want
                # to continually go up or else it may go up forever. 
                self.car.setZ(100)
                print("less")
            
            # Modify view of camera so that it is behind car
            distanceBehind = 40
            distanceAbove = 20
            self.camera.setHpr(self.carYaw, -.5, 0)
            camX = actualXPos + distanceBehind * math.sin(radToDeg*self.carYaw)
            camY = actualYPos - distanceBehind * math.cos(radToDeg*self.carYaw)
            camZ = self.carPositionZ + distanceAbove
            self.camera.setPos(camX, camY, camZ)
            return task.cont

demo = FlyThroughAir()
demo.run()
