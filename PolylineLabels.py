#-------------------------------------------------------------------------------
# Name:        Polyline Labels
# Purpose:     Generate CAD labels for polylines
# Author:      Mohammed Mwijaa
# Created:     16/06/2017
# Copyright:   (c) Moha 2017
# Status:      <Draft>
#-------------------------------------------------------------------------------
import sys


class PolylineLabels:
    def __init__():
        pass

    def dataConfig():
        pass

    def createPolylineCAD():
        pass

    def createCentroid():
        pass

    def createLabelCAD():
        pass


def main():
    Labels=PolylineLabels()
    Labels.dataConfig()
    Labels.createPolylineCAD()
    Labels.createCentroid()
    Labels.createLabelCAD()

if __name__ == '__main__':
    if len(sys.argv)==2:
        main()
    else:
        raise ValueError('Incorrect Parameters')
