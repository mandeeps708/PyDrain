from dxfwrite import DXFEngine as dxf
import csv
filename =raw_input('Enter a new name for the file:')
drawing = dxf.drawing(filename+'.dxf')
points=[]
count=0
with open('data.csv', 'rb') as csvfile:
    file = csv.reader(csvfile, delimiter=' ')
    for row in file:
        joined=', '.join(row)
        print joined
        plist=joined.split(",")
        print row
        points.append(joined)
        print plist[:1]
        count+=1
print points
for x in range(count):
    first=points[x]
    second=points[(x+1)%count]
    p1='('+first+')'
    print first.split(",")
    print first
    print second
    drawing.add(dxf.line((first), (second), color=7))
p8=(-0.8465,215.8)
p9=(0.8465,215.8)
drawing.add(dxf.line(p8, p9, color=7))

p1=(-1.25,216.7)
p2=(-1.05,217.05)
p3=(-0.85,217.05)
p4=(-0.65,216.4)
p5=(0.65,216.4)
p6=(0.85,217.05)
p7=(1.05,217.05)
p8=(1.25,216.7)

drawing.add(dxf.line(p1, p2, color=7))
drawing.add(dxf.line(p2, p3, color=7))
drawing.add(dxf.line(p3, p4, color=7))
drawing.add(dxf.line(p4, p5, color=7))
drawing.add(dxf.line(p5, p6, color=7))
drawing.add(dxf.line(p6, p7, color=7))
drawing.add(dxf.line(p7, p8, color=7))
drawing.add_layer('TEXTLAYER', color=2)
drawing.add(dxf.text('Mandeep', insert=(0, 0.2), layer='TEXTLAYER'))
drawing.save()
print "Check file test.dxf in current directory."
