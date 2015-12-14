from dxfwrite import DXFEngine as dxf
import csv
import math
import pdb
import os

# ######### Declaration ##########
points = []
data = []
area = 0
blockList = []
inner_height = 0

extraCuttingAreaL = 0
extraFillingAreaL = 0
extraCuttingAreaR = 0
extraFillingAreaR = 0

# Getting filename with which the file is to be saved.
filename = raw_input('Enter a new name for the file:')
drawing = dxf.drawing(filename+'.dxf')

# CSV file input.
print '\nCSV files in the current directory'
os.system("ls *.csv")
try:
    csvfile = raw_input('\nEnter the name of CSV file (without extension):')
    f = open(csvfile+'.csv')
except NameError and IOError:
    print '\n ##### Check file name! File ' + csvfile + '.csv not found#####\n'
    print 'Try using one from the following: (without extension)'
    os.system("ls *.csv")
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
            # pdb.set_trace()
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
                               inner_length

                             <----length----->

"""


def block(length, height, inner_height, inner_length):
    block_lx = -length / 2
    block_rx = length / 2
    block_y = float(elem1[1])
    vertical_depth = (length - inner_length) / 2

    drawing.add(dxf.line((block_lx, block_y), (block_rx, block_y), color=75,
                         layer='Block'))

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

    drawing.add(dxf.polyline(blockList, color=75, layer='Block'))
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

"""
This drawconti(data) will create the base of the drain something like following.
              __________                                ___________
             /          \                              /           \
            /            \                            /             \
           /              \                          /               \
          /                \                        /                 \
         /                  \                      /                   \
________/                    \                    /                     \________
                              \__________________/

"""

drawconti(data)

# pdb.set_trace()  # for debugging (tracing)

points = points[:-1]

theta = 180 - datum(12, 0)
theta2 = 180 - theta


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
intersectingL_x4, intersectingL_y4 = solve(datum(3, 0), datum(3, 1),
                                           datum(4, 0), datum(4, 1),
                                           datum(11, 0), datum(11, 1), theta)

# pdb.set_trace()

"""
The following are the different cases to check to which line the working space
intersects. (for the left side)
"""

if intersectingL_x1 <= datum(1, 0) and intersectingL_x1 >= datum(0, 0):
    finalL_x = intersectingL_x1
    finalL_y = intersectingL_y1
    coordinateL = tuple((str(finalL_x), str(finalL_y)))
    points.insert(1, coordinateL)

elif intersectingL_x2 >= datum(1, 0) and intersectingL_x2 <= datum(2, 0):
    finalL_x = intersectingL_x2
    finalL_y = intersectingL_y2
    coordinateL = tuple((str(finalL_x), str(finalL_y)))
    points.insert(2, coordinateL)

elif intersectingL_x3 >= datum(2, 0) and intersectingL_x3 <= datum(3, 0):
    finalL_x = intersectingL_x3
    finalL_y = intersectingL_y3
    coordinateL = tuple((str(finalL_x), str(finalL_y)))
    points.insert(3, coordinateL)

elif intersectingL_x4 >= datum(3, 0) and intersectingL_x4 <= datum(4, 0):
    finalL_x = intersectingL_x4
    finalL_y = intersectingL_y4
    coordinateL = tuple((str(finalL_x), str(finalL_y)))
    points.insert(4, coordinateL)

else:
    print 'Not a valid case. Possible Error: Wrong angle.'
    exit()

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
intersectingR_x4, intersectingR_y4 = solve(datum(6, 0), datum(6, 1),
                                           datum(5, 0), datum(5, 1),
                                           datum(10, 0), datum(10, 1), theta2)


"""
The following are the different cases to check to which line the working space
intersects. (for the right side)
"""

if intersectingR_x1 >= datum(8, 0) and intersectingR_x1 <= datum(9, 0):
    finalR_x = intersectingR_x1
    finalR_y = intersectingR_y1
    coordinateR = tuple((str(finalR_x), str(finalR_y)))
    index = points.index((str(datum(8, 0)), str(datum(8, 1))))
    points.insert(index + 1, coordinateR)

elif intersectingR_x2 >= datum(7, 0) and intersectingR_x2 <= datum(8, 0):
    finalR_x = intersectingR_x2
    finalR_y = intersectingR_y2
    coordinateR = tuple((str(finalR_x), str(finalR_y)))
    index = points.index((str(datum(7, 0)), str(datum(7, 1))))
    points.insert(index + 1, coordinateR)

elif intersectingR_x3 >= datum(6, 0) and intersectingR_x3 <= datum(7, 0):
    finalR_x = intersectingR_x3
    finalR_y = intersectingR_y3
    coordinateR = tuple((str(finalR_x), str(finalR_y)))
    index = points.index((str(datum(6, 0)), str(datum(6, 1))))
    points.insert(index + 1, coordinateR)

elif intersectingR_x4 >= datum(5, 0) and intersectingR_x4 <= datum(6, 0):
    finalR_x = intersectingR_x4
    finalR_y = intersectingR_y4
    coordinateR = tuple((str(finalR_x), str(finalR_y)))
    index = points.index((str(datum(5, 0)), str(datum(5, 1))))
    points.insert(index + 1, coordinateR)

else:
    print 'Not a valid case. Possible Error: Wrong angle.'
    exit()

# Intersection points.
intersectL = tuple((finalL_x, finalL_y))
intersectR = tuple((finalR_x, finalR_y))

"""

                           __________                                ___________
      intersectL          /          \                              /           \       intersectR
                -------->/\           \                            /            /\<---------
                        /  \           \                          /            /  \
                       /    \           \                        /            /    \
                      /      \           \                      /            /      \
