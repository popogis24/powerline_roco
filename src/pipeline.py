import arcpy


arcpy.env.overwriteOutput = False
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
Conversão de Multipartes para Singlepartes:

3- Conversão de Multipartes para Singlepartes:
Utiliza a ferramenta "Multipart To Singlepart" para converter as feições multipartidas 
resultantes da operação anterior em feições singlepartidas.
Cálculo de Atributos de Geometria:

4- Cálculo de Atributos de Geometria:
Utiliza a ferramenta "Calculate Geometry Attributes" para calcular o comprimento geodésico
 das feições resultantes e armazená-lo no campo comp_metros.

5- Exclusão de Campos Desnecessários:
Utiliza a ferramenta "Delete Field" para excluir campos desnecessários das feições resultantes.
'''