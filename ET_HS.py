#!/usr/bin/env python
# coding: latin-1

import numpy as np


class Estaciones(object):

    def __init__(self, org, heads):
        """
        se leen los codigos de las estaciones y las latitudes
        org: ficheros de datos de las estaciones, la primera linea es una
            cabecera sin datos con los nombres de las columnas
        head: contiene el nombre de las columnas que se van a leer (codigos de
            las estaciones, latitudes
        """

        # se lee el fichero de estaciones con sus coordenadas
        fi = open(org, 'r')
        lines = fi.readlines()
        fi.close()
        # se lee la linea 1 del fichero y se lee la columna donde están los
        # codigos de las estaciones, latitudes
        hw = lines[0].strip().split('\t')
        icod = hw.index(heads.id)
        ilatitud = hw.index(heads.latitud)
        # se rellenan los vectores del codigo de estacion y latitudes
        linewords = [line.strip().split('\t') for line in lines[1:]]
        self.cods = [words[icod].strip() for words in linewords]
        a = [words[ilatitud].strip() for words in linewords]
        for i in range(len(a)):
            b = a[i].split('-')
            for j in range(3):
                if b[j] == '':
                    b[j] = '0'
            a[i] = [int(b[0]), int(b[1]), int(b[2]), b[3]]
        self.latitudes = []
        self.NS = []
        for i, a1 in enumerate(a):
            a1[1] = a1[1] + a1[2]/60.
            self.latitudes.append(a1[0]+a1[1]/60.)
            self.NS.append(a1[3])


def time_2_end_get(start_time, n, j):
    """
    controla el tiempo transcurrido y el que queda para terminar el programa
    start_time: tiempo en el que se inició el programa
    n: número total de eelementos a recorrer
    j: elemento actual (el primero es 1, no 0)
    """
    from time import time
    ellapsed_min = (time() - start_time) / 60.
    average_min = (ellapsed_min/j)
    min_to_end = (n-j) * average_min
    return ellapsed_min, min_to_end


class Heads(object):
    """
    se utiliza para localizar las cabeceras de un fichero de texto con ñas
    caracteristicas de las estaciones
    """
    def __init__(self, head_id, head_latitud):
        self.h = {'id': head_id, 'latitud': head_latitud}

    @property
    def id(self):
        return self.h['id']

    @property
    def latitud(self):
        return self.h['latitud']


class DB(object):
    """
    se utiliza para pasar menos argumentos a una funcion
    db: situacion de la bdd donde están los datos
    a rellenar, etc
    select1: select que se va a utilizar, la select contiene un
        {} para rellenar con la fecha
    """
    def __init__(self, db, select1, fecha1, fecha2, date_separator='/'):
        from datetime import date

        if type(fecha1) is str and type(fecha1) is str:
            fs = [fecha.split(date_separator) for fecha in (fecha1, fecha2)]
            self.fechas = [date(int(fs1[2]), int(fs1[1]), int(fs1[0]))
                           for fs1 in fs]
        else:
            self.fechas = [fecha for fecha in (fecha1, fecha2)]

        if self.fechas[0] > self.fechas[1]:
            self.fechas[0], self.fechas[1] = DB.swap(self.fechas[0],
                                                     self.fechas[1])
        self.access_fechas = ['#{0:d}/{1:d}/{2:d}#'.format(fecha.month,
                                                           fecha.day,
                                                           fecha.year)
                              for fecha in self.fechas]

        self.db = db
        self.select1 = select1
        self.date_separator = date_separator

    @staticmethod
    def swap(x1, x2):
        return x2, x1

    def table_name_in_select_get(self, select):
        ws = select.upper().split()
        try:
            i = ws.index('FROM')
            return ws[i+1]
        except Exception as error:
            raise ValueError('no se especifica el nombre de la tabla')

    def select1_get(self, cod):
        """
        devuelve una select válida en Ms Access
        la fecha viene dada como un txt en format o europeo d/m/yyyy
        o en como un tipo date
        el formato de fecha Access 2003 es #m/d/yyyy#
        """
        return self.select1.format(cod, self.access_fechas[0],
                                   self.access_fechas[1])


