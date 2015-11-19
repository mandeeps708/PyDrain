from dxfwrite import DXFEngine as dxf
import csv
import math
import pdb

########## Declaration ##########
points = []
data = []
area = 0

#Getting filename with which the file is to be saved.
filename =raw_input('Enter a new name for the file:')
drawing = dxf.drawing(filename+'.dxf')

#CSV file input.
csvfile=raw_input('Enter the name of CSV file (without extension):')
f = open(csvfile+'.csv')


# Adding csv lines to list data.
for row in csv.reader(f):
    data.append(row)


######################### Functions Defintion #########################

##### Base Drain #####
"""Creating Base drain
"""
def drawconti(data):
    for i in range(len(data) - 1):
        element1 = tuple(data[i])
        element2 = tuple(data[i+1])

        """drawing lines for base. First 10 lines in CSV contains the
        coordinates that will create the base.
        """
        if i < 9:
            drawing.add(dxf.line(element1, element2, color=7))
            points.append(element1)
        else:
            points.append(element1)


""" Solving two equations simultaneously. Here (p1x, p1y) and (p2x, p2y)
are the two points of a line and (px, py) is a single known point of
second line and theta is the angle it makes with x-axis.
"""

def solve(p1x, p1y, p2x, p2y, px, py, theta):
    #m1 and m2 are the slopes of given line.
    m1 = (p1y - p2y)/(p1x - p2x)
    m2 = math.tan(theta*(math.pi)/180)

    #if both lines are parallel.
    if (m1 == m2):
        return -1

    c1 = (p2y - m1*p2x)
    c2 = (py - m2*px)
    x = (c2 - c1) / (m1 - m2)
    y = m2*x + c2
    return x, y

"""Determinent of a 2x2 matrix.
"""
def det(x1, y1, x2, y2):
    return float(x1)*float(y2)-float(x2)*float(y1)



"""Returing the simplified form of coordinates
"""
def datum(x, y):
    return float(data[x][y])




#################### Calling Functions ####################

drawconti(data)

#pdb.set_trace() #for debugging (tracing)

theta = 180 - 63.43
theta2 = 180 - theta
points = points[:-1]

""" (final_x, final_y) are the coordinates of the intersection points
obtained by solving the left side.
"""
intersectingL_x1, intersectingL_y1 = solve(datum(0,0), datum(0,1), datum(1,0), datum(1,1), datum(11,0), datum(11,1), theta)
intersectingL_x2, intersectingL_y2 = solve(datum(1,0), datum(1,1), datum(2,0), datum(2,1), datum(11,0), datum(11,1), theta)
intersectingL_x3, intersectingL_y3 = solve(datum(2,0), datum(2,1), datum(3,0), datum(3,1), datum(11,0), datum(11,1), theta)

if intersectingL_x1 <= datum(1,0):
    finalL_x = intersectingL_x1
    finalL_y = intersectingL_y1
    coordinateL = tuple((str(finalL_x), str(finalL_y)))
    points.insert(1, coordinateL)

elif intersectingL_x3 >= datum(2,0):
    finalL_x = intersectingL_x3
    finalL_y = intersectingL_y3
    coordinateL = tuple((str(finalL_x), str(finalL_y)))
    points.insert(3, coordinateL)

else:
    finalL_x = intersectingL_x2
    finalL_y = intersectingL_y2
    coordinateL = tuple((str(finalL_x), str(finalL_y)))
    points.insert(2, coordinateL)

intersectingR_x1, intersectingR_y1 = solve(datum(9,0), datum(9,1), datum(8,0), datum(8,1), datum(10,0), datum(10,1), theta2)
intersectingR_x2, intersectingR_y2 = solve(datum(8,0), datum(8,1), datum(7,0), datum(7,1), datum(10,0), datum(10,1), theta2)
intersectingR_x3, intersectingR_y3 = solve(datum(7,0), datum(7,1), datum(6,0), datum(6,1), datum(10,0), datum(10,1), theta2)

if intersectingR_x1 >= datum(8,0):
    finalR_x = intersectingR_x1
    finalR_y = intersectingR_y1
    coordinateR = tuple((str(finalR_x), str(finalR_y)))
    index = points.index((str(datum(8,0)), str(datum(8,1))))
    points.insert(index, coordinateR)

elif intersectingR_x3 <= datum(7,0):
    finalR_x = intersectingR_x3
    finalR_y = intersectingR_y3
    coordinateR = tuple((str(finalR_x), str(finalR_y)))
    index = points.index((str(datum(7,0)), str(datum(7,1))))
    points.insert(index, coordinateR)

else:
    finalR_x = intersectingR_x2
    finalR_y = intersectingR_y2
    coordinateR = tuple((str(finalR_x), str(finalR_y)))
    points.insert(9, coordinateR)
# Intersection points.
intersectL = tuple((finalL_x, finalL_y))
intersectR = tuple((finalR_x, finalR_y))

indexL = points.index(coordinateL)
indexR = points.index(coordinateR)

points = points[indexL:indexR+1]

""" Creates cutting plane
"""
#for i in range(10,11):
#elem1 and elem2 are the base points known of the cutting plane.

elem1 = tuple(data[10])
elem2 = tuple(data[11])
drawing.add(dxf.line(elem1, elem2, color=7))
drawing.add(dxf.line(intersectL, elem2, color=7))
drawing.add(dxf.line(elem1, intersectR, color=7))

points.extend((elem1, elem2, coordinateL))

pdb.set_trace() #for debugging (tracing)

# Calculating Area Here.
for i in range(0, len(points)-1):
    area += det(points[i][0], points[i][1], points[i+1][0], points[i+1][1])
    print area
#area = area + det(points[len(points)][0], points[len(points)][1],points[0][0],points[0][1])
if area < 0:
    area = -(area / 2)
else:
    area = area / 2
print 'Area is: ', area

drawing.add_layer('TEXTLAYER', color=2)
drawing.add(dxf.text('Mandeep', insert=(0, 0.2), layer='TEXTLAYER'))

#alpha = math.tan((180 - 90 - theta) * (math.pi) / 180)
#pdb.set_trace()
#t1, t2 = solve(-1.25, 216.7, -1.05, 217.05, -0.8465, 216.609, alpha)

########## Placing Block Now ##########

#   horizontal = 1.5
#   blockhlx = -horizontal/2
#   blockhrx = horizontal/2
#   blockhy= float(elem1[1])+0.0001

#   drawing.add(dxf.line((blockhlx, blockhy), (blockhrx, blockhy), color=7))

#   vertical = 0.50,216.7
#   blockvlx = -vertical[0]
#   blockvrx = vertical[0]
#   blockvy = vertical[1]

#   drawing.add(dxf.line((blockhlx, blockvy), (blockhlx, blockhy), color=7))
#   drawing.add(dxf.line((blockhrx, blockvy), (blockhrx, blockhy), color=7))

#   innerver = 0.45, 215.7
#   iblockvlx = -innerver[0]
#   iblockvrx = [0]
#   iblockvy = vertical[1]

#drawing.add(dxf.line((iblockvlx, iblockvy), (iblockvlx, blockvy), color=7))

#block = [['0.50', '216.7'], ['0.45','216.7'], ['0.45', '216'], ['-0.45', '216'], ['-0.45', '216.7'], ['-0.50', '216.7'], ['-0.50', '215.8001'],['0.50','215.8001'],['0.50', '216.7']]

#drawconti(block)


# Saving file now.
drawing.save()
print "Check file " + filename + ".dxf in current directory."
