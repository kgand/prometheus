import { useState, useEffect } from "react";
import Wildfire from "../types/Wildfire";


type WildfiresResponse = {
  type: "FeatureCollection";
  features: Wildfire[];
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
