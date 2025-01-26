type Wildfire = {
  type: "Feature";
  geometry: {
    type: "Point";
    coordinates: [number, number];
  };
  properties: {
    title: string;
    lat_deg: string;
    long_deg: string;
    field_percent_of_perimeter: string;
    type: string;
    field_incident_description: string;
    field_active: string;
    created: string;
    id: string;
    field_incident_overview: string;
    size: string;
    lat_min: string;
    lat_sec: string;
    urlPath: string;
    long_min: string;
    long_sec: string;
    measurement_type: string;
    field_title_and_unit: string;
    changed: string;
    field_unit_code: string;
  };
};

export default Wildfire