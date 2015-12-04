from dxfwrite import DXFEngine as dxf
import csv
import math
import pdb

# ######### Declaration ##########
points = []
data = []
area = 0
blockList = []
inner_height = 0

extraCuttingArea = 0
extraFillingArea = 0

# Getting filename with which the file is to be saved.
filename = raw_input('Enter a new name for the file:')
drawing = dxf.drawing(filename+'.dxf')

# CSV file input.
try:
    csvfile = raw_input('Enter the name of CSV file (without extension):')
    f = open(csvfile+'.csv')
except NameError and IOError:
    print '\n ##### Check file name! File', csvfile, '.csv not found#####\n'
    exit()


# Adding csv lines to list data.
for row in csv.reader(f):
    data.append(row)


# ######################## Functions Defintion #########################

# #### Base Drain #####
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
            drawing.add(dxf.line(element1, element2, color=50, layer='Base'))
            points.append(element1)
        elif i < 11:
            points.append(element1)


""" Solving two equations simultaneously. Here (p1x, p1y) and (p2x, p2y)
are the two points of a line and (px, py) is a single known point of
second line and theta is the angle it makes with x-axis.
"""


def solve(p1x, p1y, p2x, p2y, px, py, theta):
    # m1 and m2 are the slopes of given line.
    m1 = (p1y - p2y)/(p1x - p2x)
    m2 = math.tan(theta*(math.pi)/180)

    # if both lines are parallel.
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


"""
Calculates the pre-area values that are fed to the areaNegative() function
below. It takes one argument as input:
    pList: List containing the coordinates of the boundary of which the
           area is to be calculated.
"""


def preArea(pList):
    pArea = 0
    for i in range(0, len(pList)-1):
        pArea += det(pList[i][0], pList[i][1],
                     pList[i+1][0], pList[i+1][1])
    return pArea


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


"""
The block function takes four inputs and returns blockList. Four inputs are
length of block, height of block, inner height of block and inner length of
base.
                 ^           --             --      ^
                 |           | |           | |      |
                 |           | |           | |      |
                 |           | |___________| |      |
                 |           |_______________|    inner_height
                height
                               <---------->
                               inner_width

                             <----length----->

"""


def block(length, height, inner_height, inner_width):
    block_lx = -length / 2
    block_rx = length / 2
    block_y = float(elem1[1])
    vertical_depth = (length - inner_width) / 2

    drawing.add(dxf.line((block_lx, block_y), (block_rx, block_y), color=75))

    block_height = block_y + height
    horizontal_depth = height - inner_height
    inner_lx = block_lx + vertical_depth
    inner_rx = block_rx - vertical_depth
    inner_y = block_y + horizontal_depth

    blockList = [(block_lx, block_y), (block_rx, block_y),
                 (block_rx, block_height), (inner_rx, block_height),
                 (inner_rx, inner_y),  (inner_lx, inner_y),
                 (inner_lx, block_height), (block_lx, block_height),
                 (block_lx, block_y)]

    drawing.add(dxf.polyline(blockList, color=75))
    return blockList

"""
Finding Slope of a line.
"""


def slope(x1, y1, x2, y2):
    m = (y2 - y1) / (x2 - x1)
    slopedTheta = math.degrees(math.atan(m))
    return slopedTheta


# ################## Calling Functions ####################

drawing.add_layer('Base', color=2)
drawconti(data)

# pdb.set_trace()  # for debugging (tracing)

theta = 180 - datum(12, 0)
theta2 = 180 - theta
points = points[:-1]

""" (finalL_x, finalL_y) are the coordinates of the intersection points
obtained by solving the left side.
"""
intersectingL_x1, intersectingL_y1 = solve(datum(0, 0), datum(0, 1),
                                           datum(1, 0), datum(1, 1),
                                           datum(11, 0), datum(11, 1), theta)
intersectingL_x2, intersectingL_y2 = solve(datum(1, 0), datum(1, 1),
                                           datum(2, 0), datum(2, 1),
                                           datum(11, 0), datum(11, 1), theta)
intersectingL_x3, intersectingL_y3 = solve(datum(2, 0), datum(2, 1),
                                           datum(3, 0), datum(3, 1),
                                           datum(11, 0), datum(11, 1), theta)

if intersectingL_x1 <= datum(1, 0):
    finalL_x = intersectingL_x1
    finalL_y = intersectingL_y1
    coordinateL = tuple((str(finalL_x), str(finalL_y)))
    points.insert(1, coordinateL)

elif intersectingL_x3 >= datum(2, 0):
    finalL_x = intersectingL_x3
    finalL_y = intersectingL_y3
    coordinateL = tuple((str(finalL_x), str(finalL_y)))
    points.insert(3, coordinateL)

