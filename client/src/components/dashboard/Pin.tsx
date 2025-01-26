// @ts-nocheck
import { useState } from "react";
import { Marker } from "react-simple-maps";

const Pin = ({ pin }) => {
  const [isHovered, setIsHovered] = useState(false);

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

export default Pin;
