#!/home/dejice/work/python-tutorial/ast-venv/bin/python3
#/usr/bin/python3

# ALPyNA : Automatic Loop Parallelisation in Python for Heterogeneous Architectures
# Copyright (C) <2019>  <Dejice Jacob>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# long with this program.  If not, see <https://www.gnu.org/licenses/>.


import sys
import Static_Analysis_Driver as parloop

import Utils as flt_util
import numpy as np


def copy_test(acc):
    return acc.rcopy()


def gen2D_data_george(arr_type='uint32'):
    n = 32 * 1024
    _arr1 = np.arange(0, n - 2, 1, dtype=arr_type)
    _arr2 = np.arange(10000, 10000 + n - 2, 1, dtype=arr_type)
    _arr3 = np.arange(20000, 20000 + n - 2, 1, dtype=arr_type)
    _arr4 = np.arange(30000, 30000 + n - 2, 1, dtype=arr_type)
    _arr5 = np.arange(40000, 40000 + n - 2, 1, dtype=arr_type)
    _arr6 = np.arange(50000, 50000 + n - 2, 1, dtype=arr_type)
    _arr7 = np.arange(60000, 60000 + n - 2, 1, dtype=arr_type)
    _arr8 = np.arange(70000, 70000 + n - 2, 1, dtype=arr_type)
    _arr9 = np.arange(80000, 80000 + n - 2, 1, dtype=arr_type)
    _arr10 = np.arange(90000, 90000 + n - 2, 1, dtype=arr_type)
    _arr = np.array([_arr1, _arr2, _arr3, _arr4, _arr5
                     , _arr6, _arr7, _arr8, _arr9, _arr10 
                     , _arr1, _arr2, _arr3, _arr4, _arr5
                     , _arr6, _arr7, _arr8, _arr9, _arr10 
                     , _arr1, _arr2, _arr3, _arr4, _arr5
                     , _arr6, _arr7, _arr8, _arr9, _arr10 
                     , _arr1, _arr2, _arr3, _arr4, _arr5
                     , _arr6, _arr7, _arr8, _arr9, _arr10 
                     , _arr1, _arr2, _arr3, _arr4, _arr5
                     , _arr6, _arr7, _arr8, _arr9, _arr10 ], copy=True)
    return _arr

def gen2D_data(size=1024, arr_type='uint32'):
    _arr0 = np.arange(0, size , 1, dtype=arr_type)
    _arr = np.array([ np.arange(0, size, 1 , dtype=arr_type) for _rmax in range(size)], dtype=arr_type, copy=True)
    return _arr

def gen1D_data(arr_type='uint32', size=1024):
    return np.arange(0,size,1,dtype=arr_type)

def test_saxpy(filename ) :
    with open(filename, mode="r") as fd:
        code = fd.read()
        _as_mod = parloop.static_analyse(code)
        arr_y = gen1D_data()
        arr_x = gen1D_data()
        const_a = 10

        print("Generated array-y = {0}\nGenerated array-x = {1}\nconst-a = {2}".format( arr_y , arr_x , const_a ))
        _as_mod.saxpy( arr_y , arr_x , const_a )
        print("Result array-y = {0}\nGenerated array-x = {1}\nconst-a = {2}".format( arr_y , arr_x , const_a ))

def test_matmul( filename ):
    def _vm_matmul( ma , mb , mc ) :
        ma_rmax, ma_cmax = np.shape( ma )
        mb_rmax, mb_cmax = np.shape( mb )
        print(" Shape - A = {0}, Shape - B = {1} , Shape - C = {2} ".format( np.shape(ma), np.shape(mb), np.shape(mc)))

        for i in range(ma_rmax):
            for j in range(mb_cmax):
                for k in range(ma_cmax):
                    mc[i][j] = mc[i][j] + ma[i][k] * mb[k][j]

    with open(filename, mode="r") as fd:
        code = fd.read()
        _as_mod = parloop.static_analyse(code)

        _csize = 2048
        mat_A = gen2D_data(size=_csize)
        mat_B = gen2D_data(size=_csize)
        mat_C = np.zeros((_csize,_csize), dtype='uint32')
        print("Generated Matrix-A = \n{0}".format(mat_A.shape))
        #print("Generated Matrix-B = \n{0}".format(mat_B))
        #print("Generated Matrix-C = \n{0}".format(mat_C))
        #_as_mod.matmul(mat_A, mat_B, mat_C)
        print("MatMult returned = \n{0}".format(mat_C.shape))
        #mat_C = np.zeros((_csize,_csize), dtype='uint32')
        #print("VM Generated Matrix-C = \n{0}".format(mat_C))
        #_vm_matmul(mat_A, mat_B, mat_C)
        #print("VM Calculated Matrix-C = \n{0}".format(mat_C))






