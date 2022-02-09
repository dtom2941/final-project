# Dylan Tom
# andrew id: dtom
# for creating eggs
import random, math
class EggObject(object):
    gridWidth = 100
    # the y axis representation of length
    gridDepth = 100
    gridHeight = 100
    def __init__(self, name, texture="rocks.jpg", posX=0, posY=0, posZ=0, size=10):
        self.eggString = ""
        self.defaultSettings()
        self.posX = posX
        self.posY = posY
        self.posZ = posZ
        self.size = size
        self.filename = name + ".egg"
        self.texture = texture
        
    def getNormal(self, pos1, pos2, pos3):
        # will need to fix this somehow sometime, the normals are sometimes
        # negative of what they are supposed to be!
        # the 0th index is x, first y, second z in each pos
        x = (pos1[1]-pos2[1])*(pos1[2]-pos3[2])-(pos1[2]-pos2[2])*(pos1[1]-pos3[1])
        y = (pos1[2]-pos2[2])*(pos1[0]-pos3[0])-(pos1[0]-pos2[0])*(pos1[2]-pos3[2])
        z = (pos1[0]-pos2[0])*(pos1[1]-pos3[1])-(pos1[1]-pos2[1])*(pos1[0]-pos3[0])
        return (x,y,z)
        
    @staticmethod
    def setGridWidthAndHeight(width, depth, height):
        gridWidth = width
        gridHeight = height
        gridDepth = depth
    
    def editFile(self):
        file = open(self.filename, "w")
        file.write(self.eggString)
        file.close()
    
    def __repr__(self):
        return self.filename
        
    # basically so that it is formatted well
    def addCommand(self, newCommand):
        self.eggString = self.eggString + "\n" + newCommand
        
    def defaultSettings(self):
        self.eggString += "<CoordinateSystem> { Z-Up }"
        
    def addTexture(self, textureName, textureLocation):
        self.addCommand("<Texture> "+textureName+" {")
        self.addCommand("   "+textureLocation)
        self.addCommand("   <Scalar> format { rgb }")
        self.addCommand("   <Scalar> wrapu { repeat }")
        self.addCommand("   <Scalar> wrapv { repeat }")
        self.addCommand("   <Scalar> minfilter { linear_mipmap_linear }")
        self.addCommand("   <Scalar> magfilter { linear }")
        self.addCommand("   <Scalar> envtype { normal_height }")
        self.addCommand("}")

class Car(EggObject):
    def __init__(self, name, posX, posY, posZ):
        super().__init__(name, posX, posY, posZ)
        self.createVertexes()
        self.addCollisionToPolygons()

    def createPoints(self):
        pass

    def addCollisionToPolygons(self):
        # used this to get how to add the collision to the egg file:
        # https://www.panda3d.org/forums/viewtopic.php?t=782
        self.addCommand("<Group> %s {" % ("car"))# add self.__repr__ later
        #self.addCommand("      <Collide> mountainCollide { Polygon level keep descend event }")
        self.createPolygons()
        self.addCommand("}")

    # make filename something that is initially set so that it is easy to name the
    # collision array
    def createVertexes(self):
        # update to have normal vectors
        self.addCommand("<VertexPool> %s.verts {" % ("CarVertexes"))
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    self.addCommand("   <Vertex> %d { %d %d %d " % 
                                   (i*100+j*10+k,i*10,j*2*10,k*10))
                    self.addCommand("   <UV> { %d %d }" % ((i+2*k)*.5,(j+2*k)*.5))
                    self.addCommand("}")
        self.addCommand("}")
        
    def createPolygons(self):
        texture = "silver.jpg"
        k=0
        j=0
        for i in range(2):
            self.addCommand("      <Collide> poleCollide { Polygon keep descend event }")
            pos1 = [i,j,k]
            pos2 = [i,j+1,k]
            pos3 = [i,j,k+1]
            normalX, normalY, normalZ = self.getNormal(pos1,pos2,pos3)
            self.addCommand("<Polygon> {")
            self.addCommand("    <Texture> { %s }" % (texture))
            self.addCommand("    <Normal> { %f %f %f }"%(normalX, normalY, normalZ))
            self.addCommand("    <VertexRef> { %d %d %d %d <Ref> { %s.verts } }"
                    % (i*100+j*10+k, i*100+j*10+(k+1),i*100+10*(j+1)+(k+1),
                       i*100+(j+1)*10+k, "CarVertexes"))
            self.addCommand("}")
        i = 0
        k=0
        for j in range(2):
            self.addCommand("      <Collide> poleCollide { Polygon keep descend event }")
            pos1 = [i,j,k]
            pos2 = [i+1,j,k]
            pos3 = [i,j,k+1]
            normalX, normalY, normalZ = self.getNormal(pos1,pos2,pos3)
            self.addCommand("<Polygon> {")
            self.addCommand("    <Texture> { %s }" % (texture))
            self.addCommand("    <Normal> { %f %f %f }"%(normalX, normalY, normalZ))
            self.addCommand("    <VertexRef> { %d %d %d %d <Ref> { %s.verts } }"
                    % (i*100+j*10+k, i*100+j*10+(k+1),(i+1)*100+10*j+(k+1),
                       (i+1)*100+j*10+k, "CarVertexes"))
            self.addCommand("}")
        i = 0
        j = 0
        for k in range(2):
            self.addCommand("      <Collide> poleCollide { Polygon keep descend event }")
            pos1 = [i,j,k]
            pos2 = [i,j+1,k]
            pos3 = [i+1,j,k]
            normalX, normalY, normalZ = self.getNormal(pos1,pos2,pos3)
            self.addCommand("<Polygon> {")
            self.addCommand("    <Texture> { %s }" % (texture))
            self.addCommand("    <Normal> { %f %f %f }"%(normalX, normalY, normalZ))
            self.addCommand("    <VertexRef> { %d %d %d %d <Ref> { %s.verts } }"
                    % (i*100+j*10+k, i*100+(j+1)*10+k,(i+1)*100+10*(j+1)+k,
                       (i+1)*100+j*10+k, "CarVertexes"))
            self.addCommand("}")

