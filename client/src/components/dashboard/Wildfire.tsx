// @ts-nocheck
import { useState } from "react";
import { Marker } from "react-simple-maps";

const Wildfire = ({
    fire,
    minSize,
    maxSize,
    minRadius = 4,
    maxRadius = 20,
  }) => {
    const [isHovered, setIsHovered] = useState(false);
  
    const size = parseInt(fire.properties.size, 10) || 0;
  
    const radius = size
      ? minRadius +
        ((size - minSize) * (maxRadius - minRadius)) / (maxSize - minSize)
      : minRadius;
  
    const opacity = size
      ? 1 - ((size - minSize) / (maxSize - minSize)) * 0.35 // Scale opacity (max 1, min 0.3)
      : 1;
  
    return (
      <Marker
        coordinates={fire.geometry.coordinates}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        className="relative"
      >
        <circle
          r={radius}
          fill="#3B82F6"
          className="cursor-pointer"
          opacity={opacity}
        />
        {isHovered && (
          <text x={5} y={-10} className="txt">
            {fire.properties.title}
          </text>
        )}
      </Marker>
    );
  };

export default Wildfire;