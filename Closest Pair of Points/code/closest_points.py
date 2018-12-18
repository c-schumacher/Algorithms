import os 
import math
import copy
from itertools import combinations

path = 'SET PATH TO THE DIRECTORY WHERE TEST FILES ARE STORED'
os.chdir(path)

def closest_points(fname, store=False):

    def get_coords(fname):
        with open(fname) as inputFile:
            coords = [tuple(map(int, line.strip('\n').split(' '))) for line in inputFile]
        return coords

    def mergeSort(arr):
        if len(arr) > 1:
            mid = len(arr)//2
            lhalf = arr[:mid]
            rhalf = arr[mid:]

            mergeSort(lhalf)
            mergeSort(rhalf)

            i, j, k = 0, 0, 0
            while i < len(lhalf) and j < len(rhalf):
                if lhalf[i] < rhalf[j]:
                    arr[k] = lhalf[i]
                    i += 1
                else: 
                    arr[k] = rhalf[j]
                    j +=1
                k += 1

            while i < len(lhalf):
                arr[k] = lhalf[i]
                i += 1
                k += 1

            while j < len(rhalf):
                arr[k] = rhalf[j]
                j += 1
                k += 1
        return arr

    def distance(p1, p2):
        return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
    
    def brute_force(S):
        min_dist = -1
        pts = None
        for combo in combinations(S, 2):
            if min_dist < 0:
                min_dist = distance(*combo)
                pts = combo
            elif distance(*combo) < min_dist:
                min_dist = distance(*combo)
                pts = combo
        return pts[0], pts[1], min_dist

    def split_arrs(S, X, Y):
        l = len(X)//2
        x_mid = X[l][0]
        xl, xr = X[:l], X[l:]
        sl, sr = [s for s in S if s in xl], [s for s in S if s in xr]
        yl, yr = [y for y in Y if y in sl], [y for y in Y if y in sr]
        return sl, sr, xl, xr, yl, yr, x_mid
    
    def scan_mid(y, x_mid, dst_mn, mn_pts):
        y_mid = []
        for i in y:
            if x_mid - dst_mn <= i[0] <= x_mid + dst_mn:
                y_mid.append(i)       
        for i in range(len(y_mid) - 1):
            for j in range(i + 1, min(i + 7, len(y_mid))): 
                if distance(y_mid[i], y_mid[j]) < dst_mn:
                    mn_pts = y_mid[i], y_mid[j]
                    dst_mn = distance(*mn_pts)   
        return mn_pts[0], mn_pts[1], dst_mn
    
    def get_closest_pairs(S, X, Y):
        if len(S) <= 3:
            return brute_force(S)
   
        sl, sr, xl, xr, yl, yr, x_mid = split_arrs(S, X, Y)
        pl, ql, delta_l = get_closest_pairs(sl, xl, yl)
        pr, qr, delta_r = get_closest_pairs(sr, xr, yr)
    
        if delta_l < delta_r:
            delta_min = delta_l
            pts_min = (pl, ql)
        else:
            delta_min = delta_r
            pts_min = (pr, qr)
            
        p_mid, q_mid, delta_mid = scan_mid(Y, x_mid, delta_min, pts_min)  
        if delta_mid <= delta_min:
            delta_min = delta_mid
            pts_min = (p_mid, q_mid)
        return pts_min[0], pts_min[1], delta_min
    
    S = get_coords(fname)
    X = mergeSort(copy.copy(S))
    Y = [j[::-1] for j in mergeSort([i[::-1] for i in S])]
    res = get_closest_pairs(S, X, Y)
    
    if store:
        return res
    print "The minimum distance is:\n",res[2], ":", res[0], "<--->", res[1]