class BeaconLight(Car):        
    def createPolygons(self):
        # got yellow from here: https://upload.wikimedia.org/wikipedia/commons/4/44/WO_Yellow.jpg
        texture = "yellow.jpg"
        k=0
        j=0
        for i in range(2):
            self.addCommand("      <Collide> poleCollide { Polygon keep descend event }")
            pos1 = [i,j,k]
            pos2 = [i,j+1,k]
            pos3 = [i,j,k+1]
            normalX, normalY, normalZ = self.getNormal(pos1,pos2,pos3)
            self.addCommand("<Polygon> {")
            self.addCommand("    <Texture> { %s }" % (texture))
            self.addCommand("    <Normal> { %f %f %f }"%(normalX, normalY, normalZ))
            self.addCommand("    <VertexRef> { %d %d %d %d <Ref> { %s.verts } }"
                    % (i*100+j*10+k, i*100+j*10+(k+1),i*100+10*(j+1)+(k+1),
                       i*100+(j+1)*10+k, "CarVertexes"))
            self.addCommand("}")
        i = 0
        k=0
        for j in range(2):
            self.addCommand("      <Collide> poleCollide { Polygon keep descend event }")
            pos1 = [i,j,k]
            pos2 = [i+1,j,k]
            pos3 = [i,j,k+1]
            normalX, normalY, normalZ = self.getNormal(pos1,pos2,pos3)
            self.addCommand("<Polygon> {")
            self.addCommand("    <Texture> { %s }" % (texture))
            self.addCommand("    <Normal> { %f %f %f }"%(normalX, normalY, normalZ))
            self.addCommand("    <VertexRef> { %d %d %d %d <Ref> { %s.verts } }"
                    % (i*100+j*10+k, i*100+j*10+(k+1),(i+1)*100+10*j+(k+1),
                       (i+1)*100+j*10+k, "CarVertexes"))
            self.addCommand("}")
        i = 0
        j = 0
        for k in range(2):
            self.addCommand("      <Collide> poleCollide { Polygon keep descend event }")
            pos1 = [i,j,k]
            pos2 = [i,j+1,k]
            pos3 = [i+1,j,k]
            normalX, normalY, normalZ = self.getNormal(pos1,pos2,pos3)
            self.addCommand("<Polygon> {")
            self.addCommand("    <Texture> { %s }" % (texture))
            self.addCommand("    <Normal> { %f %f %f }"%(normalX, normalY, normalZ))
            self.addCommand("    <VertexRef> { %d %d %d %d <Ref> { %s.verts } }"
                    % (i*100+j*10+k, i*100+(j+1)*10+k,(i+1)*100+10*(j+1)+k,
                       (i+1)*100+j*10+k, "CarVertexes"))
            self.addCommand("}")

