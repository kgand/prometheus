import { useState, useEffect } from "react";

interface CameraData {
  camera_id: string;
  timestamp: string;
  image: string; 
}

const useImgById = (id: string) => {
  const [data, setData] = useState<CameraData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchImageData = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(`http://localhost:8000/camera?id=${id}`);
        if (!response.ok) {
          throw new Error(`Error fetching data: ${response.statusText}`);
        }
        const result: CameraData = await response.json();
        setData(result);
      } catch (err: unknown) {
        setError((err as Error).message || "Unknown error occurred");
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchImageData();
    }
  }, [id]);

  return { data, loading, error };
};

export default useImgById;
