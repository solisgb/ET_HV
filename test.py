#!/usr/bin/env python
# coding=Latin-1

import numpy as np
lat=np.array([  0.,   2.,   4.,   6.,   8.,  10.,  12.,  14.,  16.,  18.,  20.,
        22.,  24.,  26.,  28.,  30.,  32.,  34.,  36.,  38.,  40.,  42.,
        44.,  46.,  48.,  50.,  52.,  54.,  56.,  58.,  60.,  62.,  64.,
        66.,  68.,  70.], np.float32)

ro_d15=np.array([[ 14.80000019,  15.30000019,  15.5 ,  15.  ,14.19999981,  13.60000038,  13.80000019,  14.60000038, 15.19999981,  15.30000019,  14.80000019,  14.5  , 14.80000019,  15.30000019,  15.5 ,  15. , 14.19999981,  13.60000038,  13.80000019,  14.60000038, 15.19999981,  15.30000019,  14.80000019,  14.5 ],
       [ 14.39999962,  15.10000038,  15.39999962,  15.10000038,         14.39999962,  14.        ,  14.10000038,  14.69999981,        15.19999981,  15.10000038,  14.5       ,  14.19999981,         15.10000038,  15.5       ,  15.5       ,  14.89999962,         13.89999962,  13.30000019,  13.5       ,  14.39999962,         15.10000038,  15.39999962,  15.10000038,  14.89999962],
       [ 14.10000038,  14.89999962,  15.30000019,  15.30000019,         14.69999981,  14.30000019,  14.39999962,  14.89999962,         15.19999981,  14.89999962,  14.19999981,  13.80000019,         15.30000019,  15.60000038,  15.5       ,  14.69999981,         13.60000038,  13.        ,  13.19999981,  14.10000038,         15.10000038,  15.5       ,  15.30000019,  15.19999981],
       [ 13.80000019,  14.60000038,  15.30000019,  15.30000019,         14.89999962,  14.60000038,  14.69999981,  15.10000038,         15.19999981,  14.69999981,  13.89999962,  13.39999962,         15.60000038,  15.80000019,  15.5       ,  14.5       ,         13.30000019,  12.60000038,  12.89999962,  13.89999962,         15.        ,  15.60000038,  15.60000038,  15.5       ],
       [ 13.39999962,  14.39999962,  15.19999981,  15.39999962,         15.10000038,  14.80000019,  14.89999962,  15.19999981,         15.19999981,  14.5       ,  13.60000038,  13.10000038,         15.89999962,  15.89999962,  15.5       ,  14.30000019,         13.        ,  12.19999981,  12.5       ,  13.60000038,         14.89999962,  15.69999981,  15.80000019,  15.80000019],
       [ 13.        ,  14.10000038,  15.10000038,  15.5       ,         15.30000019,  15.10000038,  15.10000038,  15.30000019,         15.10000038,  14.30000019,  13.19999981,  12.69999981,         16.10000038,  16.        ,  15.39999962,  14.10000038,         12.69999981,  11.89999962,  12.19999981,  13.39999962,         14.80000019,  15.69999981,  16.        ,  16.10000038],
       [ 12.60000038,  13.80000019,  14.89999962,  15.5       ,         15.5       ,  15.30000019,  15.30000019,  15.39999962,         15.10000038,  14.10000038,  12.89999962,  12.19999981,         16.39999962,  16.20000076,  15.39999962,  13.89999962,         12.30000019,  11.5       ,  11.80000019,  13.10000038,         14.69999981,  15.80000019,  16.20000076,  16.29999924],
       [ 12.19999981,  13.5       ,  14.69999981,  15.60000038,         15.69999981,  15.60000038,  15.60000038,  15.5       ,         15.        ,  13.80000019,  12.5       ,  11.80000019,         16.60000038,  16.20000076,  15.30000019,  13.60000038,         12.        ,  11.10000038,  11.39999962,  12.80000019,         14.5       ,  15.80000019,  16.39999962,  16.60000038],
       [ 11.80000019,  13.19999981,  14.60000038,  15.60000038,         15.80000019,  15.80000019,  15.69999981,  15.60000038,         14.89999962,  13.60000038,  12.10000038,  11.39999962,         16.79999924,  16.29999924,  15.19999981,  13.39999962,         11.60000038,  10.69999981,  11.        ,  12.5       ,         14.39999962,  15.80000019,  16.60000038,  16.79999924],
       [ 11.39999962,  12.89999962,  14.39999962,  15.5       ,         15.89999962,  16.        ,  15.89999962,  15.60000038,         14.69999981,  13.30000019,  11.69999981,  10.89999962,         16.89999962,  16.29999924,  15.10000038,  13.10000038,         11.19999981,  10.19999981,  10.60000038,  12.19999981,         14.19999981,  15.80000019,  16.70000076,  17.        ],
       [ 10.89999962,  12.5       ,  14.19999981,  15.5       ,         16.        ,  16.10000038,  16.        ,  15.60000038,         14.60000038,  13.        ,  11.30000019,  10.39999962,         17.10000038,  16.29999924,  14.89999962,  12.80000019,         10.89999962,   9.80000019,  10.19999981,  11.80000019,         14.        ,  15.80000019,  16.79999924,  17.20000076],
       [ 10.5       ,  12.10000038,  13.89999962,  15.39999962,         16.10000038,  16.29999924,  16.20000076,  15.69999981,         14.39999962,  12.69999981,  10.89999962,  10.        ,         17.20000076,  16.39999962,  14.80000019,  12.5       ,         10.39999962,   9.39999962,   9.80000019,  11.5       ,         13.80000019,  15.69999981,  16.89999962,  17.39999962],
       [ 10.        ,  11.80000019,  13.69999981,  15.30000019,         16.20000076,  16.39999962,  16.29999924,  15.60000038,         14.19999981,  12.30000019,  10.39999962,   9.5       ,         17.29999924,  16.29999924,  14.60000038,  12.19999981,         10.        ,   8.89999962,   9.30000019,  11.10000038,         13.5       ,  15.60000038,  17.        ,  17.60000038],
       [  9.60000038,  11.30000019,  13.39999962,  15.30000019,         16.29999924,  16.60000038,  16.39999962,  15.60000038,         14.10000038,  12.        ,  10.        ,   9.10000038,         17.5       ,  16.29999924,  14.39999962,  11.80000019,          9.60000038,   8.5       ,   8.89999962,  10.69999981,         13.30000019,  15.5       ,  17.10000038,  17.70000076],
       [  9.10000038,  10.89999962,  13.10000038,  15.10000038,         16.29999924,  16.70000076,  16.5       ,  15.60000038,         13.80000019,  11.60000038,   9.5       ,   8.60000038,         17.60000038,  16.20000076,  14.19999981,  11.5       ,          9.19999981,   8.        ,   8.39999962,  10.30000019,         13.        ,  15.39999962,  17.10000038,  17.79999924],
       [  8.60000038,  10.5       ,  12.80000019,  15.        ,         16.29999924,  16.79999924,  16.60000038,  15.5       ,         13.60000038,  11.30000019,   9.10000038,   8.10000038,         17.60000038,  16.20000076,  14.        ,  11.10000038,          8.69999981,   7.5999999 ,   8.        ,   9.89999962,         12.69999981,  15.30000019,  17.10000038,  17.89999962],
       [  8.10000038,  10.10000038,  12.5       ,  14.5       ,         16.29999924,  16.89999962,  16.60000038,  15.5       ,         13.39999962,  10.89999962,   8.60000038,   7.5999999 ,         17.70000076,  16.10000038,  13.80000019,  10.69999981,          8.30000019,   7.0999999 ,   7.5999999 ,   9.5       ,         12.39999962,  15.10000038,  17.10000038,  18.        ],
       [  7.5999999 ,   9.69999981,  12.19999981,  14.69999981,         16.29999924,  17.        ,  16.70000076,  15.30000019,         13.10000038,  10.39999962,   8.10000038,   7.0999999 ,         17.70000076,  16.        ,  13.5       ,  10.30000019,          7.80000019,   6.5999999 ,   7.0999999 ,   9.10000038,         12.10000038,  15.        ,  17.10000038,  18.10000038],
       [  7.0999999 ,   9.19999981,  11.80000019,  14.60000038,         16.29999924,  17.        ,  16.70000076,  15.30000019,         12.89999962,  10.        ,   7.5999999 ,   6.5999999 ,         17.70000076,  15.89999962,  13.19999981,   9.89999962,          7.4000001 ,   6.19999981,   6.5999999 ,   8.69999981,         11.80000019,  14.80000019,  17.10000038,  18.10000038],
       [  6.5999999 ,   8.80000019,  11.5       ,  14.39999962,         16.29999924,  17.10000038,  16.70000076,  15.10000038,         12.5       ,   9.60000038,   7.0999999 ,   6.        ,         17.70000076,  15.69999981,  12.89999962,   9.5       ,          6.9000001 ,   5.69999981,   6.19999981,   8.19999981,         11.39999962,  14.60000038,  17.10000038,  18.20000076],
       [  6.0999999 ,   8.30000019,  11.10000038,  14.19999981,         16.20000076,  17.10000038,  16.70000076,  15.        ,         12.19999981,   9.19999981,   6.69999981,   5.5999999 ,         17.70000076,  15.60000038,  12.60000038,   9.10000038,          6.4000001 ,   5.19999981,   5.69999981,   7.80000019,         11.10000038,  14.39999962,  17.10000038,  18.20000076],
       [  5.5999999 ,   7.80000019,  10.69999981,  13.89999962,         16.10000038,  17.10000038,  16.70000076,  14.80000019,         11.89999962,   8.69999981,   6.19999981,   5.0999999 ,         17.70000076,  15.39999962,  12.30000019,   8.69999981,          6.        ,   4.69999981,   5.19999981,   7.30000019,         10.69999981,  14.19999981,  17.        ,  18.20000076],
       [  5.0999999 ,   7.30000019,  10.30000019,  13.69999981,         16.        ,  17.10000038,  16.60000038,  14.69999981,         11.60000038,   8.30000019,   5.69999981,   4.5       ,         17.60000038,  15.19999981,  12.        ,   8.19999981,          5.5       ,   4.30000019,   4.69999981,   6.9000001 ,         10.30000019,  13.89999962,  16.89999962,  18.20000076],
       [ 46.09999847,   6.9000001 ,   9.89999962,  13.39999962,         16.        ,  17.10000038,  16.60000038,  14.39999962,         11.19999981,   7.80000019,   5.0999999 ,   4.        ,         17.60000038,  15.        ,  11.60000038,   7.80000019,          5.        ,   3.79999995,   4.19999981,   6.4000001 ,          9.89999962,  13.69999981,  16.79999924,  18.20000076],
       [  4.0999999 ,   6.4000001 ,   9.5       ,  13.10000038,         13.80000019,  17.10000038,  16.5       ,  14.19999981,         10.89999962,   7.4000001 ,   4.69999981,   3.5999999 ,         17.5       ,  14.80000019,  11.19999981,   7.30000019,          4.5       ,   3.29999995,   3.79999995,   6.        ,          9.5       ,  13.39999962,  16.70000076,  18.20000076],
       [  3.5999999 ,   5.9000001 ,   9.10000038,  12.89999962,         15.69999981,  17.        ,  16.39999962,  14.        ,         10.5       ,   6.9000001 ,   4.19999981,   3.0999999 ,         17.39999962,  14.5       ,  10.89999962,   6.80000019,          4.0999999 ,   2.9000001 ,   3.29999995,   5.5       ,          9.10000038,  13.10000038,  16.60000038,  18.20000076],
       [  3.0999999 ,   5.4000001 ,   8.60000038,  12.60000038,         15.60000038,  17.        ,  16.39999962,  13.80000019,         10.10000038,   6.4000001 ,   3.70000005,   2.5999999 ,         17.29999924,  14.30000019,  10.39999962,   6.4000001 ,          3.5999999 ,   2.4000001 ,   2.9000001 ,   5.        ,          8.69999981,  12.80000019,  16.39999962,  18.10000038],
       [  2.70000005,   4.9000001 ,   8.19999981,  12.19999981,         15.39999962,  16.89999962,  16.20000076,  13.60000038,          9.69999981,   5.9000001 ,   3.20000005,   2.0999999 ,         17.20000076,  14.        ,  10.        ,   5.9000001 ,          3.0999999 ,   2.        ,   2.4000001 ,   4.5       ,          8.19999981,  12.5       ,  16.29999924,  18.10000038],
       [  2.20000005,   4.4000001 ,   7.69999981,  11.89999962,         15.30000019,  16.89999962,  16.20000076,  13.30000019,          9.30000019,   5.4000001 ,   2.70000005,   1.70000005,         17.10000038,  13.80000019,   9.60000038,   5.4000001 ,          2.70000005,   1.60000002,   2.        ,   4.        ,          7.80000019,  12.19999981,  16.10000038,  18.        ],
       [  1.79999995,   3.9000001 ,   7.19999981,  11.60000038,         15.10000038,  16.89999962,  16.10000038,  13.10000038,          8.89999962,   4.9000001 ,   2.20000005,   1.29999995,         17.        ,  13.5       ,   9.19999981,   4.9000001 ,          2.20000005,   1.20000005,   1.60000002,   3.5999999 ,          7.30000019,  11.80000019,  16.        ,  18.        ],
       [  1.29999995,   3.4000001 ,   6.80000019,  11.19999981,         14.89999962,  16.79999924,  16.        ,  12.80000019,          8.39999962,   4.4000001 ,   1.79999995,   0.89999998,         16.89999962,  13.19999981,   8.80000019,   4.4000001 ,          1.79999995,   0.80000001,   1.20000005,   3.0999999 ,          6.80000019,  11.5       ,  15.80000019,  17.89999962],
       [  0.89999998,   2.9000001 ,   6.30000019,  10.89999962,         14.80000019,  16.79999924,  15.89999962,  12.5       ,          8.        ,   4.        ,   1.39999998,   0.5       ,         16.79999924,  12.89999962,   8.30000019,   3.9000001 ,          1.39999998,   0.5       ,   0.80000001,   2.5999999 ,          6.30000019,  11.10000038,  15.60000038,  17.89999962],
       [  0.60000002,   2.4000001 ,   5.80000019,  10.5       ,         14.69999981,  16.79999924,  15.80000019,  12.19999981,          7.5       ,   3.5       ,   1.        ,   0.2       ,         16.70000076,  12.60000038,   7.9000001 ,   3.4000001 ,          1.        ,   0.2       ,   0.5       ,   2.20000005,          5.9000001 ,  10.69999981,  15.5       ,  17.89999962],
       [  0.2       ,   2.        ,   5.30000019,  10.10000038,         14.5       ,  16.89999962,  15.80000019,  12.        ,          7.0999999 ,   2.9000001 ,   0.60000002,   0.        ,         16.70000076,  12.19999981,   7.4000001 ,   2.9000001 ,          0.60000002,   0.        ,   0.2       ,   1.70000005,          5.30000019,  10.39999962,  15.30000019,  18.        ],
       [  0.        ,   1.5       ,   4.80000019,   9.80000019,         14.39999962,  17.10000038,  15.89999962,  11.69999981,          6.5999999 ,   2.4000001 ,   0.30000001,   0.        ,         16.70000076,  12.        ,   6.9000001 ,   2.4000001 ,          0.30000001,   0.        ,   0.        ,   1.29999995,          4.9000001 ,  10.        ,  15.30000019,  18.20000076],
       [  0.        ,   1.10000002,   4.19999981,   9.39999962,         14.39999962,  17.29999924,  16.10000038,  11.39999962,          6.0999999 ,   2.        ,   0.        ,   0.        ,         16.89999962,  11.69999981,   6.4000001 ,   2.        ,          0.1       ,   0.        ,   0.        ,   0.89999998,          4.4000001 ,   9.60000038,  15.19999981,  18.5       ]], np.float32)


if __name__ == "__main__":
	"""
	descripcion
	"""
	try:
		
		y=np.interp(37., lat, ro_d15[:, 0])
		print(y)
	except:
		from traceback import format_exc
		a='\n{}'.format(format_exc())
		print ('{}'.format(a))
	finally:
		print('fin')
