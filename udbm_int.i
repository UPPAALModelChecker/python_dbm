/*    Copyright 2011 Peter Bulychev
#
#    This file is part of Python binding to the UPPAAL DBM library.
#
#    This binding is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This binding is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this binding.  If not, see <http://www.gnu.org/licenses/>.
*/

%module udbm_int

%{
#define SWIG_FILE_WITH_INIT
#include "udbm_int.h"
%}

%include "std_string.i"
%include "std_vector.i"


class VarNamesAccessor{
        public:
            void setClockName(int index, std::string name);
};

class Constraint {    
    public:
        Constraint (int i, int j, int d, bool isStrict);
};

class IntClockValuation {
    public:
        IntClockValuation(int size);
        void setClockValue(int index, int);
};

class DoubleClockValuation {
    public:
        DoubleClockValuation(int size);
        void setClockValue(int index, double);
};

class IntVector {
    // for some reason it's impossible to use this http://www.swig.org/Doc1.3/Library.html#Library_nn15
    public:
        IntVector(int );
        void setElement(int , int);
};

class Federation {
    public:
        Federation(int dim);
        Federation(int dim, Constraint &t);
        Federation(const Federation&);
        std::string toStr(VarNamesAccessor &);
        Federation& operator |= (Federation &);
        Federation& operator &= (Federation &);
        Federation& operator += (Federation &);
        Federation& operator -= (Federation &);
        Federation orOp  (Federation &); // for some reason SWIG will not work if operator is defined here      
        Federation andOp (Federation &);
        Federation addOp (Federation &);
        Federation minusOp (Federation &);
        void up();
        void down();
        void mergeReduce(int, int);
        void freeClock(int i);
        bool lt(Federation& ); 
        bool gt(Federation& );
        bool le(Federation& );
        bool ge(Federation& );
        bool eq(Federation& ); 
        void setZero();
        void predt(Federation &);
        void intern();
        void setInit();
        void convexHull();
        bool containsIntValuation(IntClockValuation);
        bool containsDoubleValuation(DoubleClockValuation);
        void myExtrapolateMaxBounds(IntVector);
        bool hasZero();
        void updateValue(int x, int v);
        int size();
        int hash();
        bool isEmpty();
};


