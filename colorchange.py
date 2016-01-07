from rgbcie import rgbcie
from phue import Bridge
import math
import random
import time
from PIL import Image, ImageDraw

bridge = Bridge('192.168.2.113')        # Connect to Bridge
#converter = Converter()
#rgbcie = converter.rgbToCIE1931         # Set rgbcie as conversionmethod
couch = bridge.lights[0]                # grab Couch
crad = 50
red, green, blue = (.692,.308), (.17,.7), (.153,.048)
area = (-green[1]*blue[0] + red[1]*(-green[0]+blue[0]) + red[0]*(green[1]-blue[1]) + green[0]*blue[1])
print (red, green, blue, area)
couch.on = True
img = Image.open("path.bmp")
draw = ImageDraw.Draw(img)

### Set light l of bridge b to rgb with transitiontime val
def trans(b, l,rgb,val):
    b.lights[l].on = True
    xy = rgbcie(rgb[0],rgb[1],rgb[2])
    b.set_light(l+1,'xy',(xy[0],xy[1]),transitiontime=val)



### Distance to diagonal correct?
def chkdiag(x):
    return distdiag(x)>crad

### Inside rgb-Space?
def chkbox(x):
    return ((x[0] in range(1,256)) and (x[1] in range(1,256)) and (x[2] in range(1,256)))

### Insida Garmut in xy?
def chktrngl(tmp):
    x = rgbcie(tmp[0],tmp[1],tmp[2])
    s = (1/area)*(red[1]*blue[0]  - red[0]*blue[1]  + (blue[1]- red[1])*x[0]   + (red[0]  - blue[0])*x[1])
    t = (1/area)*(red[0]*green[1] - red[1]*green[0] + (red[1] - green[1])*x[0] + (green[0]- red[0])*x[1])
    return (s>0) and (t>0) and (1-s-t>0)


    


### Distance of a point to the diagonal
def distdiag(x):
    pline = (x[0]+x[1]+x[2])/3
    return math.sqrt((x[0]-pline)**2+(x[1]-pline)**2+(x[2]-pline)**2)

def cone(x):
    pline = (x[0]+x[1]+x[2])/3
    dist = math.sqrt((x[0]-pline)**2+(x[1]-pline)**2+(x[2]-pline)**2)
    return 20+80*(math.sqrt(2*pline**2)/math.sqrt(3*(255**2)))


### Find a random starting point
def findrndsp():
    test = False
    x = (0,0,0)
    while (not test):
        x = [random.randint(30,225),random.randint(30,225),random.randint(30,225)]
        print distdiag(x)
        test = chkdiag(x) and chktrngl(x)
    return x

### Find random direction with velocity v
def findrnddir(v):
    lmbd = random.uniform(-math.pi,math.pi)
    phi = math.acos(2*random.uniform(0,1)-1)
    return [math.sqrt(v)*math.sin(lmbd)*math.cos(phi), math.sqrt(v)*math.sin(lmbd)*math.sin(phi), math.sqrt(v)*math.cos(lmbd)]



### Move x in random direction with velocityvector v, diag-radius d,  within boundaries of RGB
def validmove(x, vv):
    tmp = [0,0,0]
    for i in range(0,3):
        tmp[i] = int(round(x[i]+vv[i]))
    if not chkdiag(tmp):
        print "Failed Diagonal"
        return False
    elif not chkbox(tmp):
        print "Failed Box"
        return False
    elif not chktrngl(tmp):
        print "Failed Triangle"
        return False
    return True


def move(x,vv):
    return [int(round(x[i]+vv[i])) for i in range(0,3)]
#    tmp = [0,0,0]
#    for i in range(0,3):
#        tmp[i] = int(round(x[i]+vv[i]))
#    return tmp

point = findrndsp()
direct = findrnddir(50)
path = [(1000*rgbcie(point[0], point[1], point[2])[0],1000*rgbcie(point[0], point[1], point[2])[1])]
#for i in range(0,40):
#     print "Step " + str(i) + ":" + str(point) + " (dst: " + str(distdiag(point)) + ")"
#    print validmove(point, direct)
while(True):
    trans(bridge, 0,point,20)
    print str(point) + " (dst: " + str(round(distdiag(point),2)) + ", xy: " + str([round(x, 2) for x in rgbcie(point[0],point[1],point[2])]) + ", vel:" + str([round(x,2) for x in direct]) + ")"
    time.sleep(2)
    while (not validmove(point, direct)):
        direct = findrnddir(50)
    point = move(point, direct)
    path.append((1000*rgbcie(point[0], point[1], point[2])[0],1000*rgbcie(point[0], point[1], point[2])[1]))
    draw.line(path,fill=(0,0,0))
    draw.point(path,fill=(255,255,255))
    img.save("pathp.bmp")


                        
