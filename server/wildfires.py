import inciweb_wildfires


def get_wildfire_incidents():
    data = inciweb_wildfires.get_incidents()

    wildfires = data["features"]

    for x in wildfires:
        x["properties"]["field_incident_overview"] = ""

    return wildfires
