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
        self.res = res
        print(self.lat1, self.lat2, self.lon1, self.lon2, self.res)
        self.latlist = list(f_range(self.lat1, self.lat2, self.res))
        self.lonlist = list(f_range(self.lon1, self.lon2, self.res))


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
        print("lat length "  + str(len(self.latlist)))
        print("lon length "  + str(len(self.lonlist)))
        print(len(self.latlist) * len(self.lonlist))
        input("Do this many points across 9 processors? (ctrl-C if u r scared) ")
        pool = Pool(9)
        single_lat_dict_list = pool.map(self.singlelat, self.latlist)
        return dict(zip(self.latlist, single_lat_dict_list))
    
    def singlelat(self, lat):
        x = {lon: self.point_calc(lat, lon) for lon in self.lonlist}
        print("lat done: " + str(lat))
        return x

    
    
def calc_trainfreq(m):
   return 1   

def samplerunbeltway():
    max_lon = 39.008953
    min_lon = 38.823838
    max_lat = -76.872716
    min_lat = -77.204129
    resi = .001
    distance_calc_obj = DistanceCalculations(min_lat, max_lat, min_lon, max_lon, resi)
    return distance_calc_obj.point_map()


def sampleruninnercity():
    max_lon = 38.951372
    min_lon = 38.869972
    max_lat = -76.982933
    min_lat = -77.982933
    resi = .001
    distance_calc_obj = DistanceCalculations(min_lat, max_lat, min_lon, max_lon, resi)
    return distance_calc_obj.point_map()


def sampleruntiny():
    max_lon = 38.917349
    min_lon = 38.875307
    max_lat = -77.003089
    min_lat = -77.051867
    resi = .001
    distance_calc_obj = DistanceCalculations(min_lat, max_lat, min_lon, max_lon, resi)
    return distance_calc_obj.point_map()


def samplerunfullcity():
    max_lon = 39.136673
    min_lon = 38.755377
    max_lat = -76.829635
    min_lat = -77.288315
    resi = .001
    distance_calc_obj = DistanceCalculations(min_lat, max_lat, min_lon, max_lon, resi)
    return distance_calc_obj.point_map()


if __name__ == '__main__':
    data = samplerunfullcity()
    csvdata = []
    for lat in data:
        for lon in data[lat]:
            csvdata.append((lat, lon, data[lat][lon]))
        
    stringydata = "\n".join([",".join(list(map(str, i))) for i in csvdata])
    with open("data.csv", "w") as f:
        f.write(stringydata)
    print("Done")