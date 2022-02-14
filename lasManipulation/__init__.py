#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
lasManipulastions/__init__.py: This module has been build to have an standard API to connect with .LAS files
"""
__author__          = "Robert Rijnbeek"
__version__         = "1.0.1"
__maintainer__      = "Robert Rijnbeek"
__email__           = "robert270384@gmail.com"
__status__          = "Development"

__creation_date__   = '14/02/2022'
__last_update__     = '14/02/2022'

# =============== Imports ===============

import pylas
import numpy as np

from pathlib import Path
from math import sqrt

from OCC.Core.Graphic3d import Graphic3d_ArrayOfPoints, Graphic3d_AspectMarker3d
from OCC.Core.AIS import AIS_PointCloud
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB 
from OCC.Core.gp import gp_Pnt
from OCC.Core.Aspect import Aspect_TOM_O_POINT

from OCC.Display.SimpleGui import init_display

class LASManipulations:
    def __init__(self,LAS_FILE):
        """
        CONSTRUCTOR FUNCTION
        """
        self.file=LAS_FILE

        self.pointcount=self.GetPointCount()
        self.format=self.GetLasFormat()
        self.argumen_list=self.GetArgumentNameList()

        self.x=self.GetXList()
        self.y=self.GetYList()
        self.z=self.GetZList()

        self.index=self.GetIndexList()

# ===== I N I T     F U N C T I O N S ======

    def GetPointCount(self):
        try:
            return self.file.header.point_count
        except:
            print("Las file has wrong data format")
            return False

    def GetLasFormat(self):
        try:
            return self.file.points_data.point_format.id
        except:
            print("Las file has wrong data format")
            return False

    def GetArgumentNameList(self):
        try:
            return self.file.points_data.point_format.dimension_names
        except:
            print("Las file has wrong data format")
            return False

    def GetXList(self):
        try:
            return self.file.x
        except:
            print("Las file has wrong data format")
            return False

    def GetYList(self):
        try:
            return self.file.y
        except:
            print("Las file has wrong data format")
            return False
    
    def GetZList(self):
        try:
            return self.file.z
        except:
            print("Las file has wrong data format")
            return False

    def GetIndexList(self):
        try:
            return np.arange(0,self.pointcount,1)
        except:
            print("Las file has wrong data format")
            return False


# ===== G E T    F U N C T I O N S =======

    def GetPointInformationByName(self,NAME):
        try:
            return self.file[NAME]
        except:
            print("Las file has no '" + str(NAME) + "' datapoint angument")
            return False

# ===== D A T A    M A N I P U L A T I O N S =========


    def CreateBasicMatrix(self):
        return np.transpose([self.x,self.y,self.z])

    def CreateMatrizByArrayList(self,ARRAY):
        if isinstance(ARRAY, list):
            return np.transpose(ARRAY)
        else:
            print("Argument is not a list")
            return False
    
# ===== G E T    C O N T O U R S ======
    
    def GetMaxValues(self,LAS=None):
        if LAS==None:
            LAS=self.file
        try:
            return LAS.header.maxs
        except:
            return [max(LAS.x),max(LAS.y),max(LAS.z)]
    
    def GetMinValues(self,LAS=None):
        if LAS==None:
            LAS=self.file
        try:
            return LAS.header.mins
        except:
            return [min(LAS.x),min(LAS.y),min(LAS.z)]


# ====== F I L T E R    U T I L I T I E S =======

    def GenericLasFilter(self,LAS=None,BOOLEAN_FUNCTION=True):
        '''
        example boolean function: (pr.file["red"] == 51456) & (pr.file["green"] == 51456)
        '''
        try:
            if LAS==None:
                LAS=self.file
            return LAS.points[BOOLEAN_FUNCTION]
        except:
            print("problems with boolean function")
            return False
    
    def LasFilterByColor(self,RGB_Array,LAS=None,Desviation=0):
        try:
            if LAS==None:
                LAS=self.file
            R=RGB_Array[0]
            G=RGB_Array[1]
            B=RGB_Array[2]     
            BOOLEAN_FUNCTION=(np.sqrt((np.power(R-LAS["red"],2)+np.power(G-LAS["green"],2)+np.power(B-LAS["blue"],2))*0.5)<=Desviation)
            return self.GenericLasFilter(LAS=LAS,BOOLEAN_FUNCTION=BOOLEAN_FUNCTION)
        except:
            print("problems with boolean function")
            return False

    def LasFilterByXYZBOX(self,XYZBOX,LAS=None):
        """
        XYZBOX exaple [[Xmin,Xmax],[Ymin,Ymax],[Zmin,Zmax]] ==> [[721864663,741864663],[598353715,618353715],[141969560,171969560]]
        """
        if LAS==None:
            LAS=self.file
        [[X_min,X_max],[Y_min,Y_max],[Z_min,Z_max]] = XYZBOX
        BOOLEAN_FUNCTION=np.logical_and(
                            np.logical_and(
                                np.logical_and(X_min <= LAS["X"] ,X_max >= LAS["X"]),
                                np.logical_and(Y_min <= LAS["Y"] ,Y_max >= LAS["Y"])),
                                np.logical_and(Z_min <= LAS["Z"] ,Z_max >= LAS["Z"]))
        return self.GenericLasFilter(LAS=LAS,BOOLEAN_FUNCTION=BOOLEAN_FUNCTION)
        

# ===== W R I T E    L A S ======

    def LasWrite(self, PATH, LAS=None):
        """
        """
        try:
            if LAS==None:
                LAS=self.file
            if Path(PATH).parent.is_dir():
                LAS.write(PATH)
                return True
            else:
                print("Directory do not exists")
                return False
        except:
            print("Error writing las file")
            return False

# ===== C R E A T E    L A S ======

    def LasCreate(self,point_format_id=None,file_version=None):
        """
        EXAMPLE = LasCreate(point_format_id=las.header.point_format_id, file_version=las.header.version)
        EXAMPLE = LasCreate(point_format_id=las.header.point_format_id)
        EXAMPLE = LasCreate()
        """
        try:
            if point_format_id == None:
                return pylas.create()
            elif  file_version == None:
                return pylas.create(point_format_id=point_format_id)
            else:
                return pylas.create(point_format_id=point_format_id,file_version=file_version)
        except:
            print("Error creating las file")
            return False

    def LasCreateByHeader(self,HEADER):
        """
        EXAMPLE = LasCreateByHeader(las.header)
        """
        try:
            return pylas.create_from_header(HEADER)
        except:
            print("Error creating las file")
            return False


# ==== L A S   D A T A    M A N I P U L T I O N =======

    def PutNewDataToLas(self, ARGUMENT_NAME,ARGUMENT_DATA, LAS = None):
        try:
            if LAS==None:
                LAS = self.file
            LAS[ARGUMENT_NAME]=ARGUMENT_DATA
            return True
        except:
            print("Error putting new data in las file")
            return False

    def PutXDataToLas(self,DATA,LAS = None):
        try:
            if LAS==None:
                LAS = self.file
            LAS.x=DATA
            return True
        except:
            print("Error putting new data in las file")
            return False
    
    def PutYDataToLas(self,DATA,LAS = None):
        try:
            if LAS==None:
                LAS = self.file
            LAS.y=DATA
            return True
        except:
            print("Error putting new data in las file")
            return False
    
    
    def PutZDataToLas(self,DATA,LAS = None):
        try:
            if LAS==None:
                LAS = self.file
            LAS.z=DATA
            return True
        except:
            print("Error putting new data in las file")
            return False

# ====== E X T R A   D I M E N S I O N S =======

    """
    pylas name	    size (bits)	    type
    u1 or uint8	    8	            unsigned
    i1 or int8	    8	            signed
    u2 or uint16	16	            unsigned
    i2 or int16	    16	            signed
    u4 or uint32	32	            unsigned
    i4 or int32	    32	            signed
    u8 or uint64	64	            unsigned
    i8 or int64	    64	            signed
    f4 or float	    32	            floating
    f8 or double	64	            floating
    """

    def PutExtraDimensionsToLas(self,NAME, TYPE, LAS = None, DESCRIPTION=None ):
        try:
            if LAS==None:
                    LAS = self.file
            if DESCRIPTION == None :
                LAS.add_extra_dim(name=NAME, type=TYPE)
                return True
            else:
                LAS.add_extra_dim(name=NAME, type=TYPE,description=DESCRIPTION)
                return True
        except:
            print("Problem with putting extra dimensions")
            return False

class LAS_Viewer(LASManipulations):
    def __init__(self,LAS_FILE):
        LASManipulations.__init__(self,LAS_FILE)

    def DisplayLAS(self, COLOR_TYPE = "RGB"):
        display, start_display, add_menu, add_function_to_menu = init_display()
        
        x_list=self.x
        y_list=self.y
        z_list=self.z
        lenght=len(x_list)
        argument_list=self.argumen_list
        if ("red" in argument_list) and ("green" in argument_list) and ("blue" in argument_list) and (COLOR_TYPE == "RGB") :
            points_3d = Graphic3d_ArrayOfPoints(lenght,True)
            red_list=(self.file["red"]/(65536))
            green_list=(self.file["green"]/(65536))
            blue_list=(self.file["blue"]/(65536))
            mat=np.transpose([x_list,y_list,z_list,red_list,green_list,blue_list])
            for x,y,z,r,g,b in mat:
                color = Quantity_Color(r, g, b, Quantity_TOC_RGB)
                points_3d.AddVertex(gp_Pnt(x, y, z),color)
        else:
            points_3d = Graphic3d_ArrayOfPoints(lenght)
            mat=np.transpose([x_list,y_list,z_list])
            for x,y,z in mat:
                points_3d.AddVertex(x, y, z)
        point_cloud = AIS_PointCloud()
        asp =  Graphic3d_AspectMarker3d(Aspect_TOM_O_POINT,Quantity_Color(0,1,1, Quantity_TOC_RGB),1)
        #point_cloud.SetAspect(asp)
        #point_cloud.SetAspect
        #point_cloud.SetAspect(asp)
        point_cloud.SetPoints(points_3d)
        # display
        
        if COLOR_TYPE is not "RGB":
            if isinstance(COLOR_TYPE,list):
                if len(COLOR_TYPE)==4 and max(COLOR_TYPE) <= 1 and min(COLOR_TYPE) >= 0:
                    point_cloud.SetColor(Quantity_Color(COLOR_TYPE[0],COLOR_TYPE[1],COLOR_TYPE[2], Quantity_TOC_RGB))
        ais_context = display.GetContext()
        ais_context.Display(point_cloud,True)
        display.DisableAntiAliasing()
        display.View_Iso()
        display.FitAll()

        start_display()


if __name__ == '__main__':
    pass