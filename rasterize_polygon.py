import rasterio
import geopandas as gpd
from rasterio.features import rasterize
import numpy as np
import fiona
import shapely
from shapely.geometry import shape
from shapely.geometry import shape, mapping
from shapely.geometry.polygon import Polygon
import rasterio.features
import os

os.makedirs("train_labels", exist_ok = True)
# read in polygons
lake_region = "2023_SIGSPATIAL_Cup_data_files/lake_polygons_training.gpkg"

keys = {}
image_geometry_dict = {}
for layername in fiona.listlayers(lake_region):
    with fiona.open(lake_region, layer=layername) as src:
        print(layername, len(src))
        for g in src:
            image = g['properties']['image'] # get image associated with
            geom = g['geometry']
            print(geom)
            values = []
            image_geometry = image_geometry_dict.get(image)
            if image_geometry is None:
                values.append(geom)
            else:
                values = image_geometry
                values.append(geom)
            
            image_geometry_dict[image] = values
            print(" --------- \n")

# output schema
shp_schema = {
    'geometry': 'Polygon',
    'properties': {'pixelvalue': 'int',
    'region_id': 'int',
    'image': 'str'}
}
for key in image_geometry_dict:
    output = "train_labels/"+key
    raster_region = "2023_SIGSPATIAL_Cup_data_files/"+key
    raster = rasterio.open(raster_region)
    geom = image_geometry_dict[key]

    all_shapes = []
    for g in geom:
        polygon = Polygon(shape(g))
        all_shapes.append(polygon)
    # for each key,value pair,
    # out put rasterized polygon, named with raster file name
    rasterized_lakes = rasterize(all_shapes,
    out_shape=raster.shape,
    fill=0,
    all_touched=False,
    transform=raster.transform,
    default_value=1,
    dtype=np.uint32
    )

    with rasterio.open(
            output, "w",
            driver = "GTiff",
            crs = raster.crs,
            transform = raster.transform,
            dtype = rasterio.uint8,
            count = 1,
            width = raster.width,
            height = raster.height) as dst:
        dst.write(rasterized_lakes, indexes = 1)




