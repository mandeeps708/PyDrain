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
try:
    csvfile=raw_input('Enter the name of CSV file (without extension):')
    f = open(csvfile+'.csv')
except NameError and IOError:
    print '\n ##### Check file name! File', csvfile,'.csv not found#####\n'
    exit()



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
            drawing.add(dxf.line(element1, element2, color=7, layer='Base'))
            points.append(element1)
        elif i < 11:
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


"""Checking if the value of determinant is negative or not. If it's
negative then it's made positive and finally the value is divided by 2,
as per the forumula of area.
"""
def areaNegative(area):
    if area < 0:
        area = -(area / 2)
    else:
        area = area / 2
    return area


#################### Calling Functions ####################

drawing.add_layer('Base', color=2)
drawconti(data)

#pdb.set_trace() #for debugging (tracing)

theta = 180 - datum(12,0)
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
drawing.add_layer('workingSpace', color=7)

elem1 = tuple(data[10])
elem2 = tuple(data[11])
drawing.add(dxf.line(elem1, elem2, color=7, layer='workingSpace'))
drawing.add(dxf.line(intersectL, elem2, color=7, layer='workingSpace'))
drawing.add(dxf.line(elem1, intersectR, color=7, layer='workingSpace'))

points.extend((elem1, elem2, coordinateL))

#pdb.set_trace() #for debugging (tracing)

# Calculating Area Here.
if float(elem2[1]) < float(points[3][1]):
    for i in range(0, len(points)-1):
        area += det(points[i][0], points[i][1], points[i+1][0], points[i+1][1])

    print 'Total Cutting Area is: ', areaNegative(area)

else:
    print 'cut plane is above the drain base'
    intersect_cut_xL, intersect_cut_yL = solve(datum(3,0), datum(3,1), datum(4,0), datum(4,1), datum(11,0), datum(11,1), 0)
    intersect_cut_xR, intersect_cut_yR = solve(datum(5,0), datum(5,1), datum(6,0), datum(6,1), datum(11,0), datum(11,1), 0)
    coordinateL = tuple((str(intersect_cut_xL), str(intersect_cut_yL)))
    coordinateR = tuple((str(intersect_cut_xR), str(intersect_cut_yR)))

    coordListL = points[:3]
    coordListL.append(coordinateL)
    coordListL.append(points[-2])
    coordListL.append(coordListL[0])
    cuttingL = 0
    cuttingR = 0

    coordListR = [ coordinateR ]
    coordListR += points[5:9]
    coordListR.append(coordListR[0])
    for i in range(0, len(coordListL)-1):
        cuttingL += det(coordListL[i][0], coordListL[i][1], coordListL[i+1][0], coordListL[i+1][1])
    for i in range(0, len(coordListR)-1):
        cuttingR += det(coordListR[i][0], coordListR[i][1], coordListR[i+1][0], coordListR[i+1][1])
    left_cutting = areaNegative(cuttingL)
    right_cutting = areaNegative(cuttingR)

    total_cutting = left_cutting + right_cutting

    fillingList = [coordinateL, coordinateR, (str(datum(5,0)), str(datum(5,1))), (str(datum(4,0)), str(datum(4,1)))]
    fillingList.append(coordinateL)
    fillingArea = 0

    for i in range(0, len(fillingList)-1):
        fillingArea += det(fillingList[i][0], fillingList[i][1], fillingList[i+1][0], fillingList[i+1][1])
    fillingArea = areaNegative(fillingArea)
    print 'Total Cutting Area is: ', total_cutting
    print 'Total filling Area is: ', fillingArea
    #intersect_index = points.index((str(datum(8,0)), str(datum(8,1))))
    # not yet implemented.
    # adding areas of left and right blocks that are created. First we
    # have to find out the intersection point.

drawing.add_layer('TEXTLAYER', color=2)
drawing.add(dxf.text('Mandeep', insert=(0, 0.2), layer='TEXTLAYER'))

#alpha = math.tan((180 - 90 - theta) * (math.pi) / 180)
pdb.set_trace()
#t1, t2 = solve(-1.25, 216.7, -1.05, 217.05, -0.8465, 216.609, alpha)

drawing.add_layer('Block', color=4)
########## Placing Block Now ##########

block_length = 1.5
block_lx = -block_length / 2
block_rx = block_length / 2
block_y= float(elem1[1])

drawing.add(dxf.line((block_lx, block_y), (block_rx, block_y), color=7))

block_height = 216.7
horizontal_depth = 0.1
vertical_depth = 0.4
inner_lx = block_lx + horizontal_depth
inner_rx = block_rx - horizontal_depth
inner_height = block_y + vertical_depth

#blockList = [(block_lx, block_y), (block_rx, block_y), (block_rx, block_height), (inner_rx , block_height), (inner_rx, inner_height),  (inner_lx, inner_height), (inner_lx, block_height), (block_lx, block_height), (block_lx, block_y)]
blockList = [(block_lx, block_y), (block_rx, block_y), (block_rx, inner_height), (inner_rx , inner_height), (inner_rx, block_height),  (inner_lx, block_height), (inner_lx, inner_height), (block_lx, inner_height), (block_lx, block_y)]

drawing.add(dxf.polyline(blockList))



# Saving file now.
drawing.save()
print "Check file " + filename + ".dxf in current directory."