_____________________/        \           \____________________/            /        \___________________
                         theta/\                                           /\ theta2
                             (__\_________________________________________/__)
"""

# pdb.set_trace()
indexL = points.index(coordinateL)
indexR = points.index(coordinateR)

points = points[indexL:indexR+1]


drawing.add_layer('workingSpace', color=7)

"""
The following block of code creates Working space or Cutting plane

        \                           /
         \                         /
          \                       /
           \                     /
            \                   /
       elem2 \_________________/elem1

"""

# elem1 and elem2 are the base points known of the cutting plane.
elem1 = tuple(data[10])
elem2 = tuple(data[11])
drawing.add(dxf.line(elem1, elem2, color=7, layer='workingSpace'))
drawing.add(dxf.line(intersectL, elem2, color=7, layer='workingSpace'))
drawing.add(dxf.line(elem1, intersectR, color=7, layer='workingSpace'))

points.extend((elem1, elem2, coordinateL))


# pdb.set_trace()  # for debugging (tracing)


# ####################### Calculating Area Here. #########################

# if the working space base length is greater then the drain base length.
if float(elem2[0]) < datum(4, 0) and float(elem1[0]) > datum(5, 0):
    if float(elem2[1]) < float(points[3][1]):
        print 'Cutting plane is below the drain base'
        for i in range(0, len(points)-1):
            area += det(points[i][0], points[i][1], points[i+1][0],
                        points[i+1][1])

        print 'Total Base Cutting Area is: ', areaNegative(area)
        """

                             __________                                ___________
        intersectL          /          \                              /           \       intersectR
                  -------->/\           \                            /            /\<---------
                          /  \           \                          /            /  \
                         /    \           \               |        /            /    \
                        /      \           \   Drain base v       /            /      \
        _______________/        \           \____________________/            /        \____________
                           theta/\                area                       /\ theta2
                               (__\_________________________________________/__)
                                  elem2                                   elem1
        """

    else:
        print 'Cutting plane is above the drain base'

        intersect_cut_xL, intersect_cut_yL = solve(datum(3, 0), datum(3, 1),
                                                   datum(4, 0), datum(4, 1),
                                                   datum(11, 0), datum(11, 1),
                                                   0)
        intersect_cut_xR, intersect_cut_yR = solve(datum(5, 0), datum(5, 1),
                                                   datum(6, 0), datum(6, 1),
                                                   datum(11, 0), datum(11, 1),
                                                   0)
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

        """

                             __________                                ___________
        intersectL          /          \                              /           \       intersectR
                  -------->/\           \<---left_cutting            /            /\<---------
                          /  \           \                          /            /  \
                         /    \           \       right_cutting--->/            /    \
                        /      \           \                      /            /      \
                 ______/        \           \                    /            /        \______
                                 \           \                  /            /
                                  \___________\________________/____________/
                               elem2           \ fillingArea  /           elem1
                                                \____________/

        """

        for i in range(0, len(coordListL)-1):
            cuttingL += det(coordListL[i][0], coordListL[i][1],
                            coordListL[i+1][0], coordListL[i+1][1])
        for i in range(0, len(coordListR)-1):
            cuttingR += det(coordListR[i][0], coordListR[i][1],
                            coordListR[i+1][0], coordListR[i+1][1])
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
        print 'Total Base Cutting Area is: ', total_cutting
        print 'Total Base Filling Area is: ', fillingArea
        # intersect_index = points.index((str(datum(8,0)), str(datum(8,1))))
        # not yet implemented.
        # adding areas of left and right blocks that are created. First we
        # have to find out the intersection point.

else:
    """
    if the working space base length is less than the drain base length. Then
    it will have to reconsider some extra cases. Some extra cutting & filling
    will be there.
    """

    print 'Sorry. This case is not yet implemented. Contact the Dev. Working \
space base length is less than the drain base length.'


# ######### Placing Block Now ##########

length = datum(13, 0)
height = datum(13, 1)
inner_height = datum(13, 2)
inner_length = datum(13, 3)
drawing.add_layer('Block', color=4)
blockList = block(length, height, inner_height, inner_length)
if float(elem2[0]) <= blockList[0][0] and float(elem1[0]) >= blockList[1][0]:
    print ''
else:
    print 'Block length should be less than the working space length.'
    exit()


# Covering area after placing block.

drawing.add_layer('extension', color=4)
margin1 = datum(14, 0)
margin2 = datum(14, 1)
blockFill_lf = (blockList[-2][0] - margin1, blockList[-2][1])
blockFill_ll = (blockList[-2][0] - margin1 - margin2, datum(0, 1))
blockFill_rf = (blockList[2][0] + margin1, blockList[2][1])
blockFill_rl = (blockList[2][0] + margin1 + margin2, datum(0, 1))

drawing.add(dxf.line(blockList[-2], blockFill_lf, color=100, layer='extension'))
drawing.add(dxf.line(blockFill_lf, blockFill_ll, color=100, layer='extension'))
drawing.add(dxf.line(blockList[2], blockFill_rf, color=100, layer='extension'))
drawing.add(dxf.line(blockFill_rf, blockFill_rl, color=100, layer='extension'))
# pdb.set_trace()

# Intersection point of extension filling line with the working space slanted.
lFillIntersectx, lFillIntersecty = solve(blockFill_lf[0], blockFill_lf[1],
                                         blockFill_ll[0], blockFill_ll[1],
                                         datum(11, 0), datum(11, 1),
                                         theta)
lFillIntersect = tuple((lFillIntersectx, lFillIntersecty))

# Angle between the forward slanted line of base with the x-axis.
angleSlopeL = slope(datum(1, 0), datum(1, 1), datum(2, 0), datum(2, 1))

# Intersection of drain left slanted line with the block extension line.
extensionIntersectLx, extensionIntersectLy = solve(blockFill_lf[0],
                                                   blockFill_lf[1],
                                                   blockFill_ll[0],
                                                   blockFill_ll[1],
                                                   datum(1, 0), datum(1, 1),
                                                   angleSlopeL)
extensionIntersectL = tuple((extensionIntersectLx, extensionIntersectLy))


# Intersection point of extension filling line with the working space slanted.
rFillIntersectx, rFillIntersecty = solve(blockFill_rf[0], blockFill_rf[1],
                                         blockFill_rl[0], blockFill_rl[1],
                                         datum(10, 0), datum(10, 1),
                                         theta2)
rFillIntersect = tuple((rFillIntersectx, rFillIntersecty))

# Angle between the backward slanted line of base with the x-axis.
angleSlopeR = slope(datum(8, 0), datum(8, 1), datum(7, 0), datum(7, 1))

# Intersection of drain right slanted line with the block extension line.
extensionIntersectRx, extensionIntersectRy = solve(blockFill_rf[0],
                                                   blockFill_rf[1],
                                                   blockFill_rl[0],
                                                   blockFill_rl[1],
                                                   datum(8, 0), datum(8, 1),
                                                   angleSlopeR)
extensionIntersectR = tuple((extensionIntersectRx, extensionIntersectRy))
# Different Cases for extra outer filling and cutting.

"""
Case I:
    Checks if the block extension line cuts the leftover area.
