#!/bin/bash -l

mkdir train_labels/region_01
mkdir train_labels/region_02
mkdir train_labels/region_03
mkdir train_labels/region_04
mkdir train_labels/region_05
mkdir train_labels/region_06

#region1
gdal_translate -projwin -5581347.0500051118433475 10875536.2075952738523483 -5081544.3222225857898593 10541779.7202169168740511 -of GTiff train_labels/Greenland26X_22W_Sentinel2_2019-06-19_20.tif train_labels/region_01/Greenland26X_22W_Sentinel2_2019-06-19_20.tif 

gdal_translate -projwin -5581347.0500051118433475 10875536.2075952738523483 -5081544.3222225857898593 10541779.7202169168740511 -of GTiff train_labels/Greenland26X_22W_Sentinel2_2019-08-25_29.tif train_labels/region_01/Greenland26X_22W_Sentinel2_2019-08-25_29.tif 

#region2
gdal_translate -projwin -5677913.2319217920303345 10555665.3549526613205671 -5106320.0163595946505666 10222803.1109571196138859 -of GTiff train_labels/Greenland26X_22W_Sentinel2_2019-06-03_05.tif train_labels/region_02/Greenland26X_22W_Sentinel2_2019-06-03_05.tif 

gdal_translate -projwin -5677913.2319217920303345 10555665.3549526613205671 -5106320.0163595946505666 10222803.1109571196138859 -of GTiff train_labels/Greenland26X_22W_Sentinel2_2019-07-31_25.tif train_labels/region_02/Greenland26X_22W_Sentinel2_2019-07-31_25.tif 

#region3
gdal_translate -projwin -5678009.2035128036513925 10252908.4107158817350864 -5127153.8705513142049313 9881350.7315969727933407 -of GTiff train_labels/Greenland26X_22W_Sentinel2_2019-06-19_20.tif train_labels/region_03/Greenland26X_22W_Sentinel2_2019-06-19_20.tif 

gdal_translate -projwin -5678009.2035128036513925 10252908.4107158817350864 -5127153.8705513142049313 9881350.7315969727933407 -of GTiff train_labels/Greenland26X_22W_Sentinel2_2019-08-25_29.tif train_labels/region_03/Greenland26X_22W_Sentinel2_2019-08-25_29.tif 

#region4
gdal_translate -projwin -5678009.2035128036513925 9943627.6213879678398371 -5161180.8945540199056268 9547815.3777213450521231 -of GTiff train_labels/Greenland26X_22W_Sentinel2_2019-06-03_05.tif train_labels/region_04/Greenland26X_22W_Sentinel2_2019-06-03_05.tif 

gdal_translate -projwin -5678009.2035128036513925 9943627.6213879678398371 -5161180.8945540199056268 9547815.3777213450521231 -of GTiff train_labels/Greenland26X_22W_Sentinel2_2019-07-31_25.tif train_labels/region_04/Greenland26X_22W_Sentinel2_2019-07-31_25.tif 

#region5
gdal_translate -projwin -3559211.9268645676784217 15646302.1948013808578253 -2366209.8097618930041790 14721683.2670614980161190 -of GTiff train_labels/Greenland26X_22W_Sentinel2_2019-06-19_20.tif train_labels/region_05/Greenland26X_22W_Sentinel2_2019-06-19_20.tif 

gdal_translate -projwin -3559211.9268645676784217 15646302.1948013808578253 -2366209.8097618930041790 14721683.2670614980161190 -of GTiff train_labels/Greenland26X_22W_Sentinel2_2019-08-25_29.tif train_labels/region_05/Greenland26X_22W_Sentinel2_2019-08-25_29.tif 

#region6
gdal_translate -projwin -3526251.9756653276272118 14894948.0426320526748896 -2447189.6939366068691015 14029708.3617717232555151 -of GTiff train_labels/Greenland26X_22W_Sentinel2_2019-06-03_05.tif train_labels/region_06/Greenland26X_22W_Sentinel2_2019-06-03_05.tif 

gdal_translate -projwin -3526251.9756653276272118 14894948.0426320526748896 -2447189.6939366068691015 14029708.3617717232555151 -of GTiff train_labels/Greenland26X_22W_Sentinel2_2019-07-31_25.tif train_labels/region_06/Greenland26X_22W_Sentinel2_2019-07-31_25.tif 