class HS(object):

    def __init__(self):
        """
        contenedor de metodos static para calcular la ETP por el método
            Hargreves-Samani
        """
        pass

    def ro_d15_mm_read(self, file_ro='Ro_mm_12m.txt'):
        """
        lee el fichero Ro_mm_12m.txt con los valores de Ro en el día 15 de
            cada año en distintas latitudes de los hemisferios N y S tomados
            de Allen y pasados a mm por San Roman
        """
        latitudes_Allen = []
        ro_d15 = []
        fi = open(file_ro)
        lines = fi.readlines()
        fi.close
        lines.pop(0)
        for line in reversed(lines):
            ws = line.strip().split()
            latitudes_Allen.append(float(ws[0]))
            a = [float(ws1) for ws1 in ws[1:]]
            ro_d15.append(a)
        return (latitudes_Allen, ro_d15)

    def ro_mm_days_year_get(self):
        """
        se leen las latitudes (N y S) y Ro del fichero de Allen
        las Ro están pasadas a mm por San Román
        los datos se leen en el fichero Ro_mm_12m.txt
            y se interpolan para todos los días del año por splines cúbicos
            se devuelve un dict con:
        lat: latitudes en el fichero de Allen
        N_y: valores de Ro para los 365 días del año en latitud N
        N_ly: valores de Ro para los 365 días del año bisiesto en latitud N
        S_y: valores de Ro para los 365 días del año en latitud S
        S_ly: valores de Ro para los 365 días del año bisiesto en latitud S
        """
        from datetime import date
        from scipy.interpolate import CubicSpline

        d15_ly = (date(2015, 12, 15),
                  date(2016, 1, 15), date(2016, 2, 15), date(2016, 3, 15),
                  date(2016, 4, 15), date(2016, 5, 15), date(2016, 6, 15),
                  date(2016, 7, 15), date(2016, 8, 15), date(2016, 9, 15),
                  date(2016, 10, 15), date(2016, 11, 15), date(2016, 12, 15),
                  date(2017, 1, 15))

        d15_y = (date(2016, 12, 15),
                 date(2017, 1, 15), date(2017, 2, 15), date(2017, 3, 15),
                 date(2017, 4, 15), date(2017, 5, 15), date(2017, 6, 15),
                 date(2017, 7, 15), date(2017, 8, 15), date(2017, 9, 15),
                 date(2017, 10, 15), date(2017, 11, 15), date(2017, 12, 15),
                 date(2018, 1, 15))

        id15_ly = np.array([item.toordinal() for item in d15_ly])
        id15_y = np.array([item.toordinal() for item in d15_y])

        latitudes_Allen, ro_d15 = self.ro_d15_mm_read()

        ro_d15_N = [item[0:12] for item in ro_d15]
        ro_d15_S = [item[12:24] for item in ro_d15]

        for i in range(len(ro_d15_N)):
            ro_d15_N[i].insert(0, ro_d15_N[i][-1])
            ro_d15_N[i].append(ro_d15_N[i][1])
            ro_d15_S[i].insert(0, ro_d15_S[i][-1])
            ro_d15_S[i].append(ro_d15_S[i][1])

        cs_N_ly = []
        cs_S_ly = []
        cs_N_y = []
        cs_S_y = []
        for i in range(len(ro_d15_N)):
            cs_N_ly.append(CubicSpline(id15_ly, ro_d15_N[i]))
            cs_S_ly.append(CubicSpline(id15_ly, ro_d15_S[i]))
            cs_N_y.append(CubicSpline(id15_y, ro_d15_N[i]))
            cs_S_y.append(CubicSpline(id15_y, ro_d15_S[i]))

        iday1_ly = date(2016, 1, 1).toordinal()
        idays_ly = [iday1_ly+i for i in range(366)]
        iday1_y = date(2017, 1, 1).toordinal()
        idays_y = [iday1_y+i for i in range(365)]

        rodays_N_ly = np.array([coef(idays_ly)
                               for coef in cs_N_ly], np.float32)
        rodays_S_ly = np.array([coef(idays_ly)
                               for coef in cs_S_ly], np.float32)
        rodays_N_y = np.array([coef(idays_y)
                               for coef in cs_N_y], np.float32)
        rodays_S_y = np.array([coef(idays_y)
                               for coef in cs_S_y], np.float32)

        return {'lat': latitudes_Allen, 'N_y': rodays_N_y, 'N_ly': rodays_N_ly,
                'S_y': rodays_S_y, 'S_ly': rodays_S_ly}

    def coef_days(self, lat_ro_days, latitud='N'):
        """
        calcula los coeficientes de los splines cubicos para las latitudes
        y valores diarios de ro que devuelve el metodo ro_mm_days_year_get
        """
        from scipy.interpolate import CubicSpline
        xs = lat_ro_days['lat']
        if latitud == 'N':
            for i in range(len(lat_ro_days['N_y'][0])):
                ys = lat_ro_days['N_y'][:, i]
                coef = CubicSpline(xs, ys)
            return coef
        elif latitud == 'S':
            raise ValueError('Latitud S no implementada')
        else:
            raise ValueError('Latitud debe ser N o S')

    def calcular(self, db, estaciones, dir_out,
                 file_out='ET_Hargreaves-Samani.txt',
                 file_ro='Ro_mm_12m.txt'):
        """
        calculo de la ET por el metodo de Hargreaves-Samani
        db: objecto DB con la BDD y la select a utilizar
        estaciones: Objeto estaciones en que para cada estación se indica
            si tiene latitud N o S y la latitud en grados
        dir_out: directorio de resultados
        file_out: nombre del fichero de resultados
        """
        from calendar import isleap
        from datetime import date
        from math import fmod
        from time import time
        from ado import Connection

        start_time = time()

        lat_ro_days = self.ro_mm_days_year_get()

        coef_N = self.coef_days(lat_ro_days)

        con = Connection(db.db)
        n = len(estaciones.cods)
        flag_show = 0

        latitudes_Allen = np.array(lat_ro_days['lat'], np.float32)

        for i, (cod1, latitud1, ns1) in enumerate(zip(estaciones.cods,
                                                  estaciones.latitudes,
                                                  estaciones.NS)):
            j = i+1
            if fmod(i, 5) == 0.0:
                flag_show = 1

            ilat = np.searchsorted(latitudes_Allen, latitud1)
            if latitud1 <= latitudes_Allen[0]:
                ilat = 0
                iro = (0, 1)
            elif latitud1 >= latitudes_Allen[-1]:
                ilat = len(latitudes_Allen) - 1
                iro = (len(latitudes_Allen)-2, len(latitudes_Allen)-1)
            else:
                ilat = np.searchsorted(latitudes_Allen, latitud1)
                iro = (ilat, ilat+1)

            select1 = db.select1_get(cod1)
            fechas_ts = con.fetchall(select1, cacheSize=10000)
            fechas = [date(item[0].year, item[0].month, item[0].day)
                      for item in fechas_ts]
            ts = np.array([[item[0], item[1]] for item in fechas_ts])
            ts = ts * 10.  # paso a grados C

            for fecha1, tmedias1 in zip(fechas, tmedias):
                day1=date(fecha1.year, 1, 1).toordinal()
                ifecha1=fecha1.toordinal()
                idy=ifecha1-day1
                #TODO: INTERPOLA RO
                if ns1=='N':
                    if isleap(fecha1, year):
                        ro=np.interp(latitud1, latitudes_Allen, ro_d15[:, fecha1.month-1])
                else:
                    z=np.interp(latitud1, latitudes_Allen, ro_d15[:, fecha1.month+11])
                ro.append(z)

                    #np.interp(2.5, xp, fp)


            if flag_show==1:
                ellapsed_min, min_to_end=time_2_end_get(start_time, n, j)
                print('Ellapsed min {0:0.1f}, {1:0.1f} min to end'.format(ellapsed_min, min_to_end))
                flag_show=0
