# Data Preprocess
## Requirements:
- GDAL command line tool
- QGIS desktop application
- Python3
- Rasterio Python package


## Data preprocess steps:
Please make sure these specific folders are not present in the current directory, since the script will create the path and generate files: test, train, filter, dem, filter_dem


Run scripts under the same directory as “2023_SIGSPATIAL_Cup_data_files”. 

Data folder can be found here: https://drive.google.com/drive/folders/1cGyDLLmZafQGetRfnqp8NPGrozed6nx-?usp=sharing


### Step 1: rasterize polygons and clip the resulted rasters
```
python3 rasterize_polygon.py
./gdal_clip_polygon.sh
```


### Step 2: merge and align ArcticDEM with provided Greenland ratsters
```
python3 gdal_merge_dem.py
./gdal_clip_dem.sh
```



### Step 3:  clip provided Greenland rasters based on polygon regions
```
./gdal_clip_train_raster.sh
./gdal_clip_test_raster.sh
```


### Following content describe each step in detail:
1.Rasterizing polygons
We use the Rasterio package to read the training polygon GeoPackage, extracting them based on their respective feature name (corresponding to a specific raster image).
Then we rasterize these polygons, setting the output pixel value to 1, if the pixel intersects or overlaps with the respective polygon.

The script is: `rasterize_polygon.py`


We use the GDAL command line to clip the rasterized polygon files according to their respective polygon region extents.
The script is: `gdal_clip_polygon.sh`


2.Downloading ArcticDEM

Download link: https://data.pgc.umn.edu/elev/dem/setsm/ArcticDEM/mosaic/latest/10m

First we download the ArcticDEM data, filtering the files that overlap with the greenland landscape.
Then we use QGIS to visualize and observe the downloaded DEM files. We separate files based on the polygon regions each file covers.

We save all DEM data in the folder named **greenland_dem**.

Within each polygon region, we use the GDAL command line to merge all corresponding files.
To ensure precise alignment with the exact pixel location as in Greenland raster, we rescale DEM pixel size to the same size as in Greenland raster.
Lastly, we align this DEM raster with the respective polygon region extent.

Following steps describe such process:
1. Reproject DEM to epsg:3857
2. Merge DEM if they belong to the same polygon region
3. Rescale the pixel size to align with the Greenland raster pixel size
4. Clip the merged and rescaled DEM to the same extent as each polygon region
Scripts can be found: `gdal_merge_dem.py`, `gdal_clip_dem.sh`


3.Partitioning by region
We use the GDAL command line to clip original rasters according to the extent of the corresponding polygon region.
We have two scripts, one works for generating training data and the other is for testing data.

The script for extracting training data is: `gdal_clip_train_raster.sh`
The script for extracting testing data is: `gdal_clip_test_raster.sh`


This provides us with one image per region for each timestamp, and associated label image for the training data.


All the processed data generated from the previous steps, can be accessed here:
https://drive.google.com/drive/folders/1cGyDLLmZafQGetRfnqp8NPGrozed6nx-?usp=sharing


# Tiling
First, each raster is scaled to 0-1 range, using min-max scaling. For tiling, we used a tile size of 256x256. We filter out the tiles with average height lower than 800 in the DEM images. We noticed that those correspond to much lower altitude regions. We also store the sum of the pixels in each tile, so that we know which tiles don’t contain any pixels associated with lakes. This is done at the start of the notebook Tile+Train.ipynb for training data and Tile+Test.ipynb for test data.


# Model architecture
We used a UNet model with 3 convolution blocks, each followed by a max-pooling layer, and 3 up convolution blocks, each followed by a convolution block. There are residual connections between the convolution blocks at each corresponding level (down,up). We started with the model provided in this file. We also added dropout in the convolution blocks to reduce the chance of overfitting. In our case, each convolution block has the following layers: [Dropout, Conv2d, BatchNorm2d, ReLU, Conv2d, BatchNorm2d, ReLU], and followed by MaxPool2d. Each up convolution block has the following layers [Upsample, Conv2d, BatchNorm2d, ReLU], and followed by a convolution block. The model code is in the file `Tile+Train.ipynb`.

# Training
This part is performed in the file `Tile+Train.ipynb`.


We use the dice loss which is typically used for segmentation problems.
It works by first getting the number of equal pixels between the ground truth and the predicted image, called intersection. Then, it gets the sum of the prediction and the ground truth, called union, to then compute dice_coefficient = 2*intersection/union. The dice loss is then, 1-dice_coefficient.
The actual loss of training the model also uses the binary-cross-entropy-loss.


The loss function looks like this:    `0.5 bce_loss + 0.5 dice_loss`
We save the model with the highest `dice_coefficient` from the validation set.


For training, we select all the samples with pixels contained in a lake polygon, and randomly select an equal number of samples in other regions. We divide these two sets into 80% for training, and 20% for testing.


The training was performed using one Nvidia A100 GPU (40GP) on Google Colabrotary.
The selected model has dice_coefficient = 0.82, obtained at epoch 243.


# Predictions
This part is performed in the file `Tile+predict.ipynb`


To make predictions for the test data, first we apply the same tiling and normalization to the test rasters as the training data. Then, we pass those tiles to the UNet model, and use 0.1 as the threshold to divide the pixels between 0 and 1, with one being the pixel where a lake exists. After that, we regenerate the original raster image, by adding each tile to its position. Then, we store a single TIFF file with the same shape,transform, and crs as the input file. This is then used in the next stage to extract the shapes, and store the final GeoPackage output.


# Extracting shapes


This part is performed in the file `Tile+predict.ipynb`


Given the predicted raster, we apply several steps to extract the shapes, and store them in the final GeoPackage file.


First, we use the shape extraction function from the Python package rasterio.



`rasterio.features.shapes`



This function extracts shapes based on pixel connectivity, if at least 8 pixels are connected they are extracted as a shape.


Then, we iterate through the shapes and apply some filters. First, we get the convex hull of the shape. Then, we remove any shapes with an area less than 100,000m^2. To remove narrow shapes, we used an approximation. First, we compute the maximum diagonal by first computing the minimum bounding rectangle. Simply using this function:

```
MultiPoint(polygon.exterior.coords).minimum_rotated_rectangle
```


We get the length of this rectangle as the maximum diagonal of the shape. Then, we compute the buffer of the shape with this distance -0.085*max_diagonal, which applied as follows:


```
shapely.buffer(polygon, -0.085*max_diagonal)
```

This way shapes with a narrow width will have zero area after applying the buffer, and we filter them out. We tried a few factors of the max_diagonal like 0.1, 0.09, 0.085, and 0.08. We found that 0.085 seems to be the best option.


After these filters, we apply a merge step. We add a 120 meters buffer to all the shapes, and merge the polygons that intersect after the buffer. Then, we get the convex hull for the resulting union polygon. This part is simply performed using these two lines for each image:


```
gdf['geometry'] = gdf['geometry'].buffer(120)
gdf = gdf.dissolve().explode(index_parts=True)
```

Then, we iterate the geometries in this dataframe and store the convex hull in the GeoPackage output file.


We further evaluated this output manually to check that the output looked reasonable enough.
