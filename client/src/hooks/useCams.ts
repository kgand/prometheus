import { useState, useEffect } from "react";
import axios from "axios";
import CamData from "../types/Cam";

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
        setData(response.data);
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

export const useUserCams = () => {
  const [data, setData] = useState<CamData[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [isError, setIsError] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUserCams = async () => {
      setLoading(true);
      setIsError(false);
      setError(null);

      try {
        const response = await axios.get<CamData[]>("http://localhost:8000/usercams");
        setData(response.data);
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

    fetchUserCams();
  }, []);

  return { data, loading, isError, error };
};