else:
    finalL_x = intersectingL_x2
    finalL_y = intersectingL_y2
    coordinateL = tuple((str(finalL_x), str(finalL_y)))
    points.insert(2, coordinateL)


""" (finalR_x, finalR_y) are the coordinates of the intersection points
obtained by solving the right side.
"""
intersectingR_x1, intersectingR_y1 = solve(datum(9, 0), datum(9, 1),
                                           datum(8, 0), datum(8, 1),
                                           datum(10, 0), datum(10, 1), theta2)
intersectingR_x2, intersectingR_y2 = solve(datum(8, 0), datum(8, 1),
                                           datum(7, 0), datum(7, 1),
                                           datum(10, 0), datum(10, 1), theta2)
intersectingR_x3, intersectingR_y3 = solve(datum(7, 0), datum(7, 1),
                                           datum(6, 0), datum(6, 1),
                                           datum(10, 0), datum(10, 1), theta2)

if intersectingR_x1 >= datum(8, 0):
    finalR_x = intersectingR_x1
    finalR_y = intersectingR_y1
    coordinateR = tuple((str(finalR_x), str(finalR_y)))
    index = points.index((str(datum(8, 0)), str(datum(8, 1))))
    points.insert(index, coordinateR)

elif intersectingR_x3 <= datum(7, 0):
    finalR_x = intersectingR_x3
    finalR_y = intersectingR_y3
    coordinateR = tuple((str(finalR_x), str(finalR_y)))
    index = points.index((str(datum(7, 0)), str(datum(7, 1))))
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
# for i in range(10,11):
# elem1 and elem2 are the base points known of the cutting plane.
drawing.add_layer('workingSpace', color=7)

elem1 = tuple(data[10])
elem2 = tuple(data[11])
drawing.add(dxf.line(elem1, elem2, color=7, layer='workingSpace'))
drawing.add(dxf.line(intersectL, elem2, color=7, layer='workingSpace'))
drawing.add(dxf.line(elem1, intersectR, color=7, layer='workingSpace'))

points.extend((elem1, elem2, coordinateL))

pdb.set_trace()  # for debugging (tracing)

# Calculating Area Here.
if float(elem2[1]) < float(points[3][1]):
    print 'cut plane is below the drain base'
    for i in range(0, len(points)-1):
        area += det(points[i][0], points[i][1], points[i+1][0], points[i+1][1])

    print 'Total Cutting Area is: ', areaNegative(area)

else:
    print 'cut plane is above the drain base'
    intersect_cut_xL, intersect_cut_yL = solve(datum(3, 0), datum(3, 1),
                                               datum(4, 0), datum(4, 1),
                                               datum(11, 0), datum(11, 1), 0)
    intersect_cut_xR, intersect_cut_yR = solve(datum(5, 0), datum(5, 1),
                                               datum(6, 0), datum(6, 1),
                                               datum(11, 0), datum(11, 1), 0)
    coordinateL = tuple((str(intersect_cut_xL), str(intersect_cut_yL)))
    coordinateR = tuple((str(intersect_cut_xR), str(intersect_cut_yR)))

    coordListL = points[:3]
    coordListL.append(coordinateL)
    coordListL.append(points[-2])
    coordListL.append(coordListL[0])
    cuttingL = 0
    cuttingR = 0

    coordListR = [coordinateR]
    coordListR += points[5:9]
    coordListR.append(coordListR[0])
    for i in range(0, len(coordListL)-1):
        cuttingL += det(coordListL[i][0], coordListL[i][1], coordListL[i+1][0],
                        coordListL[i+1][1])
    for i in range(0, len(coordListR)-1):
        cuttingR += det(coordListR[i][0], coordListR[i][1], coordListR[i+1][0],
                        coordListR[i+1][1])
    left_cutting = areaNegative(cuttingL)
    right_cutting = areaNegative(cuttingR)

    total_cutting = left_cutting + right_cutting

    fillingList = [coordinateL, coordinateR, (str(datum(5, 0)),
                                              str(datum(5, 1))),
                                             (str(datum(4, 0)),
                                              str(datum(4, 1)))]
    fillingList.append(coordinateL)

    fillingArea = preArea(fillingList)
    fillingArea = areaNegative(fillingArea)
    print 'Total Cutting Area is: ', total_cutting
    print 'Total filling Area is: ', fillingArea
    # intersect_index = points.index((str(datum(8,0)), str(datum(8,1))))
    # not yet implemented.
    # adding areas of left and right blocks that are created. First we
    # have to find out the intersection point.


