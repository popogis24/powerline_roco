import os
import arcpy
import arcpy.management as mn
import arcpy.analysis as an
import arcpy.conversion as cs
import datetime
from processors.proc_abs import Processor

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

class CalculoPerimetroRoco(Processor):
    def __init__(self, roco_de_vao, output):
        self.roco_de_vao = roco_de_vao
        self.output = output

    def select_layer_by_attribute(self):
        layer = mn.MakeFeatureLayer(in_features=self.roco_de_vao,
                                    out_layer="lyr",
                                    )
        roco_de_vao = mn.SelectLayerByAttribute(in_layer_or_view=layer,
                                                 where_clause="check_levantamento = '1'",
                                                 selection_type="NEW_SELECTION")
        return roco_de_vao

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
        mn.AddField(in_table=split_line,
            field_name="comp_metros",
            field_type="DOUBLE",
            field_alias="Comprimento (m)"
            )
        calculate_geometry = mn.CalculateGeometryAttributes(in_features=split_line,
                                                            geometry_property=[["comp_metros", "LENGTH_GEODESIC"]],
                                                            length_unit="METERS"
                                                            )
        return calculate_geometry

    def delete_field(self, calculate_geometry):
        fields_to_keep = ['ds_linha_transmissao','est_extrem','comp_metros','created_user','created_date','last_edited_user','last_edited_date']
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
        try:
            previous_row_count = self.row_count(self.output)
            selected_layer = self.select_layer_by_attribute()
            feature_to_line = self.feature_to_line(selected_layer)
            split_line = self.split_line_at_vertices(feature_to_line)
            calculate_geometry = self.calculate_geometry_attributes(split_line)
            self.delete_field(calculate_geometry)
            status = 'A execução ocorreu normalmente' if self.copy_features(split_line) else 'Houve erro na execução'
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
        except:
            return {
                'title':'Calculo de Perimetro da Área do Roço',
                'text': 'Houve erro na execução',
                'status': 'Houve erro na execução',
                'time': datetime.datetime.now(),
                'previous_row_count': 0,
                'current_row_count': 0,
            }
