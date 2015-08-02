__author__ = 'claudia'
from config import wmata
from math import hypot
from multiprocessing import Pool

def f_range(mini, maxi, step):
    while mini < maxi:
        yield mini
        mini += step

class DistanceCalculations:
    def __init__(self, lat1, lat2, lon1, lon2, res):
        self.lat1, self.lat2 = lat1, lat2
        self.lon1, self.lon2 = lon1, lon2
        self.latlist = list(f_range(self.lat1, self.lat2, self.res))
        self.lonlist = list(f_range(self.lon1, self.lon2, self.res))
        self.res = res

    def find_dist(self, stat, lata, longa):
        dx = stat.location.lon - longa
        dy = stat.location.lat - lata
        return hypot(dx,dy)
    
    def find_add(self, line, stat, lata, longa):
        wa = self.find_dist(stat, lata, longa)
        const = 1 / calc_trainfreq(line)
        return const/(wa**2)
    
    def point_calc(self, lata, longa):
        i = 0.0
        for s in wmata.lines.all:
            for staa in wmata.lines[s].stations:
                i += self.find_add(s, staa, lata, longa)
        # print("calculated (" + str(lata) + "," + str(longa) + ")")
        return i
    
    
    def point_map(self):
        print(len(self.latlist) * len(self.lonlist))
        input("Do this many points across 5 processors? (ctrl-C if u r scared) ")
        pool = Pool(5)
        single_lat_dict_list = pool.map(self.singlelat, latlist)
        return dict(zip(self.latlist, single_lat_dict_list))
    
    def singlelat(self, lat):
        return {lon: point_calc(lat, lon) for lon in self.lonlist}
    
    
def calc_trainfreq(m):
   return 1   
    
def samplerunfullcity():
    max_lon = 39.130282
    min_lon = 38.755377
    max_lat = -76.829635
    min_lat = -77.314407
    resi = .01
    distance_calc_obj = DistanceCalculations(min_lat, max_lat, min_lon, max_lon, resi)
    distance_calc_obj.point_map()
    print("Done")
    
if __name__ == '__main__':
    samplerunfullcity()