def test_george(filename):
    with open(filename, mode="r") as fd:
        code = fd.read()
        _as_mod = parloop.static_analyse(code)
        #ret = _as_mod.caledonia( np.array([[ j for j in range(10)] for i in range(10)], dtype='uint32') \
        #            , np.array([[ j for j in range(10)] for i in range(10)], dtype='uint32') , 1)

        arg_a = gen2D_data_george()
        print("Generated-data = \n{0}".format(arg_a))
        assert True, "Breakpoint before execution"
        ret = _as_mod.george(arg_a)
        print("george returned = \n{0}".format(ret))
        i_max, j_max = np.shape(ret)
        for i in range(i_max):
            for j in range(j_max):
                if i < i_max-1 and j < j_max -1 and ret[i][j] == ret[i][j+1] :
                    print("Stopping at [{0}][{1}] --- [{2}][{3}]".format(i,j,i,j+1))
                    break



def test_jacobi(filename):
    with open(filename, mode="r") as fd:
        code = fd.read()
        _as_mod = parloop.static_analyse(code)

        _dimsize = 64
        orig_coeff = gen2D_data(size=_dimsize, arr_type='float32')
        new_coeff = np.zeros((_dimsize,_dimsize), dtype='float32')
        err = np.zeros((_dimsize,_dimsize), dtype='float32')
        print("Generated-orig-coeff = \n{0}".format(orig_coeff))
        print("initial-result-coeff = \n{0}".format(new_coeff))
        print("initial-err= \n{0}".format(new_coeff))
        _as_mod.jacobi_relax_core(new_coeff, orig_coeff, err )
        print("after-result-coeff = \n{0}".format(new_coeff))
        print("after-err = \n{0}".format(err))


def test_caledonia(filename):
    with open(filename, mode="r") as fd:
        code = fd.read()
        _as_mod = parloop.static_analyse(code)

        #i_max, j_max , k_max , m_max = (48,28,40,50)
        #vec_a = np.zeros((i_max+2,j_max+2, k_max, m_max), dtype='float32')
        #vec_b = np.array([ i for i in range( i_max+2 )] , dtype='float32')
        i_max, j_max , k_max , m_max = (50,4,40,50)
        vec_a = np.zeros((i_max,j_max+10, k_max, m_max), dtype='float32')
        vec_b = np.array([ i for i in range( i_max )] , dtype='float32')
        #print("vec-a before = \n{0}".format(vec_a))
        _as_mod.caledonia( vec_a , vec_b , ( i_max, j_max, k_max, m_max ))
        #print("vec-a after = \n{0}".format(vec_a))


def test_conway(filename):
    def init_board( size ) :
        '''construct a square board (2d list of 0s) with side-length size'''
        return np.zeros((size,size), dtype=('uint32'))

    def printBoard(board):
        '''print board to stdout as a table'''
        for i in range(len(board)):
            for j in range(len(board[i])):
                print("%d" % board[i][j], end='')
            print()
        print()


    with open(filename, mode="r") as fd:
        code = fd.read()
        _as_mod = parloop.static_analyse(code)

        _size = 10
        board_a = init_board(_size)
        board_b = init_board(_size)

        # a glider 
        board_a[4][1] = 1
        board_a[4][2] = 1
        board_a[4][3] = 1
        board_a[3][3] = 1
        board_a[2][2] = 1

        for n in range(10):
            _as_mod.conway(board_a,board_b,_size)
            board_a,board_b = board_b,board_a 

        print(board_b)

       
