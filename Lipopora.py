from netCDF4 import Dataset
import numpy
from PIL import Image, ImageDraw, ImageChops
import os.path

folder = 'D:\\CT scan Lipopora\\Lipopora\\tomoHiRes_nc'
#print(dataset.file_format)
#print(dataset.dimensions.keys())
#print(dataset.dimensions['tomo_xdim'])
#print(dataset.dimensions['tomo_ydim'])
#print(dataset.dimensions['tomo_zdim'])
#print(dataset.variables.keys())
#print(dataset.variables['tomo'])
#print(dataset.variables['tomo'].shape)
#print(dataset.variables['tomo'][10,10,10])
#print(dataset.variables['tomo'][10,500,500])
j = 0
mask = Image.new("L", (2520,2520))
maskdraw = ImageDraw.Draw(mask)
maskdraw.ellipse((180,180,2520-180,2520-180),"white")

vert_list = []

def add_face( vert1, vert2, vert3, vert4 ):
    return


def add_cube( x, y , z):
    cube_vert = []
    for i in range(2):
        key_x = x + i
        for j in range(2):
            key_y = y + j
            for k in range(2):
                key_z = z + k
                vert_key = str(key_x)+"_"+str(key_y)+"_"+str(key_z)
                if not vert_list[vert_key]:
                    vert_list[vert_key] = 1
                cube_vert.append( vert_list[vert_key])
    add_face( cube_vert[0], cube_vert[1], cube_vert[2], cube_vert[3] )
    add_face( cube_vert[4], cube_vert[5], cube_vert[6], cube_vert[7] )
    add_face( cube_vert[0], cube_vert[1], cube_vert[2], cube_vert[3] )
    add_face( cube_vert[0], cube_vert[1], cube_vert[2], cube_vert[3] )
    add_face( cube_vert[0], cube_vert[1], cube_vert[2], cube_vert[3] )
    add_face( cube_vert[0], cube_vert[1], cube_vert[2], cube_vert[3] )

    return

for i in range(164):
    num = '00000000' + str(i)
    filename = 'D:/CT scan Lipopora/Lipopora/tomoHiRes_nc/block' + num[-8:] + '.nc'
    print( filename )
    dataset = Dataset(filename)

    (zlen,xlen,ylen) = dataset.variables['tomo'].shape
    for z in range(zlen):
        idx = '000000' + str(j)
        img_name = 'HiResdata2/' + idx[-5:] + '.tif'

        if os.path.isfile(img_name):
            print(img_name+ " already exists")
            #continue
        else:
            print(img_name+ " processing...")

            tomo_z = numpy.array( dataset.variables['tomo'][z])
            #print(dataset.variables['tomo'][z])

            #tomo_z += 1
            #tomo_z = tomo_z / 128
            for x in range(xlen):
                for y in range(ylen):
                    val = tomo_z[x,y]
                    if val < 10500:
                        tomo_z[x,y] = 0
                    elif val >= 13000:
                        tomo_z[x, y] = 255
                    else:
                        val = ( val - 10500 ) / 20
                        tomo_z[x,y] = 128 + val
                    #elif tomo_z[x, y] < 11000:
                    #    tomo_z[x, y] = 128
                    #elif tomo_z[x, y] < 11500:
                    #    tomo_z[x, y] = 160
                    #elif tomo_z[x,y] < 12000:
                    #    tomo_z[x, y] = 192
                    #elif tomo_z[x, y] < 12500:
                    #    tomo_z[x, y] = 224
                    #else:
                    #    tomo_z[x, y] = 255
                    #add_cube( x, y, z, vert_list )
            #min = numpy.amin( tomo_z )
            #max = numpy.amax(tomo_z)
            #avrg = numpy.average( tomo_z )
            #median = numpy.median( tomo_z)
            #print("max, min, avrage, median", max, min, avrg, median)
            #tomo_z = tomo_z / 78
            #tomo_z -= 9800
            #tomo_z = tomo_z / 32

            im = Image.fromarray(numpy.uint8(tomo_z))
            out=ImageChops.darker(im,mask)

            #print(im.mode, im.size)
            out.save(img_name)
        j+= 1
        #break
    #break
#8966-38149
#9346-37665



mask.save("mask.tif")