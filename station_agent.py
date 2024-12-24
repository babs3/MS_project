class Station:

    def __init__(self, station_id, station_name, lat, lng, initial_bike_count=0):
        self.station_id = station_id
        self.station_name = station_name
        self.lat = lat
        self.lng = lng
        self.bike_count = initial_bike_count

    def add_bike(self):
        self.bike_count += 1

    def remove_bike(self):
        if self.bike_count > 0:
            self.bike_count -= 1
        #else:
        #    print(f"[{self.station_name}] No bikes to remove!")

    def log_state(self):
        print(f"  Station {self.station_name} - Bikes: {self.bike_count}")