class Pole(EggObject):
    def __init__(self, name, posX, posY, posZ):
        super().__init__(name, posX, posY, posZ)
        self.createVertexes()
        self.addCollisionToPolygons()

    def createPoints(self):
        pass

    def addCollisionToPolygons(self):
        # used this to get how to add the collision to the egg file:
        # https://www.panda3d.org/forums/viewtopic.php?t=782
        self.addCommand("<Group> %s {" % ("pole"))# add self.__repr__ later
        self.createPolygons()
        self.addCommand("}")

    # make filename something that is initially set so thatit is easy to name the
    # collision array
    def createVertexes(self):
        # update to have normal vectors
        self.addCommand("<VertexPool> %s.verts {" % ("CarVertexes"))
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    self.addCommand("   <Vertex> %d { %d %d %d " % 
                                   (i*100+j*10+k,i*10,j*10,k*100))
                    self.addCommand("   <UV> { %d %d }" % ((i+2*k)*.5,(j+2*k)*.5))
                    self.addCommand("}")
        self.addCommand("}")

    def createPolygons(self):
        texture = "silver.jpg"
        k=0
        j=0
        for i in range(2):
            self.addCommand("      <Collide> poleCollide { Polygon keep descend event }")
            self.addCommand("<Polygon> {")
            self.addCommand("    <Texture> { %s }" % (texture))
            self.addCommand("    <VertexRef> { %d %d %d %d <Ref> { %s.verts } }"
                    % (i*100+j*10+k, i*100+j*10+(k+1),i*100+10*(j+1)+(k+1),
                       i*100+(j+1)*10+k, "CarVertexes"))
            self.addCommand("}")
        i = 0
        k=0
        for j in range(2):
            self.addCommand("      <Collide> poleCollide { Polygon keep descend event }")
            self.addCommand("<Polygon> {")
            self.addCommand("    <Texture> { %s }" % (texture))
            self.addCommand("    <VertexRef> { %d %d %d %d <Ref> { %s.verts } }"
                    % (i*100+j*10+k, i*100+j*10+(k+1),(i+1)*100+10*j+(k+1),
                       (i+1)*100+j*10+k, "CarVertexes"))
            self.addCommand("}")
        i = 0
        j = 0
        for k in range(2):
            self.addCommand("      <Collide> poleCollide { Polygon keep descend event }")
            self.addCommand("<Polygon> {")
            self.addCommand("    <Texture> { %s }" % (texture))
            self.addCommand("    <VertexRef> { %d %d %d %d <Ref> { %s.verts } }"
                    % (i*100+j*10+k, i*100+(j+1)*10+k,(i+1)*100+10*(j+1)+k,
                       (i+1)*100+j*10+k, "CarVertexes"))
            self.addCommand("}")

