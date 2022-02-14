import sys
sys.path.append('.')
from lasManipulation import LASManipulations

if __name__ == '__main__':
    
    import pylas

    las = pylas.read("DATA/LAS_FILES/fase 2.las")
    pr = LASManipulations(las)

    print(pr.CreateBasicMatrix())