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

const USA_TOPO_JSON = "https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json";

const USMap = () => {
  const { data, loading, isError, error } = useCams();

  const [zoomLevel, setZoomLevel] = useState(1); // State to store zoom level
  const [center, setCenter] = useState([-96, 40]); // State to store the map center

  useEffect(() => {
    document.documentElement.style.setProperty("--zoom", zoomLevel.toString());
  }, [zoomLevel]);

  if (loading)
    return (
      <div className="flex justify-center pt-20">
        <span className="animate-spin text-3xl">
          <FaSpinner />
        </span>
      </div>
    );

  if (isError) return <p>Error loading data: {error}</p>;

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
    console.log("Current zoom level:", zoom, "Center:", coordinates);
  };

  const resetCenter = () => {
    setCenter([-96, 40]);
    setZoomLevel(1);
  };

  return (
    <div className="relative h-full w-full flex justify-center">
      <button
        className="absolute right-2 bottom-2 rounded-lg bg-[#cacaca] p-3 text-white shadow-lg cursor-pointer"
        onClick={resetCenter}
      >
       <IoReload className="text-xl text-[#404040]"/>
      </button>
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
            onMoveEnd={handleMoveEnd} // Track zoom and center changes
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

            {pins.map((pin, index) => (
              <Pin key={index} pin={pin} />
            ))}
          </ZoomableGroup>
        </ComposableMap>
      </div>
    </div>
  );
};

const Pin = ({ pin }) => {
  const [isHovered, setIsHovered] = useState(false);
  console.log(pin.confidence);

  return (
    <Marker
      coordinates={pin.coordinates}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      className="relative"
    >
      {pin.confidence < 34 && (
        <circle r={4} fill="#4ADE80" className="cursor-pointer" />
      )}
      {pin.confidence >= 34 && pin.confidence < 67 && (
        <circle r={4} fill="#FACC15" className="cursor-pointer" />
      )}
      {pin.confidence > 67 && (
        <circle r={4} fill="#6E1423" className="cursor-pointer" />
      )}
      {isHovered && (
        <text x={5} y={-10} className="txt">
          {pin.name}
        </text>
      )}
    </Marker>
  );
};

export default USMap;
