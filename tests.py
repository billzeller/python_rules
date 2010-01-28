from Rules import Rules
                    

if __name__ == "__main__":
    r = Rules()
    assert r.matches((1,2,3), (1,2,3))
    assert r.matches((_,2,3), (1,2,3))
    assert not r.matches(3, 4)
    assert r.matches(_, 4)
    assert r.matches([1,2,_,(3,4,_)],[1,2,"holla",(3,4,5)]) 
    
    r = Rules((1, 2, _), 'rule 1',
              (1, 2, 3), 'rule 2',
              (None, 2), 'rule 3',
              lambda x: x == 234, 'rule 4',
              'something', 'rule 5')
    
    assert r(1,2,3) == 'rule 1'
    assert r(1,2,4) == 'rule 1'
    assert r(None, 2) == 'rule 3'
    assert r(234) == 'rule 4'
    assert r('something') == 'rule 5'
    
    
    f = Rules((1,1,1), 4,
              (_,5,_), lambda x,y,z: x*z,
              (_,_,_), lambda x,y,z: 100*x + 10*y + z)
              
    assert f(1,1,1) == 4
    assert f(3,5,8) == 24
    assert f(6,7,8) == 678
    
    fib1 = Rules(0, 1,
                 1, 1,
                 _, lambda x: fib1(x-1)+fib1(x-2))
                 
    def fib2(n):
        if n == 0 or n == 1:
            return 1
        else:
            return fib2(n-1) + fib2(n-2)

    for i in xrange(10):
        assert fib1(i) == fib2(i)
        
    # A dumb way to sum a list
    mysum = Rules([], 0,
                   _, lambda x: x[0]+mysum(x[1:]))
                    
    assert mysum([1,2,3,5]) == 11
    
    fact1 = Rules(0, 1,
                  _, lambda n: n*fact1(n-1))
                
    def fact2(n):
        if n == 0 or n == 1:
            return 1
        else:
            return n*fact2(n-1)
            
    for i in xrange(10):
        assert fact1(i) == fact2(i)
    
    f = Rules(lambda x: x % 2 == 0, 'even',
              _, 'odd')
              
    assert f(0) == 'even'
    assert f(1) == 'odd'
    assert f(2) == 'even'
    assert f(3) == 'odd'

    qs = Rules([], [],
               _, lambda l: qs([x for x in l[1:] if x < l[0]])
                            + l[:1]
                            + qs([x for x in l[1:] if x >= l[0]]))

    assert qs([]) == []
    assert qs([1]) == [1]
    assert qs([5,2]) == [2,5]
    assert qs([5,2,9]) == [2,5,9]
    assert qs([3,1,6,9,2]) == [1,2,3,6,9]
