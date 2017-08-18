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
import fiona
from dxfwrite import DXFEngine as dxf

class PolylineLabels:
    def __init__(self):
        self.dataPath=''
        self.polylineFeatures=''
        self.polylineCAD=''
        self.labelFeatures=''


    def dataConfig(self):
        print('Configuring Data Paths...')

        data_path=os.path.join(os.path.dirname(__file__), 'Data')
        if not os.path.exists(data_path):
            os.mkdir(data_path)
            print('Please Copy Polyline Feature Class To: {}'.format(os.path.abspath(data_path)))
            print('Tool Will Exit In Five Seconds')
            time.sleep(5)
            exit()

        self.dataPath=data_path
        self.polylineFeatures=os.path.join(data_path, sys.argv[1])
        if not os.path.exists(self.polylineFeatures):
            raise ValueError('Polyline Feature Class Not Found')
        self.polylineCAD=os.path.join(data_path, '{}_CAD.dxf'.format(sys.argv[1][:-4]))
        if os.path.exists(self.polylineCAD):
            os.remove(self.polylineCAD)
        self.labelFeatures=os.path.join(data_path, '{}_Labels.shp'.format(sys.argv[1][:-4]))
        if os.path.exists(self.labelFeatures):
            os.remove(self.labelFeatures)



    def createPolylineCAD(self):
        print('Creating The Polyline CAD...')

        with fiona.drivers():
            with fiona.open(self.polylineFeatures) as src:
                pat='utm'
                pattern=re.compile(pat)
                hit=re.search(pattern, src.crs)
                if hit==None:
                    raise ValueError('Reproject Polyline Features To UTM')

            with dxfwrite.open(self.polylineCAD, 'w') as sink:
                for rec in src:
                    sink.write(rec)


    def createCentroidFeatures(self):
        print('Calculating Centroids...')




    def createLabelCAD(self):
        print('Creating The Labels CAD...')


def main():
    Labels=PolylineLabels()
    Labels.dataConfig()
    Labels.createPolylineCAD()
    Labels.createCentroidFeatures()
    Labels.createLabelCAD()

if __name__ == '__main__':
    if len(sys.argv)==2:
        main()
    else:
        print('Run Tool As: python PolylineLabels [Polyline Feature Class]')
        print('Please Provide Polyline Feature Class ')
        raise ValueError('Incorrect Parameters')