drawing.add_layer('Block', color=4)
# ######### Placing Block Now ##########

length = 1.3930
height = 0.4100
inner_height = 0.3340
inner_width = 0.9350
blockList = block(length, height, inner_height, inner_width)

# Covering area after placing block.

margin1 = 0.3050
margin2 = 0.3190
blockFill_lf = (blockList[-2][0] - margin1, blockList[-2][1])
blockFill_ll = (blockList[-2][0] - margin1 - margin2, datum(0, 1))
blockFill_rf = (blockList[2][0] + margin1, blockList[2][1])
blockFill_rl = (blockList[2][0] + margin1 + margin2, datum(0, 1))

drawing.add(dxf.line(blockList[-2], blockFill_lf, color=100))
drawing.add(dxf.line(blockFill_lf, blockFill_ll, color=100))
drawing.add(dxf.line(blockList[2], blockFill_rf, color=100))
drawing.add(dxf.line(blockFill_rf, blockFill_rl, color=100))
pdb.set_trace()

# Intersection point of extension filling line with the working space slanted.
lFillIntersectx, lFillIntersecty = solve(blockFill_lf[0], blockFill_lf[1],
                                         blockFill_ll[0], blockFill_ll[1],
                                         datum(11, 0), datum(11, 1),
                                         theta)
lFillIntersect = tuple((lFillIntersectx, lFillIntersecty))

# Angle between the slanted line of base with the x-axis.
angleSlope = slope(datum(1, 0), datum(1, 1), datum(2, 0), datum(2, 1))

# Intersection of drain slanted line with the block extension line.
extensionIntersectx, extensionIntersecty = solve(blockFill_lf[0],
                                                 blockFill_lf[1],
                                                 blockFill_ll[0],
                                                 blockFill_ll[1],
                                                 datum(1, 0), datum(1, 1),
                                                 angleSlope)
extensionIntersect = tuple((extensionIntersectx, extensionIntersecty))

# Different Cases for extra outer filling and cutting.

"""
Case I:
    Checks if the block extension line cuts the leftover area.
"""

if extensionIntersecty < finalL_y and extensionIntersecty > datum(1, 1):
    extraCuttingCoord = [intersectL, extensionIntersect, lFillIntersect,
                         intersectL]
    extraFillingCoord = [extensionIntersect, (datum(1, 0), datum(1, 1)),
                         blockFill_ll, extensionIntersect]

    extraCuttingArea = preArea(extraCuttingCoord)
    extraCuttingArea = areaNegative(extraCuttingArea)

    extraFillingArea = preArea(extraFillingCoord)
    extraFillingArea = areaNegative(extraFillingArea)

    majorFillingCoord = [lFillIntersect, blockFill_lf, blockList[7],
                         blockList[0], (datum(11, 0), datum(11, 1)),
                         lFillIntersect]
    majorFillingArea = preArea(majorFillingCoord)
    majorFillingArea = areaNegative(majorFillingArea)

else:
    majorFillingCoord = [blockFill_ll, blockFill_lf, blockList[7],
                         blockList[0], (datum(11, 0), datum(11, 1)),
                         intersectL, (datum(1, 0), datum(1, 1)), blockFill_ll]
    majorFillingArea = preArea(majorFillingCoord)
    majorFillingArea = areaNegative(majorFillingArea)

print '################## Block placed! ###################'
print 'Major Filling Area: ', majorFillingArea

print 'Extra Cutting Area: ', extraCuttingArea
print 'Extra Filling Area: ', extraFillingArea

"""
if finalL_y < blockList[2][1]:

    if finalL_x < lFillIntersectx:
        extraCuttingCoord = [(lFillIntersectx, lFillIntersecty),
                             intersectL, (datum(2, 0), datum(2, 1)),
                             (datum(3, 0), datum(3, 1)),
                             (extensionIntersectx, extensionIntersecty),
                             blockFill_lf]
        extraCuttingCoord.append(extraCuttingCoord[0])

        extraFillingCoord = [(datum(1, 0), datum(1, 1)), blockFill_ll]

        print 'Everything will fill normally!'

else:
    print 'Will have to calculate cutting and filling differently!'

if blockFill_lf[0] > lFillIntersectx:
    print 'case I'
else:
    print 'case II'
    # AreaFillingL = det()
final_cuttingL = 0
final_cutting = [blockFill_ll]
for i in range(0, len(final_cutting)-1):
    final_cuttingL += det(final_cutting[i][0], final_cutting[i][1],
                          final_cutting[i+1][0], final_cutting[i+1][1])
"""
pdb.set_trace()
# Saving file now.
drawing.save()
print "Check file " + filename + ".dxf in current directory."
