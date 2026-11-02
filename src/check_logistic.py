import sympy as sp

def main():
    #(positive=True tells SymPy they're > 0)
    C, mu, k, K = sp.symbols("C mu k K", positive=True)
    #the left side, logistic growth with loss
    lhs = mu*C*(1 - C/K) - k*C
    #claimed form
    r  = mu - k
    Kp = K*(mu - k)/mu
    rhs = r*C*(1 - C/Kp)
    #are they the same?
    print(sp.simplify(lhs - rhs))          # should print 0

    #the equilibrium (where dC/dt = 0)
    print(sp.solve(sp.Eq(lhs, 0), C))      # should include K*(mu - k)/mu

if __name__ == "__main__":
    main()
