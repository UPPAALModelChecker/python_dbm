import udbm

import unittest

class UDBMTest(unittest.TestCase):
    def setUp(self):
        self.c = udbm.Context(["x", "y", "z"], name = "c")
    def test_int_valuation(self):
        c = self.c
        v = udbm.IntValuation(c)
        self.assertRaises(KeyError, lambda :(v["not_in_federation"]))
        self.assertRaises(TypeError, v.__setitem__, ("x", 0.1)) # too bad we aren't using python 2.7 where it's possible to use "with self.assertRaises"
        v["x"] = 1
        v["y"] = 1
        v["z"] = 1
        self.assertTrue(( (c.x == 1) & (c.y == 1) & (c.z == 1)).contains(v))
        self.assertFalse(((c.x == 2) & (c.y == 1) & (c.z == 1)).contains(v))
    def test_float_valuation(self):
        c = self.c
        v = udbm.FloatValuation(c)
        self.assertRaises(KeyError, lambda :(v["not_in_federation"]))
        v["x"] = 1.0
        v["y"] = 1.01
        v["z"] = 1
        self.assertFalse(( (c.x == 1) & (c.y == 1) & (c.z == 1)).contains(v))
        self.assertTrue(((c.x == 1) & (c.y < 2) & (c.y > 1) & (c.z == 1)).contains(v))
    def test_set_operations(self):
        c = self.c
        self.assertTrue( (c.x == 1) == (c.x >= 1) & (c.x <= 1))
        self.assertFalse( (c.x == 1) == (c.x >= 1) & (c.x < 1))
        self.assertTrue( (c.x != 1) == ((c.x > 1) | (c.x < 1)))
        self.assertFalse( (c.x != 1) == ((c.x > 1) | (c.x <= 1)))
        self.assertTrue( (c.x == 1) & (c.y == 1)  == (c.y == 1) & (c.x == 1))
        self.assertTrue( (c.x == 1) | (c.y == 1)  == (c.y == 1) | (c.x == 1))
        self.assertFalse( (c.x == 1) | (c.y == 1)  != (c.y == 1) | (c.x == 1))
        self.assertFalse( (c.x == 1) & (c.y == 1)  != (c.y == 1) & (c.x == 1))
        self.assertTrue( (c.x == 1) & (c.y == 1)  != (c.y == 1) | (c.x == 1))
        self.assertTrue( (c.x == 1) & ((c.y == 1) | (c.z ==1))  == (c.x == 1) & (c.y == 1) |(c.x == 1) & (c.z ==1) )
        self.assertFalse( (c.x == 1) & ((c.y == 1) | (c.z ==1))  == (c.x == 1) & (c.y == 1) |(c.x == 1) )
        self.assertTrue( (c.x - c.y <= 1) == (c.y - c.x >= -1))
        self.assertFalse( (c.x - c.y <= 1) == (c.y - c.x > -1))
        self.assertTrue( ((c.x - c.y == 1) & (c.x == 1) ) == ((c.x == 1) & (c.y == 0)) )
        self.assertTrue( (c.x - c.y != 1)  == ((c.x - c.y > 1) | (c.x - c.y < 1)) )
    def test_zero(self):
        c = self.c
        self.assertFalse( (c.x == 1).hasZero())
        self.assertFalse( (c.x > 1).hasZero())
        self.assertTrue( (c.x < 1).hasZero())
        self.assertTrue( ((c.x == 1) & (c.z == 2)).setZero() ==  ((c.x == 0 ) & (c.z == 0) & (c.y ==0)  ))
        self.assertTrue( ((c.x == 1) & (c.z == 2)).setZero().hasZero())
    def test_update_clocks(self):
        c = self.c
        self.assertTrue( ((c.x == 1) | (c.z == 2)).updateValue(c.x, 2)  == (c.x == 2 ) )
        self.assertTrue( ((c.x == 1) & (c.z == 2)).resetValue(c.x)  == ((c.x == 0 ) & (c.z == 2) ) )    
    def test_str(self):
        c = self.c
        self.assertTrue(str((c.x == 1) & (c.y == 1)) == "(c.x==1 & c.x==c.y & c.y==1)")
    def test_copy(self):
        c = self.c
        a = ((c.x - c.y)==1)
        b = a.copy()
        d = b.copy()
        self.assertTrue( a == b)
        b &= (c.z == 1)
        d |= (c.z == 1)
        self.assertFalse( a == b)
        self.assertFalse( d == b)
    def test_reduce(self):
        c = self.c
        a = (c.x >= 1) | (c.x <= 1)
        self.assertTrue(a.getSize() == 2)
        a.reduce()
        self.assertTrue(a.getSize() == 1)
    def test_convex_hull(self):
        c = self.c
        d1 = (c.x >= 1) & (c.x <=2) & (c.y>=1) & (c.y <=2)
        d2 = (c.x >= 3) & (c.x <=4) & (c.y>=3) & (c.y <=4)
        d3 = (c.x - c.y <= 1) & (c.y - c.x <= 1) & (c.x >= 1) & (c.y >= 1) & (c.x <= 4) & (c.y <= 4)        
        self.assertTrue((d1 + d2) == d3)
        self.assertTrue((d1 | d2).convexHull() == d3)
        d1 += d2
        self.assertTrue(d1 == d3)
    def test_sub(self):
        c = self.c
        d1 = (c.x >= 1) & (c.x <=2) & (c.y>=1) & (c.y <=2)
        d2 = (c.x >= 3) & (c.x <=4) & (c.y>=3) & (c.y <=4)
        d3 = d1 | d2
        self.assertTrue(d3 - d1 == d2)
        d3 -= d2
        self.assertTrue(d3 == d1)
    def test_up_down(self):
        c = udbm.Context(["x", "y"]) # we need only two variables here
        d1 = (c.x >= 1) & (c.x <=2) & (c.y>=1) & (c.y <=2) 
        d2 = (c.x - c.y <= 1) & (c.y - c.x <= 1) & (c.x >= 1) & (c.y >= 1)
        d3 = (c.x - c.y <= 1) & (c.y - c.x <= 1) & (c.x <= 2) & (c.y <= 2)        
        self.assertTrue(d1.up() == d2)
        self.assertTrue(d1.down() == d3)
    def test_isnt_mutable(self):
        c = self.c
        d1 = (c.x - c.y <= 1) & (c.y - c.x <= 1) & (c.x >= 1) & (c.y >= 1) & (c.y <= 4) # some random 
        d2 = d1.copy()
        d2.up()
        self.assertTrue(d1 == d2)        
        d2.down()
        self.assertTrue(d1 == d2)        
        d2.down()
        self.assertTrue(d1 == d2)        
        d2.freeClock(c.x)
        self.assertTrue(d1 == d2)        
        d2.convexHull()
        self.assertTrue(d1 == d2)        
        d2.predt(d2)
        self.assertTrue(d1 == d2)        
        d2.resetValue(c.x)
        self.assertTrue(d1 == d2)        
    def test_set_init(self):
        c = self.c
        d = (c.x - c.y <= 1) & (c.y - c.x <= 1) & (c.x >= 1) & (c.y >= 1) & (c.y <= 4) # some random
        d.setInit()
        self.assertTrue(d == ((c.x >= 0) & (c.y >= 0) & (c.z >= 0)))
        self.assertTrue(d != ((c.x >= 1) & (c.y >= 0) & (c.z >= 0)))
    def test_federation_ops(self):
        c = self.c
        d1 = (c.x - c.y <= 1) & (c.y - c.x <= 1) & (c.x >= 1) & (c.y >= 1) & (c.y <= 4) # some random
        d2 = (c.x - c.y <= 1) & (c.y - c.x <= 1) & (c.x >= 1)
        self.assertTrue(d1 <= d2)
        self.assertTrue(d1 < d2)
        self.assertTrue(d2 >= d1)
        self.assertTrue(d2 > d1)
        self.assertFalse(d1 == d2)    
        self.assertTrue(d1 != d2)
    def test_intern(self):
        c = self.c
        d = (c["x"] - c["y"] <= 1)
        d.intern()
    def testExtrapolateMaxBounds(self):
        c = self.c
        v = (c.x - c.y <= 1) & (c.x < 150) & (c.z < 150) & (c.x - c.z <= 1000)  
        a = {c.x: 100, c.y:300, c.z:400}
        self.assertTrue(v.extrapolateMaxBounds(a) == ((c.x-c.y<=1) & (c.z<150)))
    def test_free_clock(self):
        c = self.c
        self.assertTrue(((c.x >= 10) & (c.y >= 10)).freeClock(c.x) == (c.y >= 10))
    def test_zero_federation(self):
        c = self.c
        self.assertTrue(c.getZeroFederation().isZero())
        self.assertTrue(c.getZeroFederation().hasZero())
        self.assertTrue(udbm.Federation(c).isZero())
        self.assertFalse((c.x==1).isZero())
        self.assertFalse((c.x==1) == c.getZeroFederation())
    def test_hash(self):
        c = self.c
        self.assertTrue((c.x==1).hash() == (c.x==1).hash())
        self.assertFalse((c.y==1).hash() == (c.x==1).hash())
        self.assertTrue(((c.x==1) | (c.y == 1)).hash() == ((c.y == 1) | (c.x==1)).hash())
    def test_isempty(self):
        c = self.c
        self.assertTrue(((c.x==1) & (c.x !=1)).isEmpty())
        self.assertFalse(((c.x==1) | (c.x !=1)).isEmpty())
        self.assertFalse((c.x==1).isEmpty())
        self.assertFalse(((c.x==1) & (c.y !=1)).isEmpty())
        self.assertTrue( (((c.x==1) & (c.x !=1)) | ((c.y==1) & (c.y !=1))).isEmpty())
if __name__ == '__main__':
    unittest.main()
