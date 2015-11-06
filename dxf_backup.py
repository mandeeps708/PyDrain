from dxfwrite import DXFEngine as dxf
import csv
import math

filename ="test.dxf"
drawing = dxf.drawing(filename)
drawing.add(dxf.line((0,0), (5,19), color=7))

ans=raw_input("Do you want have values from csv file or default?(y/N)?")
if(ans=='y'):
    f = open('coord.csv')
    data = []
    for row in csv.reader(f):
        if(row.isdigit()):
            data.append(row)
    #for coord in csv_f:
       #print coord
        #drawing.add(dxf.line(c, d, color=7))
    drawconti(data)

    #drawing.add(dxf.line(tuple(data[-1]),tuple(data[0]),color=7))
    #print listt
#   for i in range(len(data)):
#       print i
#       print 'hi'
#       print data[i][0],data[i][1]
#       print data[i+1][0], data[i+1][1]

else:
    print "Default values taken!"
    plist=[0,0,5,10,15,10,20,0,35,0,40,10,50,10,55,0,55,0,55,0];
    #plist=['0','0','5','10','15','10','20','0']
    print plist
print "Base created"


######### Cut section #########

print "Now cut section"


def solve(p1x, p1y, p2x, p2y, px, py, theta):
    m1=(p1y-p2y)/(p1x-p2x)
    m2=math.tan(theta*(math.pi)/180)
    if(m1==m2):
        return -1
    c1=(p2y-m1*(p2x))
    c2=(py-m2*(px))
    x=(c2-c1)/(m1-m2)
    y=m2*x+c2
    return x,y

a1,b1=solve(-1.25,216.7,-1.05,217.05,-0.8465,215.8,180-63.45)
print a1,b1

count=0
for i in range(len(data)-1):
    count=count+1
    a=tuple(data[i])
    b=tuple(data[i+1])
    if count >=11:
        print data[i]
        count=count+1
        drawing.add(dxf.line(a, b, color=7))
    drawing.add(dxf.line(tuple(data[-1]),(a1,b1),color=7))

drawing.add_layer('TEXTLAYER', color=2)
drawing.add(dxf.text('Mandeep', insert=(0, 0.2), layer='TEXTLAYER'))
drawing.save()
print "Check file test.dxf in current directory."


def drawconti(data):
    for i in range(len(data)-1):
        #print listt
        #print i
        c=tuple(data[i])
        d=tuple(data[i+1])
        if i<10:
            #print c,d
            print 'hi',i
            drawing.add(dxf.line(c, d, color=7))
        else:
            print i
