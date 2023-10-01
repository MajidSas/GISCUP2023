import os
from osgeo import gdal

#region1: 17_38", 17_39", 17_40", 18_39", 18_40
#region2: 16_38", 16_39", 16_40", 17_38", 17_39", 17_40
#region3: 14_38", 14_39", 14_40", 15_38", 15_39", 15_40", 16_38", 16_39", 16_40
#region4: 13_38", 13_39", 13_40", 14_38", 14_39", 14_40", 15_38
#region5: 29_43", 29_44", 29_45", 30_43", 30_44", 30_45", 31_44", 31_45
#region6: 27_44", 27_45", 28_43", 28_44", 28_45", 28_46", 29_43", 29_44", 29_45", 29_46

os.makedirs("filter", exist_ok = True)
os.makedirs("filter_dem", exist_ok = True)

folderName = "greenland_dem"
os.makedirs(folderName+"/dem", exist_ok = True)
os.makedirs(folderName+"/dem/region_01", exist_ok = True)
os.makedirs(folderName+"/dem/region_02", exist_ok = True)
os.makedirs(folderName+"/dem/region_03", exist_ok = True)
os.makedirs(folderName+"/dem/region_04", exist_ok = True)
os.makedirs(folderName+"/dem/region_05", exist_ok = True)
os.makedirs(folderName+"/dem/region_06", exist_ok = True)

file_arr = {}
for region_id in range(1,7):
    file_arr[region_id] = {}

file_arr[1] = {"17_38", "17_39", "17_40", "18_39", "18_40"}
file_arr[2] =  {"16_38", "16_39", "16_40", "17_38", "17_39", "17_40"}
file_arr[3] = {"14_38", "14_39", "14_40", "15_38", "15_39", "15_40", "16_38", "16_39", "16_40"}
file_arr[4] = {"13_38", "13_39", "13_40", "14_38", "14_39", "14_40", "15_38"}
file_arr[5] = {"29_43", "29_44", "29_45", "30_43", "30_44", "30_45", "31_44", "31_45"}
file_arr[6] = {"27_44", "27_45", "28_43", "28_44", "28_45", "28_46", "29_43", "29_44", "29_45", "29_46"}


for region_id in range(1,7):
    files = file_arr[region_id]
    for f in files:
        region_id = str(region_id)
        #print(f + "_10m_v4.1")
        f_path = folderName+"/"+f+"_10m_v4.1"+"/"+f+"_10m_v4.1_dem.tif"
        o_path = folderName+"/dem/region_0"+region_id+"/"+f+"_10m_v4.1_dem.tif"
        #reproject to epsg:3857 crop to the same metedata as provided raster
        cmd_1 = "gdalwarp -s_srs EPSG:3413 -t_srs EPSG:3857 -r near -of GTiff " + f_path + " " +o_path
        print(cmd_1)
        os.system(cmd_1)

    region_id = str(region_id)
    #create vrt and merge dem
    cmd_2 = "gdalbuildvrt greenland_dem/dem_index_0"+region_id+".vrt greenland_dem/dem/region_0"+region_id+"/*.tif " 
    print(cmd_2)
    os.system(cmd_2)

    cmd_3 = "gdal_translate -of GTiff -co BIGTIFF=YES -co TILED=YES greenland_dem/dem_index_0"+region_id+".vrt greenland_dem/dem/region_0"+region_id+"/dem_region_0"+region_id+".tif"
    print(cmd_3)
    os.system(cmd_3)

    cmd_4 = "gdalwarp -tr 38.21851414258808 38.21851414258808 -r near -of GTiff greenland_dem/dem/region_0"+region_id+"/dem_region_0"+region_id+".tif filter/dem_region_0"+region_id+".tif"
    print(cmd_4)
    os.system(cmd_4)






