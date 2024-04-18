from distancia_roco import CalculoDistanciaRoco
from perimetro_roco import CalculoPerimetroRoco
import schedule
import time

class Pipeline:
    def __init__(self, roco_de_vao, roco_de_linha, output_calc_distancia, output_calc_perimetro):
        self.roco_de_vao = roco_de_vao
        self.roco_de_linha = roco_de_linha
        self.output_calc_distancia = output_calc_distancia
        self.output_calc_perimetro = output_calc_perimetro
        self.Calc_Perimetro = CalculoPerimetroRoco(self.roco_de_vao, self.output_calc_perimetro)
        self.Calc_Distancia = CalculoDistanciaRoco(self.roco_de_linha, self.output_calc_distancia)

    def run(self):
        self.Calc_Perimetro.run()
        self.Calc_Distancia.run()

if __name__ == "__main__":
    roco_de_vao = r"C:\Users\lucas\Documents\GitHub\powerline_roco\data\roco_de_vao.shp"
    roco_de_linha = r"C:\Users\lucas\Documents\GitHub\powerline_roco\data\roco_de_linha.shp"
    output_calc_distancia = r"C:\Users\lucas\Documents\GitHub\powerline_roco\data\output_calc_distancia.shp"
    output_calc_perimetro = r"C:\Users\lucas\Documents\GitHub\powerline_roco\data\output_calc_perimetro.shp"
    pipeline = Pipeline(roco_de_vao, roco_de_linha, output_calc_distancia, output_calc_perimetro)
    def runs_function():
        pipeline.run()
    
    schedule.every().day.at("00:00").do(runs_function)
    while True:
        schedule.run_pending()
        print("Waiting...")
        time.sleep(3600)
    