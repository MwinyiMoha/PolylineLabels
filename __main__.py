#-------------------------------------------------------------------------------
# Name:        Polyline Labels
# Purpose:     Generate CAD labels for polylines
# Author:      Mohammed Mwijaa
# Created:     16/06/2017
# Copyright:   (c) Moha 2017
# Status:      <Draft>
#-------------------------------------------------------------------------------
import sys
import os
import time
import re
from geopandas import GeoDataFrame
from dxfwrite import DXFEngine as dxf
from Shapely.Geometry import Polyline

class PolylineLabels:
    def __init__(self):
        self.polylineFeatures=''
        self.polylineCAD=''

    def dataConfig(self):
        print('Configuring Data Paths...')

        data_path=os.path.join(os.path.dirname(__file__), 'Data')
        if not os.path.exists(data_path):
            os.mkdir(data_path)
            print('Please Copy Polyline Feature Class To: {}'.format(os.path.abspath(data_path)))
            print('Tool Will Exit In Five Seconds')
            time.sleep(5)
            exit()

        self.polylineFeatures=os.path.join(data_path, sys.argv[1]+'.shp')
        if not os.path.exists(self.polylineFeatures):
            raise ValueError('Polyline Feature Class Not Found')
        self.polylineCAD=os.path.join(data_path, '{}_CAD.dxf'.format(sys.argv[1]))
        if os.path.exists(self.polylineCAD):
            os.remove(self.polylineCAD)


    def writeCAD(self, value, geometry):
        polyline=Polyline(geometry)

        #INCLUDE CODE TO PREVENT ADDING LAYERS EVERYTIME THE FUNCTION IS CALLED

        drawing = dxf.drawing(self.polylineCAD)
        drawing.add_layer('POLYLINES', color=2)
        drawing.add_layer('LABELS', color=2)
        drawing.add(dxf.line((0, 0), (10, 0), layer='POLYLINES'))
        drawing.add(dxf.text(value, insert=(polyline.centroid), layer='LABELS'))
        drawing.save()


    def getData(self):
        print('Reading Polyline Feature Class...')

        with GeoDataFrame.from_file(self.polylineFeatures) as gdf:
            gdf=gdf[sys.argv[2], geom]
            match=re.search('UTM', str(gdf.crs))
            if not match==None:
                for feature in gdf:
                    writeCAD(feature[1], feature[2])
            else:
                print('Please Use Feature Class With A Projected Coordinate Reference System')
                raise ValueError('Unsupported CRS!')


def main():
    Labels=PolylineLabels()
    Labels.dataConfig()
    Labels.getData()

if __name__ == '__main__':
    if len(sys.argv)==3:
        main()
    else:
        print('Run Tool As: python PolylineLabels [Polyline Feature Class]')
        print('Please Provide Polyline Feature Class ')
        raise ValueError('Incorrect Parameters')
