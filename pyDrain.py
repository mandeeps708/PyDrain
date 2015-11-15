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
        element2 =tuple(data[i+1])

        """drawing lines for base. First 10 lines in CSV contains the
        coordinates that will create the base.
        """
        if i < 9:
            drawing.add(dxf.line(element1, element2, color=7))
            points.append(element1)
        else:
            print i


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

"""Finding length of a line from two points
"""
def length(px1, py1, px2, py2):
    py = (py2 - py1) * (py2 - py1)
    px = (px2 - px1) * (px2 - px1)
    print 'length is ', math.sqrt(py + px)
    return math.sqrt(py + px)

#################### Calling Functions ####################

drawconti(data)

#pdb.set_trace() #for debugging (tracing)
length(-1.05, 217.05, -0.8465, 216.609)

theta = 180 - 63.43
theta2 = 180 - theta
print theta,theta2
""" (a1, b1) are the coordinates of the intersection points obtained by
solving the left side and similarly (a2, b2) are for the right side
intersection.
"""
if theta >= 90.45 and theta <= 114.77 and theta2 <= 89.55 and theta2 >= 65.23:
    a1, b1 = solve(-1.05, 217.05, -0.85, 217.05, -0.8465, 216.609, theta)
    a2, b2 = solve(1.05, 217.05, 0.85, 217.05, 0.8465, 216.609, theta2)
    print 'first case'
elif theta > 114.77 and theta <= 167.29 and theta2 < 65.23 and theta2 >= 12.71:
    a1, b1 = solve(-1.25, 216.7, -1.05, 217.05, -0.8465, 216.609, theta)
    a2, b2 = solve(1.25, 216.7, 1.05, 217.05, 0.8465, 216.609, theta2)
    print 'second case'
elif theta > 167.29 and theta <= 180 and theta2 < 12.71 and theta2 >=0:
    a1, b1 = solve(-1.45, 216.7, -1.25, 216.7, -0.8465, 216.609, theta)
    a2, b2 = solve(1.45, 216.7, 1.25, 216.7, 0.8465, 216.609, theta2)
    print 'third case'
else:
    print 'Invalid angle'

# Intersection points.
intersect1 = tuple((a1, b1))
intersect2 = tuple((a2, b2))

""" Creates cutting plane
"""
for i in range(len(data)-1):
    #elem1 and elem2 are the base points known of the cutting plane.
    elem1 = tuple(data[i])
    elem2 = tuple(data[i+1])
    if i>=10:
        #creating the base line of cutting plane.
        drawing.add(dxf.line(elem1, elem2, color=7))

    #Drawing lines using the intersection points.
    drawing.add(dxf.line(tuple(data[-1]),(a1, b1),color=7))
    drawing.add(dxf.line(tuple(data[-2]),(a2, b2),color=7))

# Appending every point needed to a list for the sake of finding area.
points=points[1:]
points.append(intersect2)
points.append(elem1)
points.append(elem2)
points.append(intersect1)
points.append(points[0])

#pdb.set_trace() #for debugging (tracing)

# Calculating Area Here.
for i in range(0, len(points)-1):
    area += det(points[i][0], points[i][1],
                points[i+1][0], points[i+1][1])
if area < 0:
    area = -(area / 2)
else:
    area = area / 2
print 'Area is: ', area

drawing.add_layer('TEXTLAYER', color=2)
drawing.add(dxf.text('Mandeep', insert=(0, 0.2), layer='TEXTLAYER'))


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
