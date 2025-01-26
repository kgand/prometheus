import { useState, useEffect } from "react";

type WildfireFeature = {
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

type WildfiresResponse = {
  type: "FeatureCollection";
  features: WildfireFeature[];
};

export const useWildfires = () => {
  const [data, setData] = useState<WildfiresResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchWildfires = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await fetch("http://localhost:8000/wildfires");
        if (!response.ok) {
          throw new Error(`Failed to fetch: ${response.statusText}`);
        }

        const data: WildfiresResponse = await response.json();
        setData(data);
      } catch (err: any) {
        setError(err.message || "Unknown error occurred");
      } finally {
        setLoading(false);
      }
    };

    fetchWildfires();
  }, []);

  return { data, loading, error };
};
