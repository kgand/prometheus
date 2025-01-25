// @ts-nocheck
import { useState } from "react";
import {
  ComposableMap,
  Geographies,
  Geography,
  Marker,
} from "react-simple-maps";

const USA_TOPO_JSON = "https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json";

const pins = [
  { name: "New York", coordinates: [-74.006, 40.7128] },
  { name: "Los Angeles", coordinates: [-118.2437, 34.0522] },
];

const USMap = () => {
  return (
    <div className="w-full max-w-[900px]">
      <ComposableMap projection="geoAlbersUsa">
        <Geographies geography={USA_TOPO_JSON}>
          {({ geographies }) =>
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
                  hover: { fill: "#d6d6d6", outline: "none" }, // Prevents color change on hover
                  pressed: { fill: "#D6D6D6", outline: "none" }, // Optional, style when clicked
                }}
              />
            ))
          }
        </Geographies>
        {pins.map((pin) => (
          <Pin pin={pin} key={pin.name} />
        ))}
      </ComposableMap>
    </div>
  );
};

const Pin = ({ pin }) => {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <>
      <Marker
        coordinates={pin.coordinates}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        className="relative bg-red-800"
      >
        <circle r={6} fill="#6E1423" className="cursor-pointer"/>
        {isHovered && (
          <text
            textAnchor="middle"
            y={15}
            style={{ fill: "#5D5A6D", paddingTop: "8px" }}
          >
            {pin.name}
          </text>
        )}
      </Marker>
    </>
  );
};

export default USMap;
