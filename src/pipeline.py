from src.distancia_roco import CalculoDistanciaRoco
from src.perimetro_roco import CalculoPerimetroRoco
import schedule
import time
from src.notificator import EmailNotification

class Pipeline:
    def __init__(self, roco_de_vao, roco_de_linha, output_calc_distancia, output_calc_perimetro):
        self.roco_de_vao = roco_de_vao
        self.roco_de_linha = roco_de_linha
        self.output_calc_distancia = output_calc_distancia
        self.output_calc_perimetro = output_calc_perimetro
        self.Calc_Perimetro = CalculoPerimetroRoco(self.roco_de_vao, self.output_calc_perimetro)
        self.Calc_Distancia = CalculoDistanciaRoco(self.roco_de_linha, self.output_calc_distancia)

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
        {log_distancia['horario']}\n
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
    roco_de_vao = r"roco_de_vao.shp"
    roco_de_linha = r"roco_de_linha.shp"
    output_calc_distancia = r"output_calc_distancia.shp"
    output_calc_perimetro = r"output_calc_perimetro.shp"
    pipeline = Pipeline(roco_de_vao, roco_de_linha, output_calc_distancia, output_calc_perimetro)
    def runs_function():
        relatorio_perimetro, relatorio_distancia = pipeline.run()
        pipeline.send_mail(relatorio_perimetro, relatorio_distancia)
        
    schedule.every().day.at("00:00").do(runs_function)
    while True:
        schedule.run_pending()
        print("Waiting...")
        time.sleep(3600)
    