#!/usr/bin/env python
# coding: latin-1
from win32com.client import Dispatch

class Connection(object):
	"""
	permite operar con una bdd access mdb or accdb
	Late Binding vs. Early Binding in COM objects. 
	This is not ADO specific, but rather an issue of using any COM object with Python. Basically, there are two ways that a Python COM object can access its methods and properties. These two methods are called Late Binding and Early Binding. If a Python COM object uses Late Binding, then every time you access a method or property of the object, it goes through the IDispatch interface to find the method/property, even if it is the same one being called each time. With Early Binding, we let Python know ahead of time what methods and properties are available to an object. This speeds up things significantly, especially inside loops, and the performance gains are actually quite substantial. To enable Early Binding for ADO objects, we need to import the ADO library. To do this:

		In PythonWin, go to Tools --> COM Makepy Utility
		In the dialog box that pops up, scroll down till you reach Microsoft ActiveX Data Objects Library. If there are multiple versions, simply pick the latest one.
		Click on the OK button. The PythonWin environment will freeze for a little bit, while the library is being imported. In a little while, you should see a message on the Interactive Window that says that a file was generated.
		You've successfully generated a Python type library for ADO. From now on, Python will automatically use the type library to early-bind any ADO objects.

	You can get by without importing the ADO library, but the performance gains are well worth it. Now, let's move on to exploring how to use the different ADO objects with Python. 

	Connection strings
	http://www.connectionstrings.com/access-2007
	
	Hay 2 maneras de grabar los resultados de un recordset a fichero
	1) método writeRecordset2file
	2) método fetchall con fieldsNames=1
		función write2file
	La manera 2 es más rápida que 1
	
	"""
	__objets_type=['TABLE', 'LINK', 'PASS-THROUGH', 'VIEW']
	__format_float_default='{0:0.2f}'
	__none2str='nd'
	__cstring={'acces2003': 'PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE= {} ;', 
		'BDAServer':'Provider=SQLOLEDB.1;Password=estrella;Persist Security Info=True;User ID=intecsa;Initial Catalog=BDAServer;Data Source=INTWKS1044\SQLEXPRESS',
		'acces2007':'Provider=Microsoft.ACE.OLEDB.12.0;Data Source={};Persist Security Info=False;'}
	__codec='cp1252'

	def __init__(self, db, cstring='access2003'):
		"""
		constructor
		"""
		from os.path import isfile, splitext

		a=splitext(db)
		if a[1][1:]=='mdb':
			assert isfile(db),'no se encuentra {0}'.format(db)
			cs=Connection.__cstring['acces2003'].format(db)
		else:
			if db=='BDAServer':
				cs=Connection.__cstring['BDAServer']
			else:
				raise Exception('No se disponde de cadena de conexión para \n{}'.format(db))

		self.db=db
		self.conn = Dispatch('ADODB.Connection')
		#self.conn.ConnectionString = "Driver={Microsoft Access Driver (*.mdb, *.accdb)};Dbq="+self.db+";Uid=Admin;Pwd=;"
		self.conn.ConnectionString = cs
		self.conn.Open()

	def __del__(self):
		self.conn.Close()

	def close(self):
		self.conn.Close()

	def __open_recordset(self, conn, recordset, cacheSize=1, maxrecords=0):
		assert cacheSize>0
		rs = Dispatch('ADODB.Recordset')
		rs.CursorLocation = 3
		rs.ActiveConnection = conn
		if maxrecords>0:
			rs.MaxRecords=maxrecords
		if cacheSize>1:
			rs.CacheSize=cacheSize
		rs.Open(recordset)
		return rs

	def tablas_get_asdict(self,tables=1,links=0,queries=0,pass_throughs=0):
		"""
		devuelve los nombres de las tablas,adjuntos,etc. de la db como una diccionario
		cuyas keys son los tipos de objetos Connection.__objets_type
		"""
		#import os.path

		for k, item in enumerate((tables,links,queries,pass_throughs)):
			assert isinstance(item, int), 'el argumento opcional {0:d} debe ser int'.format(k)

		args=[Connection.__objets_type[k] for k, item in enumerate((tables,links,queries,pass_throughs)) if item==1 ]
		if len(args)==0:
			return []

		objects=[(item, []) for item in Connection.__objets_type]
		objects=dict(objects)
		keys = objects.keys()
		
		oCat = Dispatch('ADOX.Catalog')
		oCat.ActiveConnection = self.conn
		
		for item in oCat.Tables:
			a=item.Type.lower()
			if  a in keys:
				objects[a].append(item.Name)

		return objects

	def tablas_get(self,tables=1,links=0,queries=0,pass_throughs=0):
		"""
		devuelve los nombres de las tablas,adjuntos,etc. de la db como una lista ordenada
		"""
		#import os.path
		
		for k, item in enumerate((tables,links,queries,pass_throughs)):
			assert isinstance(item, int), 'el argumento opcional {0:d} debe ser int'.format(k)

		args=[Connection.__objets_type[k] for k, item in enumerate((tables,links,queries,pass_throughs)) if item==1 ]
		if len(args)==0:
			return []
		oCat = Dispatch('ADOX.Catalog')
		oCat.ActiveConnection = self.conn
		objects=[item.Name for item in oCat.Tables if item.Type in args]
		objects.sort()
		return objects

	def fields_get(self,recordset):
		"""
		devuelve los campos de un recordset (tabla o select)como un diccionario
		cuyas keys son los nombes de los campos y contiene el type y el defined size
		"""
		if recordset.upper().startswith('SELECT'):
			rs=self.__open_recordset(self.conn, recordset, maxrecords=1)
		else:
			rs=self.__open_recordset(self.conn, '['+recordset+']', maxrecords=1)

		if rs.Fields.Count>0:
			fields=[[rs.Fields.Item(item).Name, [rs.Fields.Item(item).Type,rs.Fields.Item(item).DefinedSize ]]for item in range(rs.Fields.Count)]
			fields=dict(fields)
		else:
			fields={}
		return fields

	def fieldsNames_get(self,recordset):
		"""
		devuelve los nombres de un recordset (tabla o select) como una lista
		"""
		if recordset.upper().startswith('SELECT'):
			rs=self.__open_recordset(self.conn, recordset, maxrecords=1)
		else:
			rs=self.__open_recordset(self.conn, '['+recordset+']', maxrecords=1)

		if rs.Fields.Count>0:
			fields=[rs.Fields.Item(item).Name for item in range(rs.Fields.Count)]
		else:
			fields=[]
		return fields

	def execute(self, recordset):
		rs = Dispatch('ADODB.Recordset')
		rs.CursorLocation = 3
		rs.ActiveConnection = self.conn
		rs.Open(recordset)
		
	def fetchall(self,recordset,fieldsNames=0, cacheSize=100):
		"""
		recordset: puede ser un recordset o una sentencia select
		fieldsNames: si 1 devuelve el nombre de los campos
		cacheSize: number of records that can be cached
		"""

		for item in (fieldsNames, cacheSize):
			assert isinstance(item, int)
		rs=self.__open_recordset(self.conn, recordset, cacheSize)

		if fieldsNames==1:
			names=[rs.Fields.Item(f).Name for f in range(rs.Fields.Count)]
		else:
			names=[]
		
		try:
			rs.MoveFirst()
		except:
			return []
			
		tmp=list(zip(*rs.GetRows()))
		rs.Close()

		if tmp==None:
			data=[]
		else:
			data=[list(row) for row in tmp]

		if fieldsNames==1 and len(data)>0:   
			data.insert(0, names)
		return data
			
	def fetchone(self,recordset, cacheSize=100):
		"""
		recordset: puede ser un recordset o una sentencia select
		cacheSize: number of records that can be cached
		"""
		rs=self.__open_recordset(self.conn, recordset, cacheSize)

		if rs.RecordCount<=0:
			#data= []
			pass
		else:
			rs.MoveFirst()
			while not rs.EOF:
				row=[rs.Fields.Item(i).Value for i in range(rs.Fields.Count)]
				yield row
				rs.MoveNext()

		rs.Close()

	@staticmethod
	def row2strdefault(row, none2str=None):
		"""
		transforma los contenidos de la lista row en str de acuerdo
		a un formato preestablecido en la función
		"""
		from pywintypes import Time
		from datetime import datetime,date
		from decimal import Decimal
		
		if none2str==None:
			none2str=Connection.__none2str
		
		crow=list(row)
		for k in range(len(crow)):
			if crow[k]==None:
				crow[k]=none2str
				continue
				
			if isinstance(crow[k], str):
				crow[k]='{}'.format(crow[k])  #.encode(Connection.__codec))
			#elif isinstance(crow[k], str):
				#pass
			elif isinstance(crow[k], (type(Time(0)), datetime, date)):
				crow[k]=Connection.__default_datetimeformat2str(crow[k])
			elif isinstance(crow[k],(int, float, Decimal)):
				crow[k]='{0:g}'.format(crow[k])
			else:
				crow[k]='{}'.format(crow[k])
		return crow

	@staticmethod
	def __default_datetimeformat2str(obj):
		from pywintypes import Time
		from datetime import datetime,date
		
		if isinstance(obj, (type(Time(0)), datetime)):
			if obj.hour + obj.minute + obj.second ==0:
				obj1='{0:02d}/{1:02d}/{2:04d}'.format(obj.day, obj.month, obj.year)
			else:
				obj1='{0:02d}/{1:02d}/{2:04d} {3:02d}:{4:02d}:{5:02d}'.format(obj.day, 
				obj.month, obj.year, obj.hour, obj.minute,  obj.second)
		elif isinstance(obj,date):
			obj1='{0:02d}/{1:02d}/{2:04d}'.format(obj.day, obj.month, obj.year)
		else:
			obj1=obj
		
		return obj1
			

	@staticmethod
	def __urow2str(row, none2str=None):
		"""
		convierte a str una lista row de objetos unicode o str
		"""
		if none2str==None:
			none2str=Connection.__none2str
			
		crow=list(row)
		for k in range(len(crow)):
			if crow[k]==None:
				crow[k]=none2str
			else:
				if isinstance(crow[k], str):
					#crow[k]='{}'.format(crow[k].encode(Connection.__codec))
					crow[k]='{}'.format(crow[k])
		return crow

	@staticmethod
	def row2str(row, formatter=[], none2str=None):
		"""
		transforma los contenidos de una lista row en strings
		formatter es una lista con el formato de cada elemento de row
		si formatter tiene distinta longitud que row, se realiza un formato
			por defecto
		none2str:: valor por los que se sustutuyen los elementos de row que son None
		"""
		from pywintypes import Time
		from datetime import datetime,date
		
		if none2str==None:
			none2str=Connection.__none2str
			
		if len(formatter)!=len(row):
			#myf=[]
			use_myf=False
		else:
			#myf=formatter
			use_myf=True

		crow=list(row)
		if use_myf:
			try:
				for k in range(len(crow)):
					if crow[k]==None:
						crow[k]=none2str
						continue
					else:
						if isinstance(crow[k], str):
							#crow[k]=formatter[k].format(crow[k].encode('cp1252'))
							crow[k]=formatter[k].format(crow[k])
						elif isinstance(crow[k], (type(Time(0)), datetime, date)):
							b=''
							for a1 in formatter[k]:
								if a1!=' ':
									b=b+a1
							if b=='{}':
								crow[k]=Connection.__default_datetimeformat2str(crow[k])
							else:
								crow[k]=formatter[k].format(crow[k])
						else:
							crow[k]=formatter[k].format(crow[k])
			except:
				from traceback import format_exc
				a='\ncolumna {0:d}, tipo {1}, format {2}\n{3}'.format(k, type(crow[k]), 
					formatter[k], format_exc())   #.encode(Connection.__codec))
				raise Exception(a)
			
		else:
			crow=Connection.row2strdefault(crow)
		
		return crow

	def write_select_as_csv(self, select_stm, dst, dialect={}, add_columns=[], 
		formatter=[], return_data=False, none2str=None ):
		"""
		write el resultado del select select_stm en dst utilizando el dialecto MyDialect
		al final de la fila devuelta por select_stm se puede insertar una o varias columnas
		a través de add_columns
		dialect: dialecto csv, ahora solo utiliza el separador
		add_columns:: cada elemento es una lista cuyo primer elemento es la cabecera de la
		columna y el segundo es el contenido de la columna
		return_data: si True devuelve el resultado de la select
			la primera fila contiene el nombre de los campos
			el resto de filas almacena los datos
		"""
		import csv
		
		if none2str==None:
			none2str=Connection.__none2str
		
		if len(dialect)==0:
			pure_csv=True
		else:
			pure_csv=False
		
		data=[]
		
		fnames=self.fieldsNames_get(select_stm)
		for h, v in add_columns:
			fnames.append(h)
		if return_data:
			data.append(fnames)
	
		if len(formatter)>0 and (len(formatter)!=len(fnames)):
			formatter=[]
		#with open(dst, 'wb') as f:
		with open(dst, 'w', newline='') as f:
			if pure_csv:
				writer = csv.writer(f)
			else:
				csv.register_dialect('myDialect', delimiter=dialect['separator'])
				writer = csv.writer(f, 'myDialect')
			
			fnames=Connection.__urow2str(fnames)
			writer.writerow(fnames)
			for row in self.fetchone(select_stm):
				for h, v in add_columns:
					row.append(v)
				if return_data:
					data.append(list(row))
				
				if pure_csv:
					row=Connection.__urow2str(row)
				else:
					row=Connection.row2str(row, formatter)
					
				writer.writerow(row)
		
		if return_data:
			return data
		else:
			return None

	#deprecated, dont use them

	@staticmethod
	def write2file(dst, data, fmt=[], fieldsNames=[], overwrite=1, separator='\t', comentarios=None ):
		"""
		Graba la matriz data a fichero, el numero de columnas debe ser
		igual en todas las filas
		dst nombre de fichero de texto donde se graban los resultados
		data: matriz
		fmt: lista con los formatos de grabación de cada columna, si no se pasa se generan
			con la función formato_row
			Cada elemento fmt debe ser de la forma {0:s}, etc. Siempre debe ser {0}
			Algunos tipos deben ser tratados antes de grabarlos
			1) los tipos datetime.date, datetime.datetime y pywintypes.time se graban con
			   formato {0!s} y se transforman como obj.encode('Latin-1)
			2) los tipos str y unicode se graban con formato {0!s}.encode('Latin-1)
			3) el resto de tipos se graban directamente bajo fmt
		fieldsNames: lista con los nombres de las columnas, si no se pasa se ponen los nombres
			de los campos
		overwite: controla si se graba encima de un fichero ya existente
		separator: entre columnas
		"""
		from os.path import dirname, isdir, isfile
		from pywintypes import Time
		from datetime import datetime,date
		#from decimal import Decimal
		
		if len(data)==0:
			return
		
		if len(fieldsNames)>0 and len(fmt)>0:
			assert len(fieldsNames)==len(fmt), 'fieldsNames ({0}) y fmt ({0}) deben tener el mismo num de elementos'.format(len(fieldsNames), len(fmt))

		if len(dirname(dst))>0:
			assert isdir(dirname(dst)), 'no existe {0}'.format(dirname(dst))
		if overwrite==0 and isfile(dst):
			raise ValueError('{0} ya existe y no se puede sobreescribir'.format(dst))

		if len(fmt)!=0:
			for i, item in enumerate(fmt):
				if not isinstance(item, type('str')):
					fmt[i]=str(item)
		else:
			fmt=Connection.formato_row(data[0])

		assert len(fmt)==len(data[0]), 'fmt ({0}) y len(data[0]) deben tener el mismo num de elementos'.format(len(fmt), len(data[0]))

		type_Time=type(Time(0))
		type_Date=type(date.today())
		type_Datetime=type(datetime.today())
		#type_Decimal=type(Decimal(1.1))

		f=open(dst, 'w')
		if comentarios!=None:
			f.write('{0}\n'.format(comentarios))  #.encode(Connection.__codec)))
		
		if len(fieldsNames)>0:
			f.write('{0}'.format(fieldsNames[0]))  #.encode(Connection.__codec)))
			if len(fieldsNames)>1:
				for item in fieldsNames[1:]:
					f.write('\t{0}'.format(item))  #.encode(Connection.__codec)))
			f.write('\n')

		for row in data:
			k=0
			for col, fm in zip(row, fmt):
				if k>0: f.write(separator)
				if k==0: k=1
				if col==None:
					f.write('None')
				else:
					if isinstance(col, str):
						f.write(fm.format(col))  #.encode(Connection.__codec)))
					elif isinstance(col,type_Time):
						if col.hour + col.minute + col.second ==0:
							f.write(col.Format("%d/%m/%Y"))
						else:
							f.write(col.Format("%d/%m/%Y %H %M %S"))
					elif isinstance(col,type_Datetime):
						if col.hour + col.minute + col.second ==0:
							f.write(col.strftime("%d/%m/%Y"))
						else:
							f.write(col.strftime("%d/%m/%Y %H %M %S"))
					elif isinstance(col,type_Date):
						f.write(col.strftime("%d/%m/%Y"))
					else:
						try:
							f.write(fm.format(col))
						except:
							f.write('{0!r}'.format(col))
			f.write('\n')

		f.close()

	def writeRecordset2file(self, dst, recordset, fmt=[], fieldsNames=[], overwrite=1, separator='\t', cacheSize=1,  comentarios=None ):
		"""
		igual que write2file pero se ejecuta el recordset para extraer data
		llama a fetchone, lo que permite ejecutar la acción utilizando menos memoria
		"""
		from os.path import dirname, isdir, isfile
		from pywintypes import Time
		from datetime import datetime,date		
		#from decimal import Decimal
		
		if len(fieldsNames)>0 and len(fmt)>0:
			assert len(fieldsNames)==len(fmt), 'fieldsNames ({0}) y fmt ({0}) deben tener el mismo num de elementos'.format(len(fieldsNames), len(fmt))

		if len(dirname(dst))>0:
			assert isdir(dirname(dst)), 'no existe {0}'.format(dirname(dst))
		if overwrite==0 and isfile(dst):
			raise ValueError('{0} ya existe y no se puede sobreescribir'.format(dst))

		if len(fmt)!=0:
			flag_fmt=1
			for i, item in enumerate(fmt):
				if not isinstance(item, type('str')):
					fmt[i]=str(item)
		else:
			flag_fmt=0

		type_Time=type(Time(0))
		type_Date=type(date.today())
		type_Datetime=type(datetime.today())
		#type_Decimal=type(Decimal(1.1))

		f=open(dst, 'w')
		
		if comentarios!=None:
			f.write('{0}\n'.format(comentarios))  #.encode(Connection.__codec)))
		
		if len(fieldsNames)>0:
			f.write('{0}'.format(fieldsNames[0]))  #.encode(Connection.__codec)))
			if len(fieldsNames)>1:
				for item in fieldsNames[1:]:
					f.write('\t{0}'.format(item))  #.encode(Connection.__codec)))
			f.write('\n')

		
		for row in self.fetchone(recordset,cacheSize=cacheSize):
			if flag_fmt==0:
				flag_fmt=1
				fmt=Connection.formato_row(row)
			k=0
			for col, fm in zip(row, fmt):
				if k>0: f.write(separator)
				if k==0: k=1
				if col==None:
					f.write('None')
				else:
					if isinstance(col, str):
						f.write(fm.format(col))  #.encode(Connection.__codec)))
					elif isinstance(col,type_Time):
						if col.hour + col.minute + col.second ==0:
							f.write(col.Format("%d/%m/%Y"))
						else:
							f.write(col.Format("%d/%m/%Y %H %M %S"))
					elif isinstance(col,type_Datetime):
						if col.hour + col.minute + col.second ==0:
							f.write(col.strftime("%d/%m/%Y"))
						else:
							f.write(col.strftime("%d/%m/%Y %H %M %S"))
					elif isinstance(col,type_Date):
						f.write(col.strftime("%d/%m/%Y"))
					else:
						try:
							f.write(fm.format(col))
						except:
							f.write('{0!r}'.format(col))
			f.write('\n')

		f.close()

	@staticmethod
	def formato_row(row):
		"""
		crea una lista con los formatos de grabación de row
		los formatos de fecha hora se ponen como string y el método donde se graban es
		el encargado de pasarlos a string
		los formatos de float y decimal se crean con __format_float_default
		"""
		from pywintypes import Time
		from datetime import datetime,date
		from decimal import Decimal
		type_Time=type(Time(0))
		type_Date=type(date.today())
		type_Datetime=type(datetime.today())
		type_Decimal=type(Decimal(1.1))
		fmt=[]
		for item in row:
			if isinstance(item, str) or isinstance(item, str):
				fmt.append('{0:s}')
			elif isinstance(item, int) or isinstance(item, int):
				fmt.append('{0:d}')				
			elif isinstance(item, float) or isinstance(item, type_Decimal):
				fmt.append(Connection.__format_float_default)
			elif isinstance(item,type_Time) or isinstance(item,type_Datetime) or isinstance(item,type_Date):
				fmt.append('{0:s}')
			else:
				fmt.append('{0!r}')	
		return fmt		
