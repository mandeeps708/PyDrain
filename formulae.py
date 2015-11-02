from dxfwrite import DXFEngine as dxf
import csv
import math
filename =raw_input('Enter a new name for the file:')
drawing = dxf.drawing(filename+'.dxf')
p9=(-0.8465,215.8)
p10=(0.8465,215.8)

#drawing.add(dxf.line(p9, p10, color=7))

p1=(-1.25,216.7)
p2=(-1.05,217.05)
p3=(-0.85,217.05)
p4=(-0.65,216.4)
p5=(0.65,216.4)
p6=(0.85,217.05)
p7=(1.05,217.05)
p8=(1.25,216.7)
#p1x=10
#p1y=20
#p2x=15
#p2y=50
#theta=63.25
#px=60
#py=100

def solve(p1x, p1y, p2x, p2y, px, py, theta):
    m1=(p1y-p2y)/(p1x-p2x)
    m2=math.tan(theta*(math.pi)/180)
    print(m2)
    if(m1==m2):
        return -1
    c1=(p2y-m1*(p2x))
    c2=(py-m2*(px))
    x=(c2-c1)/(m1-m2)
    y=m2*x+c2
    print x,y
    return x,y

#solve(10,20,15,50,60,100,63.25)
a,b=solve(-1.25,216.7,-1.05,217.05,-0.8465,215.8,180-63.45)
solve(1.25,216.7, 1.05,217.05,0.8465,215.8,63.45)
drawing.add(dxf.line((-1.25,216.7),(-1.05,217.05), color=7))
drawing.add(dxf.line((-0.8465,215.8),(a,b), color=7))
#drawing.add(dxf.line(p1, p2, color=7))
#drawing.add(dxf.line(p2, p3, color=7))
#drawing.add(dxf.line(p3, p4, color=7))
#drawing.add(dxf.line(p4, p5, color=7))
#drawing.add(dxf.line(p5, p6, color=7))
#drawing.add(dxf.line(p6, p7, color=7))
#drawing.add(dxf.line(p7, p8, color=7))
drawing.add_layer('TEXTLAYER', color=2)
drawing.add(dxf.text('Mandeep', insert=(0, 0.2), layer='TEXTLAYER'))
drawing.save()
print "Check file test.dxf in current directory."
