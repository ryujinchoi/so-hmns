import math

def verify_absolute_invariance(value, expected, precision=1e-15):
    error_bounds = abs(value - expected)
    is_valid = error_bounds <= precision
    return is_valid, error_bounds

if __name__ == '__main__':
    success, err = verify_absolute_invariance(0.5, 0.5)
    print(f'[SO-HMNS COMPLETED]: Valid={success}, Error={err}')