class Rock(EggObject):
    rocks = 0
    def __init__(self, name, randPos=True, size=10, posX=0, posY=0,posZ=0,roughness=2):
        if(randPos):
            # replace later with a way of getting the exact height
            self.posX = random.randint(-EggObject.gridWidth, EggObject.gridWidth)
            self.posY = random.randint(-EggObject.gridDepth, EggObject.gridDepth)
            self.posZ = random.randint(-EggObject.gridHeight, EggObject.gridHeight)
            self.filename = name + ".egg"
        else:
            super().__init__(name, posX, posY, posZ, size)
        self.roughness = roughness
        # number of points defining center of the rock
        self.circumRockGrid = 20
        # how many rows of points there are
        # easier with odd numbers
        self.latsRockGrid = 9
        self.rockGrid = [[0]*self.circumRockGrid]*self.latsRockGrid
        self.makeRockGrid() 
        Rock.rocks+=1
        # self.createRandomDistances
        #self.decreaseHugeGradient(roughness)
        self.createVertexPool()
        self.createPolygons()
        
        
    def makeRockGrid(self):
        # can later make this so that it doesn't use magic numbers, but for
        # now it is just going to be a rock difined by the parameters that I
        # give it so it doesn't have to be generalized namely 8 rows, 20 cols
        # the number of points in concentric circle is difined by circum*cos(pi/2/lats)
        # rock grid starts from bottom
        circum = self.curcumRockGrid
        lats = self.latsRockGrid
        self.rockGrid[0][cirum//2]+=1
        # maybe do this with list comprehension
        for point in range(circum//4,3*cirum//4):
            self.rockGrid[1][point]+=1
        for point in range(circum//2-cirum//(2**1.5), circum//2+cirum//(2**1.5)):
            self.rockGrid[2][point]+=1
        for point in range(circum//2-cirum//(4)*3**.5, circum//2+cirum//(4)*3**.5):
            self.rockGrid[3][point]+=1
        for point in range(0, circum):
            self.rockGrid[4][point]+=1
        for point in range(circum//2-cirum//(4)*3**.5, circum//2+cirum//(4)*3**.5):
            self.rockGrid[5][point]+=1
        for point in range(circum//2-cirum//(2**1.5), circum//2+cirum//(2**1.5)):
            self.rockGrid[6][point]+=1
        for point in range(circum//4,3*cirum//4):
            self.rockGrid[7][point]+=1
        self.rockGrid[8][cirum//2]+=1

    rockAdjustment = 2
    
    def makeRockPoints(self):
        # the greek letter row for spherical coordinates
        prow = -math.pi/2
        deltaProw = math.pi/8
        self.addCommand("<VertexPool> %s.verts {" % ("Rock Vertexes"))
        for row in self.rockGrid:
            theta = 0
            trueRow = takeZerosOut(row)
            print(trueRow)
            deltaTheta = 2*math.pi/len(trueRow)
            for col in trueRow:
                x = 0 # edit later
                y = 0
                z = 0
                self.addCommand("   <Vertex> %d { %d %d %d }" % 
                                   (row*10**Rock.rockAdjustment+col,row,col,0))
            prow += deltaProw
        self.addCommand("}")

    def takeZerosOut(array):
        newArray = []
        for item in array:
            if item != 0:
                newArray.append(item)
        return newArray

class Mountain(EggObject):
    mountains=0
    def __init__(self, name, points=50, maxGradient=10):
        super().__init__(name)
        self.createMountain() 
        self.heightGrid = []
        self.heightGrid += [[0]*points for time in range(points)]
        Mountain.mountains+=1
        # use current mountain later so that when editting the file, the exact 
        # mountain that this is known.
        # current Mountain
        self.createRandomVertexes()
        # call this the amount of times it takes to make all of the gradients
        # look good, isn't expected to make the entire thing have gradient below
        # measure, just makes sure after going over the grid once that the
        # gradient of anything over this gradient is decreased
        self.decreaseHugeGradient(5)
        self.createVertexPool()
        self.addCollisionToPolygons()
        #self.createPolygons()

    def nicePrint(self, array):
        for row in array:
            print(row)

    def createMountain(self):
        filename = "TestMountain.egg"
        self.addTexture("ground", "models/ground.jpg")
        self.addTexture("tree", "models/tree.jpg")

    def createRandomVertexes(self):
        # adapting algorithm that was found here:
        # http://www.lighthouse3d.com/opengl/terrain/index.php3?particle
        size = len(self.heightGrid)
        # put the x and y in center of grid
        x, y = size//2, size//2
        totalHeight = 10000
        for addition in range(totalHeight):
            # increase height at specified point
            self.heightGrid[x][y] += 1
            x, y = self.newPoints(x,y)

    def newPoints(self, curX, curY):
        size = len(self.heightGrid)
        newX =curX + random.randint(-1,1)
        newY =curY + random.randint(-1,1)
        if(newX<0 or newX>=size or newY<0 or newY>=size):
            return curX, curY
        else:
            return newX, newY

    def createVertexPool(self):
        # currently made so that it can only run with single digits, 
        # will change later
        # +2 so that it also gets the outer edges
        size = len(self.heightGrid)+2
        # distance between the points
        distance = 500
        # can use self.mountains because mountain is created before new one 
        # needed. 
        self.addCommand("<VertexPool> %s.verts {" % ("MountVertexes"+str(
                                                               self.mountains)))
        distanceBetweenPoints = 20
        for i in range(size):
            for j in range(size):
                # doing this so that the position in grid is maintained
                # however the position in real space is corrected since the grid
                # should start at 0,0,0 and surrounding area should be 1 away
                xPoint = i-1
                yPoint = j-1
                # this is for the values that are not in grid
                if(xPoint<0 or yPoint<0 or xPoint>=size-2 or yPoint>=size-2):
                    # the reason why the values are not negative to begin with
                    # is so that I can number the points by index
                    self.addCommand("   <Vertex> %d { %d %d %d " %
                                   (i*Mountain.vertexAdjustment+j,
                                   i*distanceBetweenPoints,
                                   j*distanceBetweenPoints,0))
                    self.addCommand("       <UV> { %d %d }" % (i*.5,j*.5))
                    self.addCommand("  }")
                    
                else:
                    self.addCommand("   <Vertex> %d { %d %d %d " % 
                                   (i*Mountain.vertexAdjustment+j, 
                                   i*distanceBetweenPoints, 
                                   j*distanceBetweenPoints, 
                                   self.heightGrid[xPoint][yPoint]))
                    self.addCommand("       <UV> { %d %d }" % (i*.5,j*.5))
                    self.addCommand("  }")
        # adds u,v,w so that the polygons has the right place to put the image
        self.addCommand("}")

    def addCollisionToPolygons(self):
        # used this to get how to add the collision to the egg file:
        # https://www.panda3d.org/forums/viewtopic.php?t=782
        self.addCommand("<Group> %s {" % ("mountain"))# add self.__repr__ later
        #self.addCommand("      <Collide> mountainCollide { Polygon level keep descend event }")
        self.createPolygons()
        self.addCommand("}")

    vertexAdjustment = 1000
    def createPolygons(self, texture="ground"):# texture="rocks.jpg"):#texture="ground"):
        size = len(self.heightGrid)+1
        for i in range(size):
            for j in range(size):
                # these if statements are to create a pattern, take out when
                # figured out how to use actual textures
                self.addCommand("      <Collide> mountainCollide { Polygon level keep descend event }")
                if((j+i)%2 == 0):
                    self.addCommand("<Polygon> {")
                    self.addCommand("    <Texture> { %s }" % ("ground.jpg"))
                    # testing if this works for displaying texture
                    # self.addCommand("<TRef> { %s }" % (texture))
                    self.addCommand("    <VertexRef> { %d %d %d %d <Ref> { %s.verts } }" 
                    % (i*Mountain.vertexAdjustment+j, (i+1)*Mountain.vertexAdjustment+j,
                    (i+1)*Mountain.vertexAdjustment+j+1, i*Mountain.vertexAdjustment+j+1,
                                            "MountVertexes"+str(self.mountains)))
                    self.addCommand("}")
                else:
                    self.addCommand("<Polygon> {")
                    self.addCommand("    <Texture> { %s }" % ("tree.jpg"))
                    # testing if this works for displaying texture
                    # self.addCommand("<TRef> { %s }" % ("tree"))
                    self.addCommand("    <VertexRef> { %d %d %d %d <Ref> { %s.verts } }" 
                    % (i*Mountain.vertexAdjustment+j, (i+1)*Mountain.vertexAdjustment+j,
                    (i+1)*Mountain.vertexAdjustment+j+1, i*Mountain.vertexAdjustment+j+1,
                                            "MountVertexes"+str(self.mountains)))
                    self.addCommand("}")
    
    def decreaseHugeGradient(self, gradientMax = 20):
        # given the random number that is choosen this will give a number
        direction = [(-1,-1), (-1, 0), (-1, 1),
                     (0, -1),          (0, 1),
                     (1, -1), (1, 0),  (1, 1)]
        for row in range(len(self.heightGrid)):
            for col in range(len(self.heightGrid)):
                if(Mountain.maxGradientSize(self.heightGrid, row, col
                   )>gradientMax):
                    # randomly place part of height somewhere else
                    self.heightGrid[row][col] -= gradientMax//4
                    (addRow, addCol) = direction[random.randint(0,7)]
                    while(not Mountain.isValidRowAndCol(self.heightGrid, 
                                                       row+addRow, col+addCol)):
                        (addRow, addCol) = direction[random.randint(0,7)]
                    self.heightGrid[row+addRow][col+addCol] += gradientMax//4
                    

    def maxGradientSize(array, row, col):
        maxGradient = 0
        # the size of box to see how large gradient is
        boxRadius = 1
        for curRow in range(row-boxRadius, row+boxRadius+1):
            for curCol in range(col-boxRadius, col+boxRadius+1):
                # need to not cause error
                if(Mountain.isValidRowAndCol(array, curRow, curCol)):
                    # need to do it this way with row and col first so that we
                    # only detect if the current row and col is too large
                    gradient = array[row][col]-array[curRow][curCol]
                    if(gradient>maxGradient):
                        maxGradient = gradient
        return maxGradient
    
    def isValidRowAndCol(array, row, col):
        if(row>=0 and col>=0 and row<len(array) and col<len(array[0])):
            return True
        else:
            return False
    
def main():
    # testMountain1 so that I do not mess up current 1
    # 999 is too large
    m = Mountain("TestMountain1", 60)
    m.editFile()
    p = Pole("TestPole", 0, 0, 0)
    p.editFile()
    c = Car("TestCar", 0,0,0)
    c.editFile()
    b = BeaconLight("BeaconLight",0,0,0)
    b.editFile()
    
if __name__ == '__main__':
    main()