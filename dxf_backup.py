from dxfwrite import DXFEngine as dxf
import csv

filename ="test.dxf"
drawing = dxf.drawing(filename)
drawing.add(dxf.line((0,0), (5,19), color=7))

ans=raw_input("Do you want have values from csv file or default?(y/N)?")
if(ans=='y'):
    f = open('coord.csv')
    data = [row for row in csv.reader(f)]
    listt=[]
    #for coord in csv_f:
       #print coord
        #drawing.add(dxf.line(c, d, color=7))
    count=1
    for i in range(len(data)-1):
        listt.append(data[i])
        print listt
        print i
        c=tuple(data[i])
        d=tuple(data[i+1])
        if count<10:
            #print c,d
            print 'hi',i
            drawing.add(dxf.line(c, d, color=7))
        else:
            print count
    drawing.add(dxf.line(tuple(data[-1]),tuple(data[0]),color=7))
    print listt
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
#    for x,coord in plist:
#   length=len(plist)
#   print length
#   i=0
#   j=i+1
#   k=j+1
#   l=k+1
#   for x in range(len(plist)):
#       #print(plist[i])
#       #print(plist[i+1])
#       print plist[i]
#       print plist[j]
#       print plist[k]
#       print plist[l]
#       drawing.add(dxf.line((plist[i],plist[j]),(plist[k],plist[l]) , color=7))
#       #i=i+1
#       i=i+2

drawing.add_layer('TEXTLAYER', color=2)
drawing.add(dxf.text('Mandeep', insert=(0, 0.2), layer='TEXTLAYER'))
drawing.save()
print "Check file test.dxf in current directory."
