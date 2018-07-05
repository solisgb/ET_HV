# -*- coding: utf-8 -*-
"""
Programa para el cálculo de la evapotranspiración potencial por el método
    de Hargreaves y Samani
Los datos de las estaciones y de TMIN y TMAX están almacenados en una BDD
    Access
Los resultados del programa se graban en ficheros de texto

 _________________ACCIONES____________________

1. Calcular y grabar los coef ro para cada dia del año
2. Calular ls ETP por Hargreaves-Samani
"""

actions = {1: False,  2: True}

if __name__ == "__main__":
    from os.path import join
    from log_file import Log_file
    from hs import Estaciones, DB, Heads, HS

    try:

        hs = HS()

        if actions[1]:
            mm_days_year_get()

        if actions[2]:
            festaciones='Est_AEMET_TLat.txt'
            heads=Heads('IDINM', 'LATITUD')
            estaciones=Estaciones(join(dir_org, festaciones), heads)

            # SELECT para extraer los datos de la BDD
            select1='SELECT FECHA, TMAX, TMIN FROM TC WHERE IDINM="{0}" AND FECHA>={1} AND FECHA<={2} ORDER BY FECHA;'

            db=DB(db, select1, f1, f2)

            hs.calcular(db, estaciones, dir_out)
		
    except:
        from traceback import format_exc
        from msgbox_sin_tk import mostrar_error
        a='\n{}'.format(format_exc())
        mostrar_error(a)
        Log_file.write(a)
        print(a)
    finally:
        print('fin script')
        Log_file.toFile()