"""

if extensionIntersectLy < finalL_y and extensionIntersectLy > datum(1, 1):
    # if the extension point lies at the right of the leftover area.
    if blockFill_lf[0] > lFillIntersectx and blockFill_lf[1] > lFillIntersecty:

        # if the extension intersect point lies above the base drain.
        if extensionIntersectLy > datum(1, 1):
            extraFillingCoordL = [extensionIntersectL, (datum(1, 0),
                                                        datum(1, 1)),
                                  blockFill_ll, extensionIntersectL]
        else:
            print 'This case is not implemented yet. The upper portion of \
                block is less than the base level.'
            exit()

        extraCuttingCoordL = [intersectL, extensionIntersectL, lFillIntersect,
                              intersectL]

        extraCuttingAreaL = preArea(extraCuttingCoordL)
        extraCuttingAreaL = areaNegative(extraCuttingAreaL)

        extraFillingAreaL = preArea(extraFillingCoordL)
        extraFillingAreaL = areaNegative(extraFillingAreaL)

        majorFillingCoordL = [lFillIntersect, blockFill_lf, blockList[7],
                              blockList[0], (datum(11, 0), datum(11, 1)),
                              lFillIntersect]
        majorFillingAreaL = preArea(majorFillingCoordL)
        majorFillingAreaL = areaNegative(majorFillingAreaL)

    # if the extension point lies to the left of the leftover area.
    elif blockFill_lf[0] < lFillIntersectx and blockFill_lf[1] > lFillIntersecty:
        print 'extension point lies to right. Not implemented yet.'
        exit()

    else:
        print 'extension point lies in between leftover area.'
        exit()

# if extension line don't cut the leftover area.
else:
    majorFillingCoordL = [blockFill_ll, blockFill_lf, blockList[7],
                          blockList[0], (datum(11, 0), datum(11, 1)),
                          intersectL, (datum(1, 0), datum(1, 1)), blockFill_ll]
    majorFillingAreaL = preArea(majorFillingCoordL)
    majorFillingAreaL = areaNegative(majorFillingAreaL)

# For right hand side
if extensionIntersectRy < finalR_y and extensionIntersectRy > datum(8, 1):
    # if the extension point lies at the right of the leftover area.
    if blockFill_rf[0] < rFillIntersectx and blockFill_rf[1] > rFillIntersecty:

        # if the extension intersect point lies above the base drain.
        if extensionIntersectRy > datum(8, 1):
            extraFillingCoordR = [extensionIntersectR, (datum(8, 0),
                                                        datum(8, 1)),
                                  blockFill_rl, extensionIntersectR]

        else:
            print 'This case is not implemented yet. The upper portion of \
                block is less than the base level.'
            exit()

        extraCuttingCoordR = [intersectR, extensionIntersectR, rFillIntersect,
                              intersectR]

        extraCuttingAreaR = preArea(extraCuttingCoordR)
        extraCuttingAreaR = areaNegative(extraCuttingAreaR)

        extraFillingAreaR = preArea(extraFillingCoordR)
        extraFillingAreaR = areaNegative(extraFillingAreaR)

        majorFillingCoordR = [rFillIntersect, blockFill_rf, blockList[2],
                              blockList[1], (datum(10, 0), datum(10, 1)),
                              rFillIntersect]
        majorFillingAreaR = preArea(majorFillingCoordR)
        majorFillingAreaR = areaNegative(majorFillingAreaR)

    # if the extension point lies to the left of the leftover area.
    elif blockFill_rf[0] > rFillIntersectx and blockFill_rf[1] > rFillIntersecty:
        print 'extension point lies to left. Not implemented yet.'
        exit()

    else:
        print 'extension point lies in between leftover area.'
        exit()

# if extension line don't cut the leftover area.
else:
    majorFillingCoordR = [blockFill_rl, blockFill_rf, blockList[2],
                          blockList[1], (datum(10, 0), datum(10, 1)),
                          intersectR, (datum(8, 0), datum(8, 1)), blockFill_rl]
    majorFillingAreaR = preArea(majorFillingCoordR)
    majorFillingAreaR = areaNegative(majorFillingAreaR)


print '################## Block placed! ###################'

"""

                                _____                       ____
                   /\           |   |                      |  |          /\
                  /  \          |   |                      |  |         /  \
                 /    \         |   |                      |  |        /    \
                /      \        |   |                      |  |       /      \
_______________/        \       |   |______________________|  |      /        \____________
                   theta/\      |                             |     /\ theta2
                       (__\_____|_____________________________|____/__)
                          elem2                                   elem1
"""

print 'Left Major Filling Area: ', majorFillingAreaL
print 'Left Extra Cutting Area: ', extraCuttingAreaL
print 'Left Extra Filling Area: ', extraFillingAreaL

print 'Right Major Filling Area: ', majorFillingAreaR
print 'Right Extra Cutting Area: ', extraCuttingAreaR
print 'Right Extra Filling Area: ', extraFillingAreaR

print 'Total Major Filling Area: ', majorFillingAreaL + majorFillingAreaR
print 'Total Extra Cutting Area: ', extraCuttingAreaL + extraCuttingAreaR
print 'Total Extra Filling Area: ', extraFillingAreaL + extraFillingAreaR


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

# dashed line demo.
# drawing.add(dxf.line((0,0), (25,10),
#             layer='TESTLAYER', linetype='DASHED', color=1))

# Saving file now.
drawing.save()
print "Check file " + filename + ".dxf in current directory."
