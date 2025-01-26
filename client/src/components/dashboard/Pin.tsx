// @ts-nocheck
import { useState } from "react";
import { Marker } from "react-simple-maps";
import { useFireStatus } from "../../services/websocket/client";

const Pin = ({ pin }) => {
  const [isHovered, setIsHovered] = useState(false);
  const fireStatuses = useFireStatus();
  const fireStatus = fireStatuses[pin._id];

  const getPinColor = () => {
    if (fireStatus?.fireDetected) {
      return "#FF0000"; // Red for fire detected
    }
    if (pin.confidence < 34) {
      return "#4ADE80";
    }
    if (pin.confidence >= 34 && pin.confidence < 67) {
      return "#FACC15";
    }
    return "#6E1423";
  };

  return (
    <Marker
      coordinates={pin.coordinates}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      className="relative"
    >
      <circle r={4} fill={getPinColor()} className="cursor-pointer" />
      {isHovered && (
        <text x={5} y={-10} className="txt">
          {pin.name}
          {fireStatus?.fireDetected && " (🔥 Fire Detected!)"}
        </text>
      )}
    </Marker>
  );
};

export default Pin;