def test_predication(filename):
    with open(filename, mode="r") as fd:
        code = fd.read()
        _as_mod = parloop.static_analyse(code)

        #arg_A = gen1D_data(arr_type='float32', size=16*1024)
        arg_A = np.arange(0, 16*1024 , 0.5, dtype='float32')
        print("Generated Data =\n{0}".format(arg_A))
        _as_mod.ceiling( arg_A, 10)
        print("Result Data =\n{0}".format(arg_A))


def test_vector_add( filename ):
    with open(filename, mode="r") as fd:
        code = fd.read()
        _as_mod = parloop.static_analyse(code)

        _arr_size = 64*1024
        arr_a = gen1D_data(arr_type='uint32' , size=_arr_size)
        arr_b = gen1D_data(arr_type='uint32' , size=_arr_size)
        arr_c = np.zeros((_arr_size,) , dtype='uint32')
        print("Generated Data Array-A=\n{0}\nArray-B=\n{1}\nArray-C=\n{2}".format(arr_a, arr_b, arr_c))
        _as_mod.vector_add( arr_c, arr_a , arr_a )
        print("Result Data Array-A=\n{0}\nArray-B=\n{1}\nArray-C=\n{2}".format(arr_a, arr_b, arr_c))

def test_hilbert( filename ):
    with open(filename, mode="r") as fd:
        code = fd.read()
        _as_mod = parloop.static_analyse(code)

        _arr_size = 4
        _output = _as_mod.hilbert_matrix(_arr_size)
        print("Hilbert Matrix generated = \n{0}".format(_output))

def test_black_scholes( filename ):
    def randfloat( rand_var, low, high ):
        return ((1.0 - rand_var) * low) + (rand_var * high)

    with open(filename, mode="r") as fd:
        code = fd.read()
        _as_mod = parloop.static_analyse(code)

        _arr_size = 32
        _call = np.zeros( _arr_size )
        _put  = -np.ones( _arr_size )
        _stock_price = randfloat(np.random.random(_arr_size), 5.0, 30.0)
        _strike_price = randfloat(np.random.random(_arr_size), 1.0, 100.0)
        _years = randfloat(np.random.random(_arr_size), 0.25, 10.0)
        _risk_free = 0.02 
        _volatility = 0.30

        print("Initial Call array = {0}\nPut array = \n{1}".format(_call, _put))
        _output = _as_mod.black_scholes( _call, _put, \
                                         _stock_price, _strike_price ,\
                                         _years, _risk_free, _volatility, 1 )
        print("Final Call array = {0}\nPut array = \n{1}".format(_call, _put))


def test_gemver( filename ):
    with open(filename, mode="r") as fd:
        code = fd.read()
        _as_mod = parloop.static_analyse(code)

        _vec_size = 64
        _alpha, _beta = (2,1) 
        _A = gen2D_data(size=_vec_size, arr_type='uint32')
        _u1 = gen1D_data(size = _vec_size, arr_type='uint32')
        _u2 = gen1D_data(size = _vec_size, arr_type='uint32')
        _v1 = gen1D_data(size = _vec_size, arr_type='uint32')
        _v2 = gen1D_data(size = _vec_size, arr_type='uint32')
        _w = np.zeros(_vec_size, dtype='uint32')
        _x = np.zeros(_vec_size, dtype='uint32')
        _y = gen1D_data(size = _vec_size, arr_type='uint32')
        _z = gen1D_data(size = _vec_size, arr_type='uint32')
        
        _as_mod.gemver( _alpha, _beta, _A, _u1, _u2, _v1, _v2, _w, _x, _y, _z )
        print("Output : A' = \n{0}\nOutput x=\n{1}\nOutput w=\n{2}".format(_A,_x,_w))


def test_atax( filename ):
    with open(filename, mode="r") as fd:
        code = fd.read()
        _as_mod = parloop.static_analyse(code)

        _vec_size = 64
        _A = gen2D_data(size=_vec_size, arr_type='uint32')
        _x = gen1D_data(size = _vec_size, arr_type='uint32')
        _y = np.zeros(_vec_size, dtype='uint32')
        _tmp = gen1D_data(size = _vec_size, arr_type='uint32')
        _as_mod.atax( _A, _x, _y, _tmp )
        print("Output : A' = \n{0}\nOutput y=\n{1}".format(_A,_y))

def test_syr2k( filename ):
    with open(filename, mode="r") as fd:
        code = fd.read()
        _as_mod = parloop.static_analyse(code)

        _vec_size = 64
        _alpha, _beta = (1,2)
        _A = gen2D_data(size=_vec_size, arr_type='float32')
        _B = gen2D_data(size=_vec_size, arr_type='float32')
        _C = gen2D_data(size=_vec_size, arr_type='float32')
        _as_mod.syr2k( _alpha, _beta, _C,_A,_B)
        print("Output : C' = \n{0}".format(_C))


def test_mandelbrot( filename ):
    with open(filename, mode="r") as fd:
        code = fd.read()
        _as_mod = parloop.static_analyse(code)

        _vec_size , _ksize = (32, 3)
        _c = np.array([[complex(float(x)/10000,float(y)/10000) for y in range(_vec_size) ] for x in range(_vec_size)])
        _img = np.zeros((_vec_size,_vec_size),dtype='uint32')
        print("Input : c' = \n{0}\n,Input image = \n{1}".format(_c, _img))
        _as_mod.mandelbrot( _img, _c, 100, 4 )
        print("Output : c' = \n{0}\n,Output image = \n{1}".format(_c, _img))



def test_convolution2D( filename ):
    with open(filename, mode="r") as fd:
        code = fd.read()
        _as_mod = parloop.static_analyse(code)

        _vec_size , _k_size = (32,3)
        _out = gen2D_data(size=_vec_size, arr_type='float32')
        _in = gen2D_data(size=_vec_size, arr_type='float32')
        _h = gen2D_data(size=_k_size, arr_type='float32')
        print("Input : _out' = \n{0}\n,Input _in = \n{1}\nInput _h = \n{2}".format(_out, _in, _h))
        _as_mod.conv2d( _out , _in, _h )
        print("Output : _out' = \n{0}\n,Output _in = \n{1}\nOutput _h = \n{2}".format(_out, _in, _h))
        
def test_fbcorr( filename ):
    with open(filename, mode="r") as fd:
        code = fd.read()
        _as_mod = parloop.static_analyse(code)

        _num_imgs , _num_filters , _vec_size , _ksize = (4, 4, 64, 5)
        imgs = np.random.randn( _num_imgs, _vec_size , _vec_size, 3 )
        filters = np.random.randn( _num_filters, _ksize , _ksize , 3 )
        output = np.zeros((_num_imgs, _num_filters, _ksize * 3, _ksize * 3 ))
        print("Input : output = \n{0}\n,Input imgs = \n{1}\nInput filters = \n{2}".format(output, imgs, filters))
        _as_mod.fbcorr( imgs , filters, output )
        print("Output : output = \n{0}\n,Output imgs = \n{1}\nOutput filters = \n{2}".format(output, imgs, filters))



def test_dls_example( filename ):
    with open(filename, mode="r") as fd:
        code = fd.read()
        _as_mod = parloop.static_analyse(code)

        _im , _jm , _km, _mm = ( 10,100,100,100 )
        _limits = (_im , _jm , _km, _mm )
        #_constants = (10, 99, -1)
        #_constants = (0, 1, -2)
        _constants = (1, 1, -1)
        _idm, _jdm, _kdm , _mdm = ( _im+10 , _jm + 100  , _km, _mm )
        _arg_b = np.arange( 0, 10, step = 1 ,  dtype='float32') 
        _arg_a = np.zeros((_idm, _jdm, _kdm , _mdm), dtype='float32')
        _as_mod.caledonia( _arg_a, _arg_b, _constants, _limits )


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Usage : Please pass name of file on command-line")
    else:
        filename = sys.argv[1]
        test_matmul(filename)
