from netCDF4 import Dataset
import numpy
from PIL import Image, ImageDraw, ImageChops
import os.path

folder = 'D:\\RSES_SamLee_Lipopora_lissaANU59521J\\tomoLoRes_roi_nc'
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

def convert_val( val ):
    if val < 11000:
        return  0
    elif val >= 21000:
        return 255
    else:
        val = (val - 11000) / 200
        return 192 + val


for i in range(2):
    num = '00000000' + str(i)
    filename = 'D:/RSES_SamLee_Lipopora_lissaANU59521J/tomoLoRes_roi_nc/block' + num[-8:] + '.nc'
    print( filename )
    dataset = Dataset(filename)

    (zlen,xlen,ylen) = dataset.variables['tomo'].shape
    for z in range(zlen):
        mask = Image.new("L", (656, 656))
        maskdraw = ImageDraw.Draw(mask)
        #maskdraw.ellipse((15, 15, 635, 635), "white")
        #maskdraw.rectangle((15, 15, 460, 480), "white")
        maskdraw.polygon( (5,15, 5,350, 15,350, 55, 480, 460,480, 460,54, 362,15 ), "white")
        #   maskdraw.rectangle( ( 0, 480, 656, 656 ), "black")
        maskdraw.polygon(
            (26, 388, 143, 468, 272, 530, 365, 552, 530, 560, 525, 571, 405, 587, 328, 588, 265, 570, 168, 523,
             87, 470, 23, 425), "black")

        idx = '000000' + str(j)
        foldername = 'D:/RSES_SamLee_Lipopora_lissaANU59521J/tomoLoRes_roi_nc/LowResdata7/'
        img_name =  foldername + idx[-5:] + '.tif'
        img_name2 = foldername + idx[-5:] + '_2.tif'
        img_name3 = foldername + idx[-5:] + '_mask.tif'

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
                    #print(val)
                    tomo_z[x,y] = convert_val(val)
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
            for x in range(xlen):
                for y in range(ylen):
                    if tomo_z[x,y] == 0:
                        continue
                    else:
                        x1 = max( 0, x-2)
                        y1 = max( 0, y-2)
                        x2 = min( xlen-1, x+2)
                        y2 = min( ylen-1, y+2)
                        zero_count = 0
                        filter_count = 0
                        for filterx in range(x1,x2  ):
                            for filtery in range(y1,y2):
                                val = tomo_z[filterx,filtery]
                                #print( x, y, "check", filter_count, filterx, filtery, val )
                                filter_count += 1
                                if val == 0:
                                    zero_count += 1
                        if zero_count > 10:
                            #print( "erase", x, y, zero_count)
                            maskdraw.point((y,x),"black")
                            #tomo_z[filterx,filtery] = 0
                        #else:
                            #print( "no erase", x, y, zero_count)


            im = Image.fromarray(numpy.uint8(tomo_z))
            out=ImageChops.darker(im,mask)
            #print(im.mode, im.size)
            out.save(img_name)
            #im.save(img_name2)
            #mask.save(img_name3)
        j+= 1
        #break
    #break
#8966-38149
#9346-37665



mask.save("mask.tif")