#-------------------------------------------------------------------------------
# Name:        Polyline Labels
# Purpose:     Generate CAD labels for polylines
# Author:      Mohammed Mwijaa
# Created:     16/06/2017
# Copyright:   (c) Moha 2017
# Status:      <Draft>
#-------------------------------------------------------------------------------
import argparse
import os
import time
from pyproj import Proj
from geopandas import GeoDataFrame as gdf
from dxfwrite import DXFEngine as dxf
from Shapely.Geometry import LineString

class PolylineLabels:
    def __init__(self):
        self.dataPath=os.path.join(os.path.dirname(__file__), args.Data_Folder)
        self.polylineFeatures=os.path.join(self.dataPath, args.Input_File)
        self.polylineCAD=os.path.join(self.dataPath, args.Input_File.replace('shp', 'dxf'))
        self.valueColumn=args.Field_Name
        self.UTMZone=args.UTM_Zone

    def dataConfig(self):
        print('Validating Data Paths...')

        if not os.path.exists(self.dataPath):
            os.mkdir(self.dataPath)
            print('Please Copy Polyline Feature Class To: {}'.format(os.path.abspath(self.dataPath)))
            print('Tool Will Exit In Five Seconds')
            time.sleep(5)
            exit()
        if not os.path.exists(self.polylineFeatures):
            raise ValueError('Polyline Feature Class Not Found')
        if os.path.exists(self.polylineCAD):
            os.remove(self.polylineCAD)

    def writeCAD(self, fid, value, coords):
        print('Writing Feature With ID: {}...'.format(fid))

        drawing = dxf.drawing(self.polylineCAD)
        if fid==0:
            drawing.add_layer('POLYLINES', color=2)
            drawing.add_layer('LABELS', color=2)

        drawing.add(dxf.polyline(coords, layer='POLYLINES'))
        drawing.add(dxf.text(value, insert=LineString(coords).centroid, layer='LABELS'))
        drawing.save()

    def getData(self):
        print('Reading Polyline Feature Class...')

        UTM=Proj()
        with gdf.from_file(self.polylineFeatures) as df:
            df.to_crs(UTM)
            for rec in df.iterfeatures():
                fid, value, coords=rec['id'], rec['properties'][self.valueColumn], rec['geometry']['coordinates']
                writeCAD(fid, value, coords)

        print('Script Completed')
        print('Output File: {}'.format(os.path.abspath(self.polylineCAD)))

def main():
    Labels=PolylineLabels()
    Labels.dataConfig()
    Labels.getData()

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('Input_File', help='Feature Class Containing Polyline Features(Include File Extension)')
    parser.add_argument('Field_Name', help='Name Of Column Holding Values To Be Used As Labels')
    parser.add_argument('UTM_Zone', help='UTM Zone Where The Input File Lies')
    parser.add_argument('--Data_Folder', default='Data', help='Folder Containing Data Files')
    args=parser.parse_args()
    main()