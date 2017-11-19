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
import geopandas as gpd
from dxfwrite import DXFEngine as dxf
from shapely.geometry import LineString, mapping

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
            print('Output File Exists: Removing...')
            os.remove(self.polylineCAD)

    def writeCAD(self):
        print('Reading Polyline Feature Class...')

        drawing = dxf.drawing(self.polylineCAD)
        drawing.add_layer('POLYLINES', color=2)
        drawing.add_layer('LABELS', color=2)

        UTM=Proj(proj='utm', zone=int(args.UTM_Zone), ellps=args.Datum)
        #Code for reprojection in case features are in GCS

        df=gpd.read_file(self.polylineFeatures)
        for rec in df.iterfeatures():
            print('Writing Feature With ID: {}...'.format(rec['properties']['ID']))

            value, coords=rec['properties'][self.valueColumn], rec['geometry']['coordinates']
            centroid=mapping(LineString(coords).centroid)
            xy=centroid['coordinates']
            drawing.add(dxf.polyline(coords, layer='POLYLINES'))
            drawing.add(dxf.text(value, insert=xy, layer='LABELS'))
            #Code to control text size
            
            drawing.save()

        print('Script Completed')
        print('Output File: {}'.format(os.path.abspath(self.polylineCAD)))


def main():
    Labels=PolylineLabels()
    Labels.dataConfig()
    Labels.writeCAD()

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('Input_File', help='Feature Class Containing Polyline Features(Include File Extension)')
    parser.add_argument('Field_Name', help='Name Of Column Holding Values To Be Used As Labels')
    parser.add_argument('UTM_Zone', help='UTM Zone Where The Input File Lies')
    parser.add_argument('--Datum', default='WGS84', help='Datum For The Projection System')
    parser.add_argument('--Data_Folder', default='Data', help='Folder Containing Data Files')
    args=parser.parse_args()
    main()