import os
import math

#path = "SET PATH TO DIRECTORY WHERE TEST FILES ARE STORED"
os.chdir(path)

def convexHull(fname):
    def get_coords(fname):
        with open(fname) as inputFile:
            coords = [tuple(map(int, line.strip("\n").split(" "))) for line in inputFile]
        return coords
    
    def get_p0(lst):
        p0_idx = 0
        for idx in range(1, len(lst)):
            if lst[idx][1] < lst[p0_idx][1]: p0_idx = idx
        return lst[p0_idx]
    
    def distance(p1, p2):
        return math.sqrt((p2[1]-p1[1])**2 + (p2[0]-p1[0])**2)
    
    def polarAngle(p1, p0):
        return math.atan2(p1[1]-p0[1], p1[0]-p0[0]) 

    def polarMergeSort(lst, pzero):
        collinears = []
        if len(lst) > 1:
            mid = len(lst)//2
            lhalf = lst[:mid]
            rhalf = lst[mid:]

            polarMergeSort(lhalf, pzero)
            polarMergeSort(rhalf, pzero)

            i, j, k = 0, 0, 0

            while i < len(lhalf) and j < len(rhalf):
                if polarAngle(lhalf[i], pzero) == polarAngle(rhalf[j], pzero):
                    if distance(lhalf[i], pzero) > distance(rhalf[j], pzero):
                        collinears.append(rhalf[j])
                    elif distance(lhalf[i], pzero) < distance(rhalf[j], pzero):
                        collinears.append(lhalf[i])
                    else:
                        rhalf.remove(rhalf[j])
                
                if polarAngle(lhalf[i], pzero) < polarAngle(rhalf[j], pzero):
                    lst[k] = lhalf[i]
                    i += 1                    
                else:
                    lst[k] = rhalf[j]
                    j += 1
                k += 1
            while i < len(lhalf):
                lst[k] = lhalf[i]
                i += 1
                k += 1

            while j < len(rhalf):
                lst[k] = rhalf[j]
                j += 1
                k += 1    
        return [x for x in lst if x not in collinears]    
    
    def xproduct(p0, pi, pj):
        x0, y0 = p0[0], p0[1]
        xi, yi = pi[0], pi[1]
        xj, yj = pj[0], pj[1]
        return (xi-x0)*(yj-y0)-(xj-x0)*(yi-y0)
    
    lst = get_coords(fname)
    pzero = get_p0(lst)                
    lst.remove(pzero)                   
    lst = polarMergeSort(lst, pzero)    
    
    if len(lst) >= 2:
        stack = [pzero, lst[0], lst[1]]
        for i in range(2, len(lst)):
            while xproduct(stack[-2], stack[-1], lst[i]) < 0:
                stack.pop()
            if xproduct(stack[-2], stack[-1], lst[i]) == 0:
                stack.pop()
                stack.append(lst[i])
                continue
            stack.append(lst[i])
        return stack
    else:
        return [pzero]+lst
