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


#include "dbm/gen.h"
#include "dbm/fed.h"
#include "dbm/mingraph.h"
#include "dbm/ClockAccessor.h"
#include "hash/tables.h"
#include "hash/compute.h"

#include <string.h>
#include <map>
#include <iostream>
#include <vector>

using namespace dbm;
using namespace std;


class VarNamesAccessor: public ClockAccessor {
        map<int, string> names_map;
        public:
            void setClockName(int index, std::string name) {
                names_map[index] = string(name);
            }
            virtual const std::string getClockName(cindex_t i) const {
                map<int, string>::const_iterator iterator = this->names_map.find(i);
                return iterator->second;
            }
            bool hasClockName(cindex_t i) const {
                map<int, string>::const_iterator iterator = this->names_map.find(i);
                return (iterator != names_map.end());
            }
};

class Constraint {    
    friend class Federation;
    constraint_t constraint;
public:
    Constraint (int i, int j, int d, bool isStrict) : 
        constraint(cindex_t(i), cindex_t(j), int32_t(d), isStrict) {
    }
};

class IntClockValuation {
    friend class Federation;
        IntValuation val;
    public:
        IntClockValuation(int size): 
            val(size) {}
        void setClockValue(int index, int value)  {
            val[index] = value;
        }
};

class DoubleClockValuation {
    friend class Federation;
        DoubleValuation val;
    public:
        DoubleClockValuation(int size): 
            val(size) {}
        void setClockValue(int index, double value)  {
            val[index] = value;
        }
};

class IntVector {
    // for some reason it's impossible to use this http://www.swig.org/Doc1.3/Library.html#Library_nn15
    public:
        vector<int> v;
        IntVector(int i) : v(i) {}
        int getElement(int i)  {
            return v[i];
        }
        void setElement(int i, int val)  {
            v[i] = val;
        }

};



class Federation : public fed_t {
    public:
        Federation(int dim) : fed_t(dim)  {} 
        Federation(int dim, Constraint &c) : fed_t(dim) { 
            dbm_t dbm(dim);
            dbm.setInit(); 
            dbm &= c.constraint;
            add(dbm);
        };

        Federation(fed_t f): fed_t(f) {};
        
        std::string toStr(const VarNamesAccessor &a) {   
            VarNamesAccessor b = a;
            for (unsigned int i=1; i<getDimension(); i++) {
                if (!b.hasClockName(i)) {
                    std::ostringstream stream;
                    stream << "c" << i;
                    b.setClockName(i, stream.str());
                }
            }
            return toString(b);
        }

        Federation andOp (const Federation &arg) {            
            VarNamesAccessor a;
            return Federation((*this) & arg);
        }        
        
        Federation orOp (const Federation &arg) {
            return Federation((*this) | arg);
        }        
        
        Federation addOp (const Federation &arg) {
            return Federation((*this) + arg);
        }        
        
        Federation minusOp (const Federation &arg) {
            return Federation((*this) - arg);
        }        

        void opFreeClock(int i) {
            this->freeClock(i);
        }

        bool containsIntValuation(IntClockValuation v) {
            return this->contains(v.val);
        }
        bool containsDoubleValuation(DoubleClockValuation v) {
            return this->contains(v.val);
        }    

        void myExtrapolateMaxBounds(IntVector v) {
            int dimension = getDimension();
            int32_t *ia = (int32_t *)malloc(sizeof (int32_t) * dimension);
            for (int i=0; i<dimension; i++) {
                ia[i] = v.v[i];
            }
            extrapolateMaxBounds(ia);
            free(ia);
        }
}
;

