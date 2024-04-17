# -*- coding: utf-8 -*-
"""
Generated by ArcGIS ModelBuilder on : 2024-04-17 17:12:36
"""
import arcpy
from sys import argv

#For inline variable substitution, parameters passed as a String are evaluated using locals(), globals() and isinstance(). To override, substitute values directly.
def Model2(Input_Roço, Output):  # Calculadora de roço 2

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    arcpy.ImportToolbox(r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\Data Management Tools.tbx")

    # Process: Select Layer By Attribute (Select Layer By Attribute) (management)
    ROCO_VAO_REALIZAR_06042022, Count = arcpy.management.SelectLayerByAttribute(in_layer_or_view=Input_Roço.__str__().format(**locals(),**globals())if isinstance(Input_Roço, str) else Input_Roço, where_clause="check_levantamento = '1'")

    # Process: Feature To Line (Feature To Line) (management)
    Output_Feature_Class = "C:\\AppData\\Local\\Temp\\ArcGISProTemp5636\\e16d612f-8c75-4dca-a6f5-5f19d1512764\\Default.gdb\\ROCO_VAO_REALIZAR_06042022_F1"
    arcpy.management.FeatureToLine(in_features=[ROCO_VAO_REALIZAR_06042022], out_feature_class=Output_Feature_Class)

    # Process: Split Line At Vertices (Split Line At Vertices) (management)
    arcpy.management.SplitLine(in_features=Output_Feature_Class, out_feature_class=Output.__str__().format(**locals(),**globals())if isinstance(Output, str) else Output)

    # Process: Calculate Geometry Attributes (Calculate Geometry Attributes) (management)
    ROCO_VAO_REALIZAR_06042022_F2 = arcpy.management.CalculateGeometryAttributes(in_features=Output.__str__().format(**locals(),**globals())if isinstance(Output, str) else Output, geometry_property=[["comp_metros", "LENGTH_GEODESIC"]], length_unit="METERS", coordinate_system="GEOGCS[\"GCS_SIRGAS_2000\",DATUM[\"D_SIRGAS_2000\",SPHEROID[\"GRS_1980\",6378137.0,298.257222101]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]")[0]

    # Process: Delete Field (Delete Field) (management)
    OutputFinal = arcpy.management.DeleteField(in_table=ROCO_VAO_REALIZAR_06042022_F2, drop_field=["FID_ROCO_VAO_REALIZAR_06042022", "dt_confirmacao", "check_levantamento", "check_realizacao", "nu_ordem_conf", "area_albers", "st_obs", "nm_gregional", "ds_tipo_roco", "id_responsavel", "dt_levantamento", "nu_ordem_lev", "created_user", "created_date", "last_edited_user", "last_edited_date", "long_centroide", "lat_centroide", "horainicio", "uf", "municipio", "insplimp", "agente", "id_agente", "nom_lt", "id_equipamento", "vao", "obs_a", "obs1", "tipolimpeza", "motivo_nao_realizada", "obs_b", "obs2", "aerolevantamento", "num_foto", "num_foto_aerolevantamento", "latitude_aerolevantamento", "longitude_aerolevantamento", "altitude_aerolevantamento", "horatermino", "num_mes", "ano", "note1", "note2", "note3", "avaliacao", "note4", "note7", "image1_count", "image4_count", "globalid", "creationdate", "creator", "editdate", "editor", "realizacao", "ORIG_FID", "ORIG_SEQ"])[0]

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace="C:\\Users\\anderson.souza\\Documents\\ArcGIS\\Projects\\MyProject20\\MyProject20.gdb", workspace="C:\\Users\\anderson.souza\\Documents\\ArcGIS\\Projects\\MyProject20\\MyProject20.gdb"):
        Model2(*argv[1:])
