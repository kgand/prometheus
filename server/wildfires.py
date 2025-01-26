import inciweb_wildfires


def get_wildfire_incidents():
    data = inciweb_wildfires.get_incidents()

    wildfires = data["features"]


    return wildfires
