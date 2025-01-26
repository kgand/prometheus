// @ts-nocheck
import { useState } from "react";
import {
  ComposableMap,
  Geographies,
  Geography,
  Marker,
  ZoomableGroup
} from "react-simple-maps";
import { useCams } from "../../hooks/useCams";
import { FaSpinner } from "react-icons/fa";

const USA_TOPO_JSON = "https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json";

const USMap = () => {
  const { data, loading, isError, error } = useCams();

  if (loading) return (
    <div className="pt-20 flex justify-center">
      <span className="animate-spin text-3xl"><FaSpinner/></span>
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
      cam.latitude < 71.538800 &&
      cam.latitude > 51.209300 &&
      cam.longitude < -129.199600 &&
      cam.longitude > -179.148909;
    const isHawaii =
      cam.latitude < 28.402123 && 
      cam.latitude > 18.776344 &&
      cam.longitude < -154.755792 &&
      cam.longitude > -178.443593;

    return isContinentalUS || isAlaska || isHawaii;
  })
  .map((cam) => ({
    name: cam.title || "Unknown",
    coordinates: [cam.longitude, cam.latitude],
    designation: cam.description || "No Description",
  }));


  return (
    <div className="w-full max-w-[900px] cursor-grab ">
      <ComposableMap projection="geoAlbersUsa">
      <ZoomableGroup zoom={1} center={[-96, 40]} minZoom={1} maxZoom={8} className="">
        <Geographies geography={USA_TOPO_JSON}>
          {({ geographies }) => 
            Array.isArray(geographies) ? (
              geographies.map((geo) => (
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
            ) : null
          }
        </Geographies>
       
        {pins.map((pin, index) => (
          <Pin key={index} pin={pin} />
        ))}
         </ZoomableGroup>
      </ComposableMap>
    </div>
  );
};

const Pin = ({ pin }) => {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <Marker
      coordinates={pin.coordinates}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      className="relative"
    >
      <circle r={4} fill="#6E1423" className="cursor-pointer" />
      {isHovered && (
        <text 
          x={5} 
          y={-10} 
          style={{
            fontSize: "1vw", // Adjust size as needed
            backgroundColor: "white",
            padding: "0.2vw",
            borderRadius: "0.5vw",
            boxShadow: "0px 2px 4px rgba(0, 0, 0, 0.2)",
          }}
          className="text-xs bg-white p-1 rounded shadow"
        >
          {pin.name}
        </text>
      )}
    </Marker>
  );
};

export default USMap;