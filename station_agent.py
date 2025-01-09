class Station:
    def __init__(self, station_id, station_name, lat, lng, initial_bike_count=0, capacity=15):
        self.station_id = station_id
        self.station_name = station_name
        self.lat = lat
        self.lng = lng
        self.bike_count = initial_bike_count
        self.capacity = capacity

    def add_bike(self):
        self.bike_count += 1
        #if self.bike_count < self.capacity:
        #    self.bike_count += 1
        #    self.log_state()
        #else:
        #    print(f"[{self.station_name}] Station is full!")

    def remove_bike(self):
        if self.bike_count > 0:
            self.bike_count -= 1
        else:
            print(f"[{self.station_name}] No bikes to remove!")

    def get_availability_rate(self):
        return self.bike_count / self.capacity if self.capacity > 0 else 0

    def log_state(self):
        print(f"Station {self.station_name} - Bikes: {self.bike_count}/{self.capacity}")
