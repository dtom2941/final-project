# Dylan Tom
# andrew id: dtom
# section O

# editted from the panda3D example RoamingRalph that came with panda3D
# which was made by Ryan Myers, and models made by Jeff Styers, Reagan Heller

from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import CollisionHandlerQueue, CollisionRay, CollisionTube
from panda3d.core import Filename, AmbientLight, DirectionalLight, PointLight
from panda3d.core import PandaNode, NodePath, Camera, TextNode, GeomNode
from panda3d.core import CollideMask
from direct.gui.OnscreenText import OnscreenText
from direct.actor.Actor import Actor
from direct.gui.DirectGui import *
from panda3d.core import CullFaceAttrib
from EggMaker import EggObject, Mountain, Car, Pole
import random, time
import sys
import os
import math

class RacingGame(ShowBase):
    # method completely taken from RoamingRalph demo:
    def addInstructions(self, pos, msg):
        return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1), scale=.05,
                            shadow=(0, 0, 0, 1), parent=base.a2dTopLeft,
                            pos=(0.08, -pos - 0.04), align=TextNode.ALeft)

    def addWin(self, time):
        msg = ("You finished the course in: \n%d seconds \n press z to race again"
              % (time))
        self.winText = OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1), scale=.2,
                            shadow=(0, 0, 0, 1), parent=base.a2dTopLeft,
                            pos=(0.10, -0.5), align=TextNode.ALeft)

    def destroyWin(self):
        if(self.winText!=None):
            self.winText.destroy()

    def setUpFlyingInstructions(self):
        self.inst[0] = self.addInstructions(.06, "Arrow Keys to move around")
        self.inst[1] = self.addInstructions(.12, "w and s to control pitch")
        self.inst[2] = self.addInstructions(.18, "a and d to control yaw")
        self.inst[3] = self.addInstructions(.24, "h to switch to driving mode")
        self.inst[4] = self.addInstructions(.3, "mouse click to add object")
        self.inst[5] = self.addInstructions(.36, "m to go to main")

    def startMovement(self):
        taskMgr.add(self.move, "moveTask")

    def destroyInstructions(self):
        # got way to destroy text from:
        # https://www.panda3d.org/manual/index.php/OnscreenText
        for element in self.inst:
            element.destroy()

    def startCreating(self):
        self.switchToCreateMode()
        self.destroyStartScreenButtons()
        self.startMovement()

    def startDriving(self):
        self.switchToDrivingMode()
        self.destroyStartScreenButtons()
        self.startMovement()

    def startTutorial(self):
        self.mode = self.modeTutorial
        self.setUpTutorial()
        self.destroyStartScreenButtons()
        self.startMovement()

    def setUpStartScreenButtons(self):
        self.creatingButton = DirectButton(text="Start Creating", scale=.1, command=self.startCreating, pos=(0,0,.2))
        self.drivingButton = DirectButton(text="Start Driving", scale=.1, command=self.startDriving, pos=(0,0,0))
        self.tutorialButton = DirectButton(text="Start Tutorial", scale=.1, command=self.startTutorial, pos=(0,0,-.2))

    def destroyStartScreenButtons(self):
        self.creatingButton.destroy()
        self.drivingButton.destroy()
        self.tutorialButton.destroy()

    def setAddObjectTree(self):
        self.createdObject = self.createTree
        
    def setAddObjectRock(self):
        self.createdObject = self.createRock
        
    def setAddObjectPole(self):
        self.createdObject = self.createPole

    def setUpCreateButtons(self):
        # todo: add toggle for instructions so that they do not always interfere with button
        self.treeButton = DirectButton(text="Add Block", scale=.1, command=self.setAddObjectTree, pos=(0,0,.85))
        #self.rockButton = DirectButton(text="Add Rock", scale=.1, command=self.setAddObjectRock, pos=(-.5,.9,.85))
        self.poleButton = DirectButton(text="Add Pole", scale=.1, command=self.setAddObjectPole, pos=(.5,0,.85))
        
    def setUpCreateObjects(self):
        self.createdObject = 0
        self.createTree = 0
        self.createRock = 1
        self.createPole = 2
        
    def destroyCreateButtons(self):
        self.treeButton.destroy()
        #self.rockButton.destroy()
        self.poleButton.destroy()

    def setUpDrivingInstructions(self):
        self.inst[0] = self.addInstructions(.06, "Right arrow and left arrow to turn")
        self.inst[1] = self.addInstructions(.12, "Forward and Backward arrow to go forward and backward")
        self.inst[2] = self.addInstructions(.18, "h to switch to add object mode")
        self.inst[3] = self.addInstructions(.24, "z to switch to start the race")
        self.inst[4] = self.addInstructions(.30, "m to go to main")

    def setUpWindow(self):
        # set up the egg files needed
        # since this method is made for python 2.7 but these objects are made for python 3.5, seems to be incompatible
        #m = Mountain("TestMountain", 60)
        #m.editFile()
        #p = Pole("TestPole", 0, 0, 0)
        #p.editFile()
        #c = Car("TestCar", 0,0,0)
        #c.editFile()
        #b = BeaconLight("BeaconLight",0,0,0)
        #b.editFile()
        # Set up the window, camera, etc        
        ShowBase.__init__(self)

        # Set the background color to black
        self.win.setClearColor((0, 1, 1, 1))
        # this is the model I created using mountainMaker.py
        self.environ = loader.loadModel("TestMountain1")
        self.environ.reparentTo(render)

        self.car = loader.loadModel("TestCar")
        # found how to solve the problem of only being able to see objects from
        # certain angles with this: 
        # http://www.panda3d.org/manual/index.php/Backface_Culling_and_Frontface_Culling
        self.car.setTwoSided(True)
        self.car.reparentTo(render)

        # Create some lighting
        # this is a part that is completely unchanged from demo
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor((.3, .3, .3, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection((-5, -5, -5))
        directionalLight.setColor((1, 1, 1, 1))
        directionalLight.setSpecularColor((1, 1, 1, 1))
        # to get light from other direction to light up things on both sides
        directionalLight2 = DirectionalLight("directionalLight")
        directionalLight2.setDirection((5, 5, 5))
        directionalLight2.setColor((1, 1, 1, 1))
        directionalLight2.setSpecularColor((1, 1, 1, 1))
        render.setLight(render.attachNewNode(ambientLight))
        render.setLight(render.attachNewNode(directionalLight))
        render.setLight(render.attachNewNode(directionalLight2))

    def setUpCar(self):
        # for adjusting so that the position is the center of the car
        self.adjustedXForCenter = 10/2
        self.adjustedYForCenter = 20/2

        # for some reason can't change this or the collisions do not work
        self.carPositionX = 20
        self.carPositionY = 20
        self.carPositionZ = 100
        # note for rotating camera: from this website: 
        # https://www.panda3d.org/manual/index.php/Common_State_Changes
        # setHpr(Yaw, Pitch, Roll)

        # setting up initial conditions for which way camera is rotated
        self.carYaw = 0
        self.carPitch = 0
        (actualXPos, actualYPos) = RacingGame.findActualCenter(self,
                                        self.carPositionX, self.carPositionY,
                                        self.adjustedXForCenter,
                                        self.adjustedYForCenter, self.carYaw)
        self.car.setX(actualXPos)
        self.car.setY(actualYPos)
        self.car.setZ(self.carPositionZ)
        self.car.setHpr(self.carYaw, self.carPitch, 0)

    def setUpCamera(self):
        # for flying mode
        self.cameraPositionX = 500
        self.cameraPositionY = 500
        self.cameraPositionZ = 40
        # note for rotating camera: from this website: 
        # https://www.panda3d.org/manual/index.php/Common_State_Changes
        # setHpr(Yaw, Pitch, Roll)
        
        # setting up initial conditions for which way camera is rotated
        self.cameraYaw = 0
        self.cameraPitch = 0
        
        # Set up the camera
        self.disableMouse()
        
        # should probably clean up these magic numbers
        self.camera.setPos(self.cameraPositionX, self.cameraPositionY,
                           self.cameraPositionZ)

    def setUpKeyMap(self):
        # This is used to store which keys are currently pressed.
        self.keyMap = {
            "left": 0, "right": 0, "forward": 0, "cam-left": 0, "cam-right": 0,
            "backward": 0, "cam-up": 0, "cam-down": 0, "add-car": 0,
            "switch-mode":0, "mouse-click":0, "race-start":0, "to-main":0}
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

        self.accept("m", self.setKey, ["to-main", True])
        self.accept("m-up", self.setKey, ["to-main", False])

        # starting race
        self.accept("z", self.setKey, ["race-start", True])
        self.accept("z-up", self.setKey, ["race-start", False])

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

    def __init__(self):
        self.setUpWindow()
        self.setUpKeyMap()
        #instructions
        self.inst = [""]*6
        self.setUpFlyingInstructions()

        self.mouseClicked = False

        self.winText = None

        # important for setting the size relative to everything else
        # found it here : https://www.panda3d.org/manual/index.php/Common_State_Changes
        # set the mode that the player is currently in
        self.mode = 0
        self.modeFly = 2
        self.modeRace = 1
        self.modeStart = 0
        self.modeTutorial = 3
        # to ensure that when pressing h it only switches once each press
        self.hasSwitched = False
        self.raceBegan = False
        self.raceTime = 0
        self.poleOn = 0

        self.setUpCamera()
        self.setUpCar()
        self.setUpCarCollider()
        self.setUpMouseCollider()
        self.setUpStartScreenButtons()
        # make the rocks and other stuff that will show up
        self.setUpCreateObjects()
        self.objects = []
        self.poles = []
        self.beaconLight = None
        self.beaconLightZ = 50
        self.target = None

        taskMgr.add(self.move, "moveTask")

    def findCollisionTube(self):
        # using bassically same formula as Y position
        # decided not to use this because possible problems with ground getting
        # hit instead of things in front
        degToRad = math.pi/180
        xAddition = (self.adjustedXForCenter*math.cos(self.carYaw*degToRad)+
                    self.adjustedYForCenter*math.sin(self.carYaw*degToRad))/2
        yAddition = (self.adjustedXForCenter*math.cos(self.carYaw*degToRad)+
                    self.adjustedYForCenter*math.sin(self.carYaw*degToRad))

    def findCarFrontDir(self):
        degToRad = math.pi/180
        xDir = -1*math.sin(degToRad*self.carYaw)*math.cos(degToRad*self.carPitch)
        yDir = 1*math.cos(degToRad*self.carYaw)*math.cos(degToRad*self.carPitch)
        zDir = 1*math.sin(degToRad*self.carPitch)
        return (xDir, yDir, zDir)

    def setUpCarCollider(self):
        self.carCollideTrav = CollisionTraverser()
        base.cTrav = self.carCollideTrav
        self.handler = CollisionHandlerQueue()
        self.carRay = CollisionRay(self.carPositionX, self.carPositionY, 
                                   self.carPositionZ, 0, 0, -1)
        self.carForwardHandler = CollisionHandlerQueue()
        # so that it doesn't collide with things forward and backward. 
        degToRad = math.pi/180
        (xDir, yDir, zDir) = self.findCarFrontDir()
        self.carRayForward = CollisionRay(self.carPositionX, self.carPositionY,
                                    self.carPositionZ, xDir,yDir, zDir)
        self.carForwardCollision = CollisionNode("forwardCollision")
        self.carForwardCollision.addSolid(self.carRayForward)
        self.carForwardCollision.setIntoCollideMask(CollideMask.allOff())
        self.carForwardCollisionNode = self.car.attachNewNode(self.carForwardCollision)
        (centerX,centerY) = self.findActualCenter(0,0,self.adjustedXForCenter,
                                           self.adjustedYForCenter, self.carYaw)
        self.carRayForward.setOrigin(5,10, 5)
        self.carCollision = CollisionNode("groundCollision")
        self.carCollision.addSolid(self.carRay)
        self.carCollision.setIntoCollideMask(CollideMask.allOff())
        self.carCollisionNode = self.car.attachNewNode(self.carCollision)
        self.carCollideTrav.addCollider(self.carCollisionNode, self.handler)
        self.carCollideTrav.addCollider(self.carForwardCollisionNode, self.carForwardHandler)
        self.carForwardCollisionNode.show()

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
        pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
        pickerNode.setIntoCollideMask(CollideMask.allOff())
        self.pickerRay = CollisionRay()
        pickerNode.addSolid(self.pickerRay)
        pickerNp = camera.attachNewNode(pickerNode)
        self.mouseCollideTrav.addCollider(pickerNp, self.mousehandler)

    # Records the state of the arrow keys
    def setKey(self, key, value):
        self.keyMap[key] = value

    def switchToCreateMode(self):
        self.mode = self.modeFly
        self.destroyInstructions()
        self.setUpFlyingInstructions()
        self.hasSwitched = True
        self.setUpCreateButtons()

    def switchToDrivingMode(self):
        self.mode = self.modeRace
        self.destroyInstructions()
        self.setUpDrivingInstructions()
        self.hasSwitched = True

    def switchToMainMode(self):
        self.mode = 0
        self.setUpStartScreenButtons()

    def setTutorialText(self, str):
        # reusing inst so that it is easy to erase
        self.inst[0] = self.addInstructions(.06, str)

    def move(self, task):
        if(self.keyMap["to-main"]):
            self.switchToMainMode()
        elif(self.mode==self.modeFly):
            if self.keyMap["switch-mode"] and not self.hasSwitched:
                self.switchToDrivingMode()
                self.destroyCreateButtons()
            elif not self.keyMap["switch-mode"]:
                # to ensure switch mode only happens once per button pressed
                self.hasSwitched = False
            self.findNewCameraPosition()
            self.checkAndAddNewObject()
        elif(self.mode == self.modeRace):
            if self.keyMap["switch-mode"] and not self.hasSwitched:
                self.destroyWin()
                self.switchToCreateMode()
            elif not self.keyMap["switch-mode"]:
                # this ensures that when key is pressed only switch states once
                self.hasSwitched = False
            self.findCarNewXandY()
            # when implementing the use of the mouse look here:
            # https://www.panda3d.org/manual/index.php/Clicking_on_3D_Objects
            self.setCarZ()
            self.setCameraPositionBehindCar()
            if(self.keyMap["race-start"] and not self.raceBegan and len(self.poles)>=2):
                self.destroyWin()
                # try so that if there are not enough poles then the game
                # doesn't crash
                try:
                    self.raceBegan = True
                    self.raceTime = time.time()
                    # puts in the car where the first two poles are
                    # first col of poles is model, second x coord, thrid y coord, fourth z coord
                    self.carPositionX = (self.poles[0][1]+self.poles[1][1])/2
                    self.carPositionY = (self.poles[0][2]+self.poles[1][2])/2
                    # meant to show where car should go
                    # got info on how to do point lights from here:
                    # https://www.panda3d.org/manual/index.php/Lighting
                    self.beaconLight = PointLight("beaconLight")
                    self.beaconLight.setColor((1,1,1,1))
                    self.beaconLight.setAttenuation((0,0,1))
                    self.beaconLightHolder = render.attachNewNode(self.beaconLight)
                    (beaconLightX, beaconLightY) = self.getNextGateCenter()
                    # target for driver
                    if(self.target==None):
                        self.target = loader.loadModel("BeaconLight.egg")
                    self.target.setTwoSided(True)
                    self.target.reparentTo(render)
                    if(beaconLightX!=None):
                        self.beaconLightHolder.setPos(beaconLightX, beaconLightY, self.beaconLightZ)
                        render.setLight(self.beaconLightHolder)
                        self.target.setPos(beaconLightX, beaconLightY, self.beaconLightZ)
                except:
                    # not enough poles
                    pass
            if(self.raceBegan):
                # minus 1 just in case non even
                if(self.poleOn+1>=len(self.poles)):
                    self.raceBegan = False
                    self.addWin(time.time()-self.raceTime)
                    # since race ended
                    try:
                        self.target.destroy()
                    except:
                        pass
                    self.beaconLight = None # use object + lights
                    self.beaconLightHolder = None
                    self.poleOn = 0
                else:
                    acceptableError = 100
                    # formula I created: (p2y-p1y)/(p2x-p1x)*(p2x-pAx)+p2y = 
                    # expected pAy
                    # so if the actual car positionY is within acceptableError of
                    # pAy then the car is between the two poles
                    # if in between poles
                    middleX = (self.poles[self.poleOn][1]+self.poles[self.poleOn+1][1])/2
                    middleY = (self.poles[self.poleOn][2]+self.poles[self.poleOn+1][2])/2
                    expectedCarY = ((self.poles[self.poleOn][2]-self.poles[self.poleOn+1][2])/
                                (self.poles[self.poleOn][1]-self.poles[self.poleOn+1][1])*
                                (self.poles[self.poleOn][1]-self.carPositionX)+
                                self.poles[self.poleOn][2])
                    # do not really care about car being inbetween pole in z axis
                    # because 2 demensional
                    if(expectedCarY+acceptableError>self.carPositionY and 
                       expectedCarY-acceptableError<self.carPositionY):
                        self.poleOn+=2
                        # only when last pole found is it necesary to add light
                        # to guide to next place elsewhere
                        (beaconLightX, beaconLightY) = self.getNextGateCenter()
                        if(beaconLightX!=None):
                            self.beaconLightHolder.setPos(beaconLightX, beaconLightY, self.beaconLightZ)
                            self.target.setPos(beaconLightX, beaconLightY, self.beaconLightZ)
        elif(self.mode == self.modeTutorial):
            self.destroyWin()
            # do the tutorial part for the creating
            timeBeforeNext = 2
            if(self.tutorialPause == True):
                if(time.time()-self.tutorialActionTime>timeBeforeNext):
                    self.tutorialPause = False
            else:
                if(self.tutorialStep == -1):
                    self.destroyInstructions()
                    self.setTutorialText("use w and s to move camera up and down")
                    self.tutorialStep+=1
                # do this until the user has completed all of the task
                self.checkTutorialStep(0, (self.keyMap["cam-up"] or 
                      self.keyMap["cam-down"]), 
                      "use a and d to rotate camera right and left")
                self.checkTutorialStep(1, (self.keyMap["cam-left"] or 
                      self.keyMap["cam-right"]), 
                      "use up-arrow and down-arrow to turn camera forward and backward")
                self.checkTutorialStep(2, (self.keyMap["forward"] or 
                      self.keyMap["backward"]), 
                      "use left-arrow and right-arrow to slide camera left and right")
                self.checkTutorialStep(3, (self.keyMap["left"] or
                      self.keyMap["right"]), 
                     "use mouse click to place objects on terrain")
                self.checkTutorialStep(4, (self.keyMap["mouse-click"]), 
                      "use up-arrow and down-arrow to move car forward and backward",
                      (self.switchToDrivingMode,self.destroyInstructions))
                # need to ensure that the mode stays as tutorial
                self.mode = self.modeTutorial
                # then tutorial part for the driving
                self.checkTutorialStep(5, (self.keyMap["forward"] or
                      self.keyMap["backward"]), 
                      "use right-arrow and left-arrow to rotate car left and right")
                self.checkTutorialStep(6, (self.keyMap["left"] or
                      self.keyMap["right"]), "Use poles to make the race course\n use z to start race")
                self.checkTutorialStep(7, True, "Follow yellow block through the gates till you win")
                self.checkTutorialStep(8, True, "Watch for high Terrain and blocks because you can not get through those")
                self.checkTutorialStep(9, True, "")
                if(self.tutorialStep>9):
                    # switch to main
                    self.switchToMainMode()
            # for movement
            if(self.tutorialStep<=4):
                self.findNewCameraPosition()
                self.checkAndAddNewObject()
            if(self.tutorialStep>4 and self.tutorialStep<=9):
                self.findCarNewXandY()
                self.setCarZ()
                self.setCameraPositionBehindCar()
        return task.cont

    def getNextGateCenter(self):
        if(len(self.poles)>self.poleOn+1):
            positionX = (self.poles[self.poleOn][1]+self.poles[self.poleOn+1][1])/2
            positionY = (self.poles[self.poleOn][2]+self.poles[self.poleOn+1][2])/2
            return (positionX, positionY)
        else:
            return (None, None)

    def checkTutorialStep(self, step, keysNeeded, nextText, functions=None):
        if(self.tutorialStep == step and self.tutorialNextStep == True):
            if(functions!=None):
                for func in functions:
                    func()
            self.destroyInstructions()
            self.setTutorialText(nextText)
            self.tutorialStep+=1
            self.tutorialNextStep = False
        elif(self.tutorialStep == step and keysNeeded):
            self.tutorialNextStep = True
            self.tutorialActionTime = time.time()
            self.tutorialPause = True

    def setUpTutorial(self):
        self.tutorialStep = -1
        self.tutorialPause = False
        # this records when last tutorial action taken
        self.tutorialActionTime = 0
        self.tutorialNextStep = False

    def checkAndAddNewObject(self):
        # clicking on 3D objects comes from here:
        # https://www.panda3d.org/manual/index.php/Clicking_on_3D_Objects
        # checks if it needs to add any objects:
        if(self.keyMap["mouse-click"] and self.mouseClicked == False):
            self.mouseClicked = True
            # found way to speed this up by only doing collision check
            # when mouse clicked by not using cTrav like in this method
            # the way I did it I found here:
            # https://www.panda3d.org/manual/index.php/Clicking_on_3D_Objects
            # self.mouseCollideTrav.traverse(render)
            if(base.mouseWatcherNode.hasMouse()):
                mousePos = base.mouseWatcherNode.getMouse()
                self.pickerRay.setFromLens(base.camNode, mousePos.getX(), mousePos.getY())
                # do not put this before previous line, will get the coordinates
                # of last mouse click and where pickerRay was
                # ahhhhhhh!!!!!!!!!!!
                self.mouseCollideTrav.traverse(render)
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
                    adjustedX = 10/2
                    adjustedY = 20/2
                    yaw = 0
                    # have to adjust this once there are different sized
                    # objects added
                    (actualXPos, actualYPos) =RacingGame.findActualCenter(
                                    self, newX, newY, adjustedX, adjustedY,
                                    yaw)
                    if(self.createdObject==self.createPole):
                        self.poles.append([loader.loadModel("TestPole.egg"),
                                                 actualXPos, actualYPos, newZ])
                        self.poles[len(self.poles)-1][0].reparentTo(render)
                        self.poles[len(self.poles)-1][0].setTwoSided(True)
                        self.poles[len(self.poles)-1][0].setPos(actualXPos, 
                                                               actualYPos, newZ)
                    else:
                        newCar = loader.loadModel("TestCar.egg")
                        newCar.reparentTo(render)
                        newCar.setPos(actualXPos,actualYPos, newZ)
                        # should take out because slow, but objects can not be
                        # seen without this because only seen from one direction
                        # even though normal vectors set up. 
                        newCar.setTwoSided(True)
                        self.objects.append(newCar)
        elif(not self.keyMap["mouse-click"]):
            # elif because for some reason mouseClicked was becoming false
            # while click still pressed
            self.mouseClicked = False

    def findNewCameraPosition(self):
        # Get the time that elapsed since last frame.  We multiply this with
        # the desired speed in order to find out with which distance to move
        # in order to achieve that desired speed.
        dt = globalClock.getDt()
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

    def carForwardImpact(self):
        # update position so that it is pointing right directions
        #(dirX, dirY, dirZ) = self.findCarFrontDir()
        #self.carRayForward.setDirection(dirX, dirY, dirZ)
        degToRad = math.pi/180
        # + math.pi since it is taking corner and going to center rather
        # than opposite that function actually does
        #(centerX,centerY) = self.findActualCenter(0,0,self.adjustedXForCenter,
        #                                   self.adjustedYForCenter, self.carYaw
        #                                   +math.pi)
        posAboveGround = 5
        # need to update with new coordinates
        self.carCollideTrav.traverse(render)
        collisions = list(self.carForwardHandler.getEntries())
        # closest collision using pythagorean formula
        collisions.sort(key=lambda x: (x.getSurfacePoint(render).getX()-
                         self.carPositionX)**2+(x.getSurfacePoint(render).getY()
                        -self.carPositionY)**2)
        if(len(collisions)>0):
            (actualX, actualY) = RacingGame.findActualCenter(self,
                                    self.carPositionX, self.carPositionY,
                                    self.adjustedXForCenter,
                                    self.adjustedYForCenter, self.carYaw)
            distance = ((collisions[0].getSurfacePoint(render).getX()-
                        actualX)**2+
                        (collisions[0].getSurfacePoint(render).getY()-
                        actualY)**2)**.5
            error = .9 # so that the collisionray does not detect car itself
            return distance/2<=self.adjustedYForCenter*.9
        else:
            return False

    def findCarNewXandY(self):
        # Get the time that elapsed since last frame.  We multiply this with
        # the desired speed in order to find out with which distance to move
        # in order to achieve that desired speed.
        deltaTime = globalClock.getDt()
        degreeAdjustment = 60
        positionAdjustment = 100
        # should switch rad and Deg in variable name
        radToDeg = math.pi/180
        # the x and y component of left and right moves, do not need to
        # compensate in z axis because not doing any roll, so there should be
        # no zComponent
        xComponent = math.sin(self.carYaw*radToDeg)
        yComponent = math.cos(self.carYaw*radToDeg)
        if self.keyMap["left"]:
            self.carYaw += degreeAdjustment * deltaTime
        if self.keyMap["right"]:
            self.carYaw -= degreeAdjustment * deltaTime
        if(self.keyMap["forward"] and not self.carForwardImpact()):
            self.carPositionX -= positionAdjustment * deltaTime*xComponent
            self.carPositionY += positionAdjustment * deltaTime*yComponent
        if self.keyMap["backward"]:
            self.carPositionX += positionAdjustment * deltaTime*xComponent
            self.carPositionY -= positionAdjustment * deltaTime*yComponent
        # need to consider both the x and y component of offset for both
        # because x slowly changes to y as it turns
        (actualXPos, actualYPos) = RacingGame.findActualCenter(self, 
                                    self.carPositionX, self.carPositionY,
                                    self.adjustedXForCenter,
                                    self.adjustedYForCenter, self.carYaw)
        self.car.setX(actualXPos)
        self.car.setY(actualYPos)
        self.car.setZ(self.carPositionZ)
        self.car.setHpr(self.carYaw, self.carPitch, 0)

    def setCarZ(self):
        # almost directly taken from ralph example
        entries = list(self.handler.getEntries())
        entries.sort(key=lambda x: x.getSurfacePoint(render).getZ())
        # worry about which thing it collides with later
        if (len(entries) > 0):
            # and entries[0].getIntoNode().getName() == "mountainCollide":
            self.carPositionZ = (entries[0].getSurfacePoint(render).getZ())
        else:
            # because at 25 everything should be below car and do not want
            # to continually go up or else it may go up forever. 
            self.carPositionZ = 25
        self.setCameraPositionBehindCar()

    def setCameraPositionBehindCar(self):
            # Modify view of camera so that it is behind car
            # should be named degToRad
            radToDeg = math.pi/180
            distanceBehind = 200
            distanceAbove = 60
            self.camera.setHpr(self.carYaw, -.5, 0)
            (actualXPos, actualYPos) = self.findActualCenter(self.carPositionX, self.carPositionY, 
                                      self.adjustedXForCenter, self.adjustedXForCenter, self.carYaw)
            camX = actualXPos + distanceBehind * math.sin(radToDeg*self.carYaw)
            camY = actualYPos - distanceBehind * math.cos(radToDeg*self.carYaw)
            camZ = self.carPositionZ + distanceAbove
            self.camera.setPos(camX, camY, camZ)

    def findActualCenter(self, positionX, positionY, adjustedX, adjustedY, yaw):
        # will need to fix this later, it seems to be adjusting wrong 
        # so that it is puting box away from click instead of on it
        # update, I think this is fixed?!?
        degToRad = math.pi/180
        actualXPos = (positionX - adjustedX * math.cos(degToRad*yaw) +
                      adjustedY * math.sin(degToRad*yaw))
        actualYPos = (positionY - adjustedY*math.cos(degToRad*yaw) -
                      adjustedX*math.sin(degToRad*yaw))
        return (actualXPos, actualYPos)

demo = RacingGame()
demo.run()
