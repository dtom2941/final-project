# Dylan Tom
# andrew id: dtom
# for creating eggs
import random
class Mountain(object):
    mountains=0
    def __init__(self, size = 5):
        self.eggString = ""
        self.createMountain() 
        self.heightGrid = []
        self.heightGrid += [[0]*size for time in range(size)]
        Mountain.mountains+=1
        self.createRandomVertexes()
        self.createVertexPool()
        self.createPolygons()
    
    def editFile(self, filename):
        file = open(filename, "w")
        file.write(self.eggString)
        file.close()
    
    def __repr__(self):
        return self.eggString
    
    # basically so that it is formatted well
    def addCommand(self, newCommand):
        self.eggString = self.eggString + "\n" + newCommand
    
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
    
    def defaultSettings(self):
        self.eggString += "<CoordinateSystem> { Z-Up }"
    
    def createMountain(self):
        filename = "TestMountain.egg"
        self.defaultSettings()
        self.addTexture("ground", "models/ground.jpg")
    
    def createRandomVertexes(self):
        # adapting algorithm that was found here
        size = len(self.heightGrid)
        # put the x and y in center of grid
        x, y = size//2, size//2
        totalHeight = 1000
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
                    self.addCommand("   <Vertex> %d { %d %d %d }" % (i*Mountain.vertexAdjustment+j,i,j,0))
                else:
                    self.addCommand("   <Vertex> %d { %d %d %d }" % (i*Mountain.vertexAdjustment+j, i, j, 
                                    self.heightGrid[xPoint][yPoint]))
        self.addCommand("}")
                                
    vertexAdjustment = 100
    def createPolygons(self, texture="ground.jpg"):#texture="ground"):
        size = len(self.heightGrid)+1
        for i in range(size):
            for j in range(size):
                self.addCommand("<Polygon> {")
                self.addCommand("    <Texture> { %s }" % (texture))
                self.addCommand("    <VertexRef> { %d %d %d %d <Ref> { %s.verts } }" 
                % (i*Mountain.vertexAdjustment+j, (i+1)*Mountain.vertexAdjustment+j,
                  (i+1)*Mountain.vertexAdjustment+j+1, i*Mountain.vertexAdjustment+j+1,
                                           "MountVertexes"+str(self.mountains)))
                self.addCommand("}")
    
def main():
    m = Mountain(99)
    filename = "TestMountain.egg"
    m.editFile(filename)
    
if __name__ == '__main__':
    main()