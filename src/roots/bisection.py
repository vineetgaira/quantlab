def bisection_method(f, a, b, tol=1e-5, max_iter=100):
    """
    Finds a root of function f in the interval [a, b] using the bisection method.
    """
    # Step 1: Verify the interval contains a root (opposite signs)
    if f(a) * f(b) >= 0:
        raise ValueError("The bisection method fails: f(a) and f(b) must have opposite signs.")
    
    print(f"{'Iter':<5} | {'a':<8} | {'b':<8} | {'c (Mid)':<8} | {'f(c)':<8}")
    print("-" * 50)
    
    for i in range(1, max_iter + 1):
        # Step 2: Find the midpoint
        c = (a + b) / 2
        fc = f(c)
        
        print(f"{i:<5} | {a:<8.4f} | {b:<8.4f} | {c:<8.4f} | {fc:<8.4f}")
        
        # Step 3: Check if the root is found or interval is small enough
        if abs(fc) < tol or (b - a) / 2 < tol:
            return c
        
        # Step 4: Narrow down the interval
        if f(a) * fc < 0:
            b = c  # Root is in the left half
        else:
            a = c  # Root is in the right half
            
    return (a + b) / 2

# Example Usage:
# Find the root of f(x) = x^2 - 4
func = lambda x: x**2 - 4

# Initial interval [0, 3]
root = bisection_method(func, a=0, b=3)
print("-" * 50)
print(f"Estimated Root: {root:.5f}")
