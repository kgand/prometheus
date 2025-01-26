// @ts-nocheck
import { useState, useEffect } from "react";
import {
  ComposableMap,
  Geographies,
  Geography,
  Marker,
  ZoomableGroup,
} from "react-simple-maps";
import { useCams } from "../../hooks/useCams";
import { FaSpinner } from "react-icons/fa";
import { IoReload } from "react-icons/io5";
import { useWildfires } from "../../hooks/useWildfires";
import { useFireStatus } from "../../services/websocket/client";
import Pin from "./Pin";
import Wildfire from "./Wildfire";
import MapOptions from "./MapOptions";

const USA_TOPO_JSON = "https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json";

const USMap = () => {
  const { data, loading, isError, error } = useCams();
  const {
    data: wildfires,
    loading: firesLoading,
    error: fireError,
  } = useWildfires();
  const fireStatuses = useFireStatus();

  const [zoomLevel, setZoomLevel] = useState(1);
  const [center, setCenter] = useState([-96, 40]);
  const [showPins, setShowPins] = useState<boolean>(true);
  const [showWildfires, setShowWildfires] = useState<boolean>(true);

  // Get active fire locations from fireStatuses
  const activeFirePins = Object.values(fireStatuses)
    .filter(status => status.fireDetected && status.location)
    .map(status => ({
      coordinates: [status.location.lng, status.location.lat],
      cameraId: status.cameraId
    }));

  useEffect(() => {
    document.documentElement.style.setProperty("--zoom", zoomLevel.toString());
  }, [zoomLevel]);

  if (loading || firesLoading)
    return (
      <div className="flex justify-center pt-20">
        <span className="animate-spin text-3xl">
          <FaSpinner />
        </span>
      </div>
    );

  if (isError || fireError) return <p>Error loading data: {error}</p>;

  const pins = data
    .filter((cam) => {
      const isContinentalUS =
        cam.latitude < 49.384358 &&
        cam.latitude > 24.396308 &&
        cam.longitude < -66.93457 &&
        cam.longitude > -125;
      const isAlaska =
        cam.latitude < 71.5388 &&
        cam.latitude > 51.2093 &&
        cam.longitude < -129.1996 &&
        cam.longitude > -179.148909;
      const isHawaii =
        cam.latitude < 28.402123 &&
        cam.latitude > 18.776344 &&
        cam.longitude < -154.755792 &&
        cam.longitude > -178.443593;

      return isContinentalUS || isAlaska || isHawaii;
    })
    .map((cam) => ({
      ...cam,
      name: cam.title || "Unknown",
      coordinates: [cam.longitude, cam.latitude],
      designation: cam.description || "No Description",
    }));

  const handleMoveEnd = ({ zoom, coordinates }) => {
    setZoomLevel(zoom);
    setCenter(coordinates);
  };

  const resetCenter = () => {
    setCenter([-96, 40]);
    setZoomLevel(1);
  };

  const wildfireSizes = wildfires.map(
    (wf) => parseInt(wf.properties.size, 10) || 0,
  );
  const minSize = Math.min(...wildfireSizes);
  const maxSize = Math.max(...wildfireSizes);

  return (
    <div className="relative flex h-full w-full justify-center">
      <div className="absolute right-2 bottom-2 flex flex-col items-end gap-4">
        <button
          className="cursor-pointer rounded-lg bg-[#cacaca] p-3 text-white shadow-lg"
          onClick={resetCenter}
        >
          <IoReload className="text-xl text-[#404040]" />
        </button>
        <MapOptions
          showPins={showPins}
          setShowPins={setShowPins}
          showWildfires={showWildfires}
          setShowWildfires={setShowWildfires}
        />
      </div>
      <div className="h-full w-full max-w-[900px] cursor-grab pt-4">
        <ComposableMap
          projection="geoAlbersUsa"
          style={{ overflow: "visible" }}
        >
          <ZoomableGroup
            zoom={zoomLevel}
            center={center}
            minZoom={1}
            maxZoom={8}
            onMoveEnd={handleMoveEnd}
          >
            <Geographies geography={USA_TOPO_JSON}>
              {({ geographies }) =>
                Array.isArray(geographies)
                  ? geographies.map((geo) => (
                      <Geography
                        key={geo.rsmKey}
                        geography={geo}
                        style={{
                          default: {
                            fill: "#d6d6d6",
                            outline: "none",
                            stroke: "#f1f1f1",
                            strokeWidth: 0.5,
                          },
                          hover: { fill: "#d6d6d6", outline: "none" },
                          pressed: { fill: "#D6D6D6", outline: "none" },
                        }}
                      />
                    ))
                  : null
              }
            </Geographies>

            {/* Dynamic fire pins */}
            {activeFirePins.map((firePin) => (
              <Marker key={firePin.cameraId} coordinates={firePin.coordinates}>
                <circle r={6} fill="#FF0000" className="cursor-pointer animate-pulse" />
                <circle r={12} fill="#FF0000" fillOpacity={0.3} className="cursor-pointer animate-ping" />
              </Marker>
            ))}

            {showPins && (
              <>
                {pins.map((pin, index) => (
                  <Pin key={index} pin={pin} />
                ))}
              </>
            )}

            {showWildfires && (
              <>
                {wildfires.map((fire) => (
                  <Wildfire
                    key={fire.properties.id}
                    fire={fire}
                    minSize={minSize}
                    maxSize={maxSize}
                  />
                ))}
              </>
            )}
          </ZoomableGroup>
        </ComposableMap>
      </div>
    </div>
  );
};

export default USMap;
