# -*- coding: utf-8 -*-
"""
Generated by ArcGIS ModelBuilder on : 2024-04-17 17:11:10
"""
import arcpy
from sys import argv

#For inline variable substitution, parameters passed as a String are evaluated using locals(), globals() and isinstance(). To override, substitute values directly.
def Model1(Input_Vãos_de_linhas, Input_Roço_de_Vão, Output):  # Cálculadora de comprimento entre vão e roço

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    arcpy.ImportToolbox(r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\Data Management Tools.tbx")

    # Process: Select Layer By Location (Select Layer By Location) (management)
    vaodelinhasdetransmissao, Output_Layer_Names, Count = arcpy.management.SelectLayerByLocation(in_layer=[Input_Vãos_de_linhas], select_features=Input_Roço_de_Vão.__str__().format(**locals(),**globals())if isinstance(Input_Roço_de_Vão, str) else Input_Roço_de_Vão, search_distance="10 Meters")

    # Process: Erase (Erase) (analysis)
    vaos_lt_Erase = "C:\\AppData\\Local\\Temp\\ArcGISProTemp11676\\a7dd7d46-2d6e-489d-8483-1d4fe19a5a29\\Default.gdb\\vaodelinhasdetransmissao_Era"
    arcpy.analysis.Erase(in_features=vaodelinhasdetransmissao, erase_features=Input_Roço_de_Vão.__str__().format(**locals(),**globals())if isinstance(Input_Roço_de_Vão, str) else Input_Roço_de_Vão, out_feature_class=vaos_lt_Erase)

    # Process: Multipart To Singlepart (Multipart To Singlepart) (management)
    arcpy.management.MultipartToSinglepart(in_features=vaos_lt_Erase, out_feature_class=Output.__str__().format(**locals(),**globals())if isinstance(Output, str) else Output)

    # Process: Calculate Geometry Attributes (2) (Calculate Geometry Attributes) (management)
    Updated_Features = arcpy.management.CalculateGeometryAttributes(in_features=Output.__str__().format(**locals(),**globals())if isinstance(Output, str) else Output, geometry_property=[["comp_metros", "LENGTH_GEODESIC"]], length_unit="METERS", coordinate_system="GEOGCS[\"GCS_SIRGAS_2000\",DATUM[\"D_SIRGAS_2000\",SPHEROID[\"GRS_1980\",6378137.0,298.257222101]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]")[0]

    # Process: Delete Field (Delete Field) (management)
    vaos_lt_Erase_MultipartToSin_2_ = arcpy.management.DeleteField(in_table=Updated_Features, drop_field=["ORIG_FID", "comprimento", "coord_x", "coord_y", "created_date", "created_user", "id_pm_concessao", "vl_potencia", "sg_concessao", "vl_corrente_curta_duracao", "vl_corrente_longa_duracao", "vl_classe_tensao", "last_edited_user", "last_edited_date", "comprimentovlt", "r1", "r4", "r7", "r8", "r10", "r12", "r13", "r14", "idbdit", "idbdittf", "idbdittt", "idbditlt", "created_user", "created_date", "vl_tensao_nominal"])[0]

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace="C:\\Users\\anderson.souza\\Documents\\ArcGIS\\Projects\\MyProject20\\MyProject20.gdb", workspace="C:\\Users\\anderson.souza\\Documents\\ArcGIS\\Projects\\MyProject20\\MyProject20.gdb"):
        Model1(*argv[1:])
