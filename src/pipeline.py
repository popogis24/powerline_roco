import schedule
import time
from processors.proc_distance import CalculoDistanciaRoco
from processors.proc_perimeter import CalculoPerimetroRoco
from notificator import EmailNotification
from configs import Config
from database import Database
import arcpy.conversion as cs
import os
import arcpy

settings = Config()
print('Iniciando o programa...')
print('Aguarde...')
class Pipeline:
    def __init__(self, vao_de_linha, roco_de_vao, output_calc_distancia, output_calc_perimetro):
        self.vao_de_linha = vao_de_linha
        self.roco_de_vao = roco_de_vao
        self.output_calc_distancia = output_calc_distancia
        self.output_calc_perimetro = output_calc_perimetro
        self.exported_vao_de_linha = self.export_without_attach(self.vao_de_linha, 'vao_de_linha')
        self.exported_roco_de_vao = self.export_without_attach(self.roco_de_vao, 'roco_de_vao')
        self.Calc_Perimetro = CalculoPerimetroRoco(self.exported_roco_de_vao, self.output_calc_perimetro)
        self.Calc_Distancia = CalculoDistanciaRoco(self.exported_vao_de_linha, self.exported_roco_de_vao, self.output_calc_distancia)

    def export_without_attach(self, feature_class, name):
        arcpy.env.overwriteOutput = True
        diretorio = settings.ARCGIS["workspace"]
        filename = os.path.join(diretorio, name+"_noATTACH")
        with arcpy.EnvManager(maintainAttachments="NOT_MAINTAIN_ATTACHEMENTS"):
            exported_feature = cs.ExportFeatures(in_features=feature_class,
                                                out_features=filename,
                                                )
        print(filename)
        return exported_feature.getOutput(0)
    def send_mail(self, log_perimetro:dict, log_distancia:dict):
        subject = "Relatório de cálculo de perímetro e distância"
        text = f'''
        {log_perimetro['title']}\n
        {log_perimetro['text']}\n
        {log_perimetro['status']}\n
        {log_perimetro['time']}\n
        Contagem de linhas anterior: {log_perimetro['previous_row_count']}\n
        Contagem de linhas atual: {log_perimetro['current_row_count']}\n
        \n
        {log_distancia['title']}\n
        {log_distancia['text']}\n
        {log_distancia['status']}\n
        {log_distancia['time']}\n
        Contagem de linhas anterior: {log_distancia['previous_row_count']}\n
        Contagem de linhas atual: {log_distancia['current_row_count']}\n
        '''
        email = {
            'subject': subject,
            'text': text
        }
        notification = EmailNotification(email)
        notification.send_email()

    def run(self):
        perimetro = self.Calc_Perimetro.run()
        distancia = self.Calc_Distancia.run()
        return perimetro, distancia
    

if __name__ == "__main__":
    vao_de_linha = settings.ARCGIS["vao_de_linha"]
    roco_de_vao = settings.ARCGIS["roco_de_vao"]
    output_calc_distancia = settings.ARCGIS["output_calc_distancia"]
    output_calc_perimetro = settings.ARCGIS["output_calc_perimetro"]
    db_manager = Database('log.db')
    pipeline = Pipeline(vao_de_linha, roco_de_vao, output_calc_distancia, output_calc_perimetro)
    
    def run_function():
        relatorio_perimetro, relatorio_distancia = pipeline.run()
        pipeline.send_mail(relatorio_perimetro, relatorio_distancia)
        db_manager.insert_data(relatorio_perimetro, 'perimetro')
        db_manager.insert_data(relatorio_distancia, 'distancia')
        print('-'*50)
        for k,v in relatorio_perimetro.items():
            print(f'{k}: {v}')
        print('-'*50)
        for k,v in relatorio_distancia.items():
            print(f'{k}: {v}')
        print('-'*50)
        
    print('Inputs Corretos - Em processamento...')
    run_function()
    
    print('Processo finalizado, notificação de status enviada ao email "victor.farias@taesa.com.br"')
    # schedule.every().day.at("00:00").do(run_function)
    # while True:
    #     schedule.run_pending()
    #     print("Waiting...")
    #     time.sleep(3600)
    