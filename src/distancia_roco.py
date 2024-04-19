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
        
1- Seleção de Camadas por Localização:
Utiliza a ferramenta "Select Layer By Location" para selecionar features de uma camada
 (Input_Vãos_de_linhas) com base na sua relação espacial com outra camada 
(Input_Roço_de_Vão) a uma distância de 10 metros.

2- Exclusão de Áreas de Interseção:
Utiliza a ferramenta "Erase" para remover áreas de interseção entre os vãos de transmissão
 (vaodelinhasdetransmissao) e as áreas de roçado (Input_Roço_de_Vão).

3- Conversão de Multipartes para Singlepartes:
Utiliza a ferramenta "Multipart To Singlepart" para converter as feições multipartidas 
resultantes da operação anterior em feições singlepartidas.

4- Cálculo de Atributos de Geometria:
Utiliza a ferramenta "Calculate Geometry Attributes" para calcular o comprimento geodésico
 das feições resultantes e armazená-lo no campo comp_metros.

5- Exclusão de Campos Desnecessários:
Utiliza a ferramenta "Delete Field" para excluir campos desnecessários das feições resultantes.
'''

class CalculoDistanciaRoco:
    def __init__(self, vaos_de_linha, roco_de_vao, output):
        self.vaos_de_linha = vaos_de_linha
        self.roco_de_vao = roco_de_vao
        self.output = output

    def select_layer_by_location(self):
        layer = mn.MakeFeatureLayer(in_features=self.vaos_de_linha,
                                    out_layer="lyr",
                                    )
        vao_de_linha = mn.SelectLayerByLocation(in_layer=layer,
                                                 overlap_type="INTERSECT",
                                                 select_features=self.roco_de_vao,
                                                 selection_type="NEW_SELECTION"
                                                 )
        return vao_de_linha

    def erase(self, selected_layer):
        erased_layer = an.Erase(in_features=selected_layer,
                                erase_features=self.roco_de_vao,
                                out_feature_class="in_memory//erased_layer"
                                )
        return erased_layer

    def explode(self, erased_layer):
        exploded_layer = cs.MultipartToSinglepart(in_features=erased_layer,
                                                   out_feature_class="in_memory//exploded_layer"
                                                   )
        return exploded_layer

    def calculate_geometry_attributes(self, exploded_layer):
        calculated_layer = mn.CalculateGeometryAttributes(in_features=exploded_layer,
                                                          geometry_property=[["LENGTH_GEODESIC", "comp_metros"]],
                                                          length_unit="METERS"
                                                          )
        return calculated_layer

    def delete_field(self, calculated_layer):
        fields_to_keep = []
        clear_layer = mn.DeleteField(in_table=calculated_layer,
                                     drop_field=fields_to_keep,
                                     method="KEEP_FIELDS")
        return clear_layer

    def copy_features(self, clear_layer):
        copy_features = mn.CopyFeatures(in_features=clear_layer,
                                        out_feature_class=self.output
                                        )
        return copy_features

    def row_count(self, fc):
        result = mn.GetCount(fc)
        count = int(result)
        return count

    def run(self):
        previous_row_count = self.row_count(self.output)

        selected_layer = self.select_layer_by_location()
        erased_layer = self.erase(selected_layer)
        exploded_layer = self.explode(erased_layer)
        calculated_layer = self.calculate_geometry_attributes(exploded_layer)
        clear_layer = self.delete_field(calculated_layer)
        self.copy_features(clear_layer)
        status = 'A execução ocorreu normalmente' if self.copy_features(clear_layer) else 'Houve erro na execução'
        current_row_count = self.row_count(self.output)
        current_time = datetime.datetime.now()
        return {
            'title':'Calculo de Distância entre Roço e Torre',
            'text': 'Processo finalizado!',
            'status': status,
            'horario': current_time,
            'previous_row_count': previous_row_count,
            'current_row_count': current_row_count,
        }
