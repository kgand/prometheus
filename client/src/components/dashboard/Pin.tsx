// @ts-nocheck
import { useState } from "react";
import { Marker } from "react-simple-maps";
import { useFireStatus } from "../../services/websocket/client";
import { motion } from "framer-motion";

const Pin = ({ pin, setSelectedCam, setShowCamModal }) => {
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

  const handleClick = () => {
    setShowCamModal(true);
    setSelectedCam(pin);
  };

  return (
    <>
      <Marker
        coordinates={pin.coordinates}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        onClick={handleClick}
        className="relative"
      >
        <circle r={4} fill={getPinColor()} className="cursor-pointer" />
        {isHovered && (
          <motion.text
            x={5}
            y={-10}
            className="txt"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.3 }}
          >
            {pin.name}
            {fireStatus?.fireDetected && " (🔥 Fire Detected!)"}
          </motion.text>
        )}
      </Marker>
    </>
  );
};

export default Pin;
