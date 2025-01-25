import { useState, useEffect } from "react";
import axios from "axios";

// Types
interface RelatedPark {
  states: string;
  parkCode: string;
  designation: string;
  fullName: string;
  url: string;
  name: string;
}

interface CamData {
  _id: string;
  id: string;
  url: string;
  title: string;
  description: string;
  images: string[];
  relatedParks: RelatedPark[];
  status: string;
  statusMessage: string;
  isStreaming: boolean;
  tags: string[];
  latitude: number;
  longitude: number;
  geometryPoiId: string;
  credit: string;
}

export const useCams = () => {
  const [data, setData] = useState<CamData[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [isError, setIsError] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCams = async () => {
      setLoading(true);
      setIsError(false);
      setError(null);

      try {
        const response = await axios.get<CamData[]>("http://localhost:8000/allcams");
        setData(response.data.slice(1));
      } catch (err) {
        setIsError(true);
        if (axios.isAxiosError(err)) {
          setError(err.message);
        } else {
          setError("An unexpected error occurred.");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchCams();
  }, []);

  return { data, loading, isError, error };
};
