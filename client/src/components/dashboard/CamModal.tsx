// @ts-nocheck
import React from "react";
import { FaXmark } from "react-icons/fa6";
import { FaSpinner } from "react-icons/fa";
import useImgById from "../../hooks/useImgById";
import { useWeather } from "../../hooks/useWeather";
import { WiHumidity, WiStrongWind, WiThermometer } from "react-icons/wi";

interface CamData {
  camera_id: string;
  timestamp: string;
  image: string;
}

interface CamModalProps {
  setShowCamModal: (show: boolean) => void;
  selectedCam: CamData | null;
}

const CamModal: React.FC<CamModalProps> = ({
  setShowCamModal,
  selectedCam,
}) => {
  const { data, loading, error } = useImgById(selectedCam?.id || "");
  const { data: weatherData, loading: weatherLoading, error: weatherError } = useWeather(
    selectedCam?.latitude || 0,
    selectedCam?.longitude || 0
  );

  return (
    <div
      className="modal-bg absolute inset-0 z-20 flex items-center justify-center"
      onClick={() => setShowCamModal(false)}
    >
      <div
        className="relative w-[500px] rounded-xl border border-gray-300 bg-white shadow-xl max-h-[600px] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="absolute top-4 right-4 z-30 cursor-pointer p-2 text-xl text-black border border-gray-300 shadow-xl rounded-full bg-white" onClick={() => setShowCamModal(false)}>
          <FaXmark className=""  />
        </div>

        <div className="px-4 py-4">
          {loading ? (
            <p className="text-center text-gray-500">Loading...</p>
          ) : error ? (
            <p className="text-center text-red-500">Error: {error}</p>
          ) : data ? (
            <>
              {data.image && (
                <img
                  src={`data:image/jpeg;base64,${data.image}`}
                  alt="Camera Feed"
                  className="mt-4 max-w-full rounded-lg border border-gray-200 shadow-sm"
                />
              )}
              <div className="flex items-center justify-between gap-4 pt-4">
                <p className="text-xl font-semibold">{selectedCam?.name}</p>
                <p className="min-w-32 font-medium">
                  Fire Confidence: {selectedCam.confidence.toFixed(2)}%{" "}
                </p>
              </div>
              <p className="pt-2">{selectedCam.description}</p>

              {/* Weather Information */}
              <div className="mt-4 rounded-lg border border-gray-200 bg-gray-50 p-4">
                {weatherLoading ? (
                  <div className="flex justify-center py-4">
                    <FaSpinner className="animate-spin text-2xl text-gray-500" />
                  </div>
                ) : weatherError ? (
                  <p className="text-center text-red-500">Failed to load weather data</p>
                ) : weatherData && weatherData.main ? (
                  <>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <img 
                          src={`http://openweathermap.org/img/w/${weatherData.weather[0].icon}.png`}
                          alt={weatherData.weather[0].description}
                          className="h-12 w-12"
                        />
                        <div>
                          <p className="text-lg font-medium">{weatherData.weather[0].main}</p>
                          <p className="text-sm text-gray-600 capitalize">{weatherData.weather[0].description}</p>
                        </div>
                      </div>
                    </div>
                    <div className="mt-3 grid grid-cols-3 gap-4">
                      <div className="flex items-center gap-2">
                        <WiThermometer className="text-2xl text-gray-600" />
                        <div>
                          <p className="text-sm text-gray-600">Temperature</p>
                          <p className="font-medium">{Math.round(weatherData.main.temp)}°C</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <WiHumidity className="text-2xl text-gray-600" />
                        <div>
                          <p className="text-sm text-gray-600">Humidity</p>
                          <p className="font-medium">{weatherData.main.humidity}%</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <WiStrongWind className="text-2xl text-gray-600" />
                        <div>
                          <p className="text-sm text-gray-600">Wind Speed</p>
                          <p className="font-medium">{weatherData.wind.speed} m/s</p>
                        </div>
                      </div>
                    </div>
                  </>
                ) : (
                  <p className="text-center text-gray-500">No weather data available</p>
                )}
              </div>
            </>
          ) : (
            <p className="text-center text-gray-500">
              No camera data available.
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default CamModal;
