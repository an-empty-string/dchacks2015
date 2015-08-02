import requests
import operator
import redis
import json
from functools import reduce

class Service:
    bus = "Bus"
    bus_predictions = "NextBusService"
    rail = "Rail"
    rail_predictions = "StationPrediction"
    incidents = "Incidents"

def build_url(*t):
    return "https://api.wmata.com/%s.svc/json/%s" % t

class MetrorailAddress:
    def __init__(self, data):
        self.street_address = data["Street"]
        self.city = data["City"]
        self.state = data["State"]
        self.zip_code = data["Zip"]

    def __repr__(self):
        return "%s\n%s, %s %s" % (self.street_address, self.city, self.state, self.zip_code)

class MetrorailLocation:
    def __init__(self, lat, lon, address):
        self.lat = lat
        self.lon = lon
        self.address = address

    def __repr__(self):
        return "[%s, %s]\n%s" % (self.lat, self.lon, repr(self.address))

class MetrorailCostInformation:
    def __init__(self, peak, offpeak, reduced):
        self.peak = peak
        self.offpeak = offpeak
        self.reduced = reduced

    def __repr__(self):
        return "$%.2f peak, $%.2f otherwise" % (self.peak, self.offpeak)

class MetrorailRouteMeta:
    def __init__(self, start, end, cost, distance, time):
        self.start = start
        self.end = end
        self.cost = cost
        self.distance = distance
        self.time = time

    def __repr__(self):
        return "From %s to %s (%s, %.2fmi, %dmin)" % (self.start, self.end, self.cost, self.distance, self.time)

class MetrorailRoute:
    def __init__(self, path, meta):
        self.path = path
        self.transfers = self.path[1:-1]
        self.meta = meta

    def __repr__(self):
        start = self.path[0]
        end = self.path[-1]
        transfer_string = "\n".join(["Transfer at %s" % station for station in self.transfers]) + "\n"
        return "Start at %s\n%sEnd at %s\n\n%s" % (start, transfer_string, end, self.meta)

class MetrorailTrainPrediction:
    def __init__(self, line, destination, station, time, car):
        self.line = line
        self.destination = destination
        self.station = station
        self.time = time
        self.time_int = self.time_format(time)
        self.cars = self.car_format(car)

    def car_format(self, car):
        if car == "2":
            return 8
        if car == "-":
            return 6
        return int(car)

    def time_format(self, time):
        if time == "ARR":
            return 1
        if time == "BRD":
            return 0
        return int(time)

    def __repr__(self):
        return "%i-car train on %s arriving in %smin to %s (destination is %s)" % (self.cars, self.line, self.time, self.station, self.destination)

class MetrorailStation:
    def __init__(self, api, name, station_code, lines, location):
        self.api = api
        self.name = name
        self.station_code = station_code
        self.location = location
        self._line_codes = lines
        self._cache = {}

    def route(self, other):
        return MetrorailRoute(self.api.rail_system.station_to_station_path(self, other), self.route_meta(other))

    def route_meta(self, other):
        if other in self._cache:
            return self._cache[other]
        data = self.api.get_json(build_url(Service.rail, "jSrcStationToDstStationInfo"),
            FromStationCode=self.station_code, ToStationCode=other.station_code)["StationToStationInfos"][0]
        result = MetrorailRouteMeta(self, other,
            MetrorailCostInformation(data["RailFare"]["PeakTime"], data["RailFare"]["OffPeakTime"],
            data["RailFare"]["SeniorDisabled"]), data["CompositeMiles"], data["RailTime"])
        self._cache[other] = result
        return result

    def trains(self):
        station_codes = [i.station_code for i in self.api.stations.all.values() if i == self]
        data = self.api.get_json(build_url(Service.rail_predictions, "GetPrediction/%s" % ",".join(station_codes)), nocache=True)["Trains"]
        return [MetrorailTrainPrediction(
                    self.api.lines[i["Line"]],
                    self.api.stations[i["DestinationCode"]],
                    self,
                    i["Min"],
                    i["Car"]
                ) for i in data if (
                    i["DestinationCode"] is not None and
                    MetrorailLines._line_valid(i["Line"]) and
                    i["Car"] is not None
                )]

    def _lines(self):
        return {self.api.lines[code] for code in self._line_codes}

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return "%s (%s)" % (self.name, ", ".join(self._line_codes))

    lines = property(_lines)

class MetrorailStations:
    def __init__(self, api):
        self.api = api
        self._cache = {}
        self._raw_json = {}

    def by_name(self, name):
        maybe_data = list(filter(lambda k: k.name.lower() == name.lower(), self.all.values()))
        if maybe_data:
            return maybe_data[0]
        return None

    @staticmethod
    def _lines(data):
        return [data["LineCode%d" % i] for i in range(1, 5) if data["LineCode%d" % i] is not None]

    def _all(self):
        if self._raw_json:
            data = self._raw_json
        else:
            data = self.api.get_json(build_url(Service.rail, "jStations"))["Stations"]
            self._raw_json = data

        for station in data:
            if station["Code"] not in self._cache:
                self._cache[station["Code"]] = MetrorailStation(
                                                    self.api,
                                                    station["Name"],
                                                    station["Code"],
                                                    self._lines(station),
                                                    MetrorailLocation(
                                                        station["Lat"],
                                                        station["Lon"],
                                                        MetrorailAddress(station["Address"])
                                                    )
                                               )

        self._fix_cache()
        return self._cache

    def __getitem__(self, station_code):
        self._fix_cache()
        if station_code in self._cache:
            return self._cache[station_code]

        maybe_data = list(filter(lambda k: k["Code"] == station_code, self._raw_json))
        if len(maybe_data) > 0:
            self._cache[station_code] = MetrorailStation(
                                            self.api,
                                            maybe_data[0]["Name"],
                                            station_code,
                                            self._lines(maybe_data[0]),
                                            MetrorailLocation(
                                                maybe_data[0]["Lat"],
                                                maybe_data[0]["Lon"],
                                                MetrorailAddress(maybe_data[0]["Address"])
                                            )
                                        )

        self._raw_json = self.api.get_json(build_url(Service.rail, "jStations"))["Stations"]
        return self.__getitem__(station_code)

    def _fix_cache(self):
        for name in [i["Name"] for i in filter(lambda k: bool(k["StationTogether1"]), self._raw_json)]:
            stations = [self._cache[station["Code"]] for station in
                    filter(lambda k: k["Name"] == name, self._raw_json) if station["Code"] in self._cache]
            if not stations:
                continue
            all_lines = reduce(operator.or_, [i.lines for i in stations])
            for station in stations:
                station._line_codes = [i.line_code for i in all_lines]

    all = property(_all)

class MetrorailLine:
    def __init__(self, api, friendly_name, line_code, start, end, int_end1, int_end2):
        self.api = api
        self.friendly_name = friendly_name
        self.line_code = line_code
        self.start = start
        self.end = end
        self.path = self._get_path()
        end_codes = []
        end_codes.append(start)
        if int_end1:
            end_codes.append(int_end1)
        if int_end2:
            end_codes.append(int_end2)
        end_codes.append(end)
        self.destination_codes = end_codes

    @property
    def destinations(self):
        return [self.api.stations[code] for code in self.destination_codes] 
    

    def _get_path(self):
        return [i["StationCode"] for i in self.api.get_json(build_url(Service.rail, "jPath"),
            FromStationCode=self.start, ToStationCode=self.end)["Path"]]

    def _stations(self):
        return [self.api.stations[code] for code in self.path]

    def __repr__(self):
        return "%s Line (%s)" % (self.friendly_name, self.line_code)

    stations = property(_stations)

class MetrorailLines:
    def __init__(self, api):
        self.api = api
        self._cache = {}
        self._raw_json = {}


    def _line_valid(line_str):
        if line_str is None or len(line_str) < 2 or line_str == "No":
            return False
        return True

    def _all(self):
        if self._raw_json:
            data = self._raw_json
        else:
            data = self.api.get_json(build_url(Service.rail, "jLines"))["Lines"]
            self._raw_json = data

        for line in data:
            if line["LineCode"] not in self._cache:
                self._cache[line["LineCode"]] = MetrorailLine(
                    self.api,
                    line["DisplayName"],
                    line["LineCode"],
                    line["StartStationCode"],
                    line["EndStationCode"],
                    line["InternalDestination1"],
                    line["InternalDestination2"]
                )

        return self._cache

    def __getitem__(self, line_code):
        if line_code in self._cache:
            return self._cache[line_code]

        maybe_data = list(filter(lambda k: k["LineCode"] == line_code, self._raw_json))
        if len(maybe_data) > 0:
            self._cache[line_code] = MetrorailLine(
                self.api,
                maybe_data[0]["DisplayName"],
                line_code,
                maybe_data[0]["StartStationCode"],
                maybe_data[0]["EndStationCode"],
                maybe_data[0]["InternalDestination1"],
                maybe_data[0]["InternalDestination2"])
            return self._cache[line_code]

        self._raw_json = self.api.get_json(build_url(Service.rail, "jLines"))["Lines"]
        return self.__getitem__(line_code)

    all = property(_all)

class MetrorailSystem:
    def __init__(self, api):
        self.api = api
        self.graph = self._build_graph()

    def _adjacent_stations_on_line(self, line, station):
        position = line.stations.index(station)
        adjacent = []
        if position != 0:
            adjacent.append(line.stations[position - 1])
        if position != len(line.stations) - 1:
            adjacent.append(line.stations[position + 1])
        return adjacent

    def _all_adjacent_stations(self, station):
        adjacent = []
        for line in station.lines:
            adjacent += self._adjacent_stations_on_line(line, station)
        return adjacent

    def _build_graph(self):
        stations = self.api.stations.all.values()
        graph = {}
        for station in stations:
            graph[station] = self._all_adjacent_stations(station)
        return graph

    def _collapse_same_line_stations(self, path):
        if len(path[0].lines & path[-1].lines):
            return [path[0], path[-1]]

        last_transfer = path[0]
        lines = path[0].lines
        collapsed = [path[0]]
        for idx, station in enumerate(path):
            if len(last_transfer.lines & station.lines):
                continue
            last_transfer = path[idx - 1]
            collapsed.append(last_transfer)
        collapsed.append(path[-1])
        return collapsed

    def station_to_station_path(self, start, end):
        closed_set = []
        open_set = {}
        open_set[start] = 0
        parents = {}
        while open_set:
            current = sorted(list(open_set), key=lambda k: open_set[k])[0]
            if current == end:
                break
            closed_set.append(current)
            for neighbor in self.graph[current]:
                if neighbor in closed_set:
                    continue
                if neighbor in open_set and open_set[neighbor] < open_set[current] + 1:
                    continue
                parents[neighbor] = current
                open_set[neighbor] = open_set[current] + 1
            del open_set[current]
        else:
            return False

        path = []
        node = end
        while node != start:
            path.append(node)
            node = parents[node]
        path.append(start)
        path.reverse()
        return self._collapse_same_line_stations(path)

    def predictions(self):
        return sum(list(self.all_trains().values()), [])

    def all_trains(self):
        data = self.api.get_json(build_url(Service.rail_predictions, "GetPrediction/All"), nocache=True)["Trains"]
        result = {}
        for prediction in data:
            if prediction["LocationCode"] is None or prediction["DestinationCode"] is None or prediction["Car"] is None:
                continue
            if self.api.stations[prediction["LocationCode"]] not in result:
                result[self.api.stations[prediction["LocationCode"]]] = []
            result[self.api.stations[prediction["LocationCode"]]].append(
                MetrorailTrainPrediction(
                    self.api.lines[prediction["Line"]],
                    self.api.stations[prediction["DestinationCode"]],
                    self.api.stations[prediction["LocationCode"]],
                    prediction["Min"],
                    prediction["Car"]
                )
            )

        all_stations = self.api.stations.all
        for station in all_stations:
            st = all_stations[station]
            if st not in result:
                result[st] = []
        return result

class MetroApi:
    def __init__(self, api_key, redis_info={}):
        self.api_key = api_key
        if redis_info != {}:
            self.cache = redis.StrictRedis(**redis_info)
        else:
            self.cache = None
        self.lines = MetrorailLines(self)
        self.stations = MetrorailStations(self)
        self.rail_system = MetrorailSystem(self)

    def get_json(self, url, *semi_params, **params):
        params.update(dict(api_key=self.api_key, url=url))
        nocache = "nocache" in params or self.cache is None
        if "nocache" in params: del params["nocache"]

        for i in semi_params: params.update(dict(i="yes"))
        if not nocache:
            data = self._cache_get(params)
            if data:
                return data

        data = requests.get(url, params=params).json()

        if not nocache:
            self._cache(params, data)

        return data

    def _cache(self, params, data):
        key = ",".join(list(map(lambda k: "=".join(k), sorted(params.items()))))
        value = json.dumps(data)
        self.cache.set(key, value)

    def _cache_get(self, params):
        key = ",".join(list(map(lambda k: "=".join(k), sorted(params.items()))))
        value = self.cache.get(key)
        if not value:
            return None
        return json.loads(value.decode("utf-8"))
