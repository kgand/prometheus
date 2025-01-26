import { useState, useEffect } from "react";

interface WeatherData {
  main: {
    temp: number;
    humidity: number;
    feels_like: number;
  };
  weather: Array<{
    main: string;
    description: string;
    icon: string;
  }>;
  wind: {
    speed: number;
  };
}

export const useWeather = (lat: number, lon: number) => {
  const [data, setData] = useState<WeatherData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchWeather = async () => {
      if (!lat || !lon) return;
      
      setLoading(true);
      setError(null);

      try {
        const response = await fetch(`http://localhost:8000/weather?lat=${lat}&lon=${lon}`);
        if (!response.ok) {
          throw new Error(`Failed to fetch weather: ${response.statusText}`);
        }

        const weatherData: WeatherData = await response.json();
        setData(weatherData);
      } catch (err: any) {
        setError(err.message || "Unknown error occurred");
      } finally {
        setLoading(false);
      }
    };

    fetchWeather();
  }, [lat, lon]);

  return { data, loading, error };
}; 