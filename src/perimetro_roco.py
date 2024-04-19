import os
import arcpy
import arcpy.management as mn
import arcpy.analysis as an
import arcpy.conversion as cs
import datetime
arcpy.env.overwriteOutput = True
'''
████████╗ █████╗ ███████╗███████╗ █████╗ 
╚══██╔══╝██╔══██╗██╔════╝██╔════╝██╔══██╗
   ██║   ███████║█████╗  ███████╗███████║
   ██║   ██╔══██║██╔══╝  ╚════██║██╔══██║
   ██║   ██║  ██║███████╗███████║██║  ██║
   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝
        
1- Seleção por atributo (SelectLayerByAttribute):
Seleciona feições (ou elementos) do mapa baseadas em uma expressão de consulta. 
Aqui, a seleção é feita onde a coluna check_levantamento é igual a '1'

2- Conversão de feições em linhas (FeatureToLine):
Converte feições (neste caso, polígonos) em linhas.

3- Divisão de linhas em vértices (SplitLineAtVertices):
Divide as linhas em seus vértices

4- Cálculo de atributos de geometria (CalculateGeometryAttributes):
Calcula as propriedades geométricas das linhas resultantes, neste caso, o comprimento geodésico em metros

5- Exclusão de campos (DeleteField): 
Remove campos específicos do conjunto de dados resultante. Esses campos são listados explicitamente na função DeleteField.
'''

class CalculoPerimetroRoco:
    def __init__(self, roco_de_vao, output):
        self.roco_de_vao = roco_de_vao
        self.output = output

    def select_layer_by_attribute(self):
        layer = mn.MakeFeatureLayer(in_features=self.roco_de_vao,
                                    out_layer="lyr",
                                    )
        vao_de_linha = mn.SelectLayerByAttribute(in_layer=layer,
                                                 where_clause="check_levantamento = '1'",
                                                 selection_type="NEW_SELECTION"
                                                 )
        return vao_de_linha

    def feature_to_line(self, selected_layer):
        feature_to_line = mn.FeatureToLine(in_features=selected_layer,
                                            out_feature_class="in_memory//roco_de_vao"
                                            )
        return feature_to_line

    def split_line_at_vertices(self, feature_to_line):
        split_line = mn.SplitLine(in_features=feature_to_line,
                                   out_feature_class="in_memory//split_line"
                                   )
        return split_line

    def calculate_geometry_attributes(self, split_line):
        calculate_geometry = mn.CalculateGeometryAttributes(in_features=split_line,
                                                            geometry_property=[["comp_metros", "LENGTH_GEODESIC"]],
                                                            length_unit="METERS"
                                                            )
        return calculate_geometry

    def delete_field(self, calculate_geometry):
        fields_to_keep = []
        delete_field = mn.DeleteField(in_table=calculate_geometry,
                                      drop_field=fields_to_keep,
                                      method="KEEP_FIELDS"
                                      )
        return delete_field

    def copy_features(self, clear_layer):
        copy_features = mn.CopyFeatures(in_features=clear_layer,
                                         out_feature_class=self.output
                                         )
        return copy_features

    def row_count(self, fc):
        result = arcpy.GetCount_management(fc)
        count = int(result.getOutput(0))
        return count

    def run(self):
        previous_row_count = self.row_count(self.output)

        selected_layer = self.select_layer_by_attribute()
        feature_to_line = self.feature_to_line(selected_layer)
        split_line = self.split_line_at_vertices(feature_to_line)
        calculate_geometry = self.calculate_geometry_attributes(split_line)
        clear_layer = self.delete_field(calculate_geometry)
        self.copy_features(clear_layer)
        status = 'A execução ocorreu normalmente' if self.copy_features(clear_layer) else 'Houve erro na execução'
        current_row_count = self.row_count(self.output)
        current_time = datetime.datetime.now()
        return {
            'title':'Calculo de Perimetro da Área do Roço',
            'text': 'Processo finalizado!',
            'status': status,
            'time': current_time,
            'previous_row_count': previous_row_count,
            'current_row_count': current_row_count,
        }
