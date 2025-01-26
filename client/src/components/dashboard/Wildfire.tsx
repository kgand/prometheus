// @ts-nocheck
import { useState } from "react";
import { Marker } from "react-simple-maps";
import { motion } from "framer-motion";

const Wildfire = ({
  fire,
  minSize,
  maxSize,
  minRadius = 4,
  maxRadius = 20,
  setSelectedWildfire,
  setShowWildfireModal,
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

  const handleClick = () => {
    setShowWildfireModal(true);
    setSelectedWildfire(fire);
  };

  return (
    <Marker
      coordinates={fire.geometry.coordinates}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      onClick={handleClick}
      className="relative"
    >
      <circle
        r={radius}
        fill="#3B82F6"
        className="cursor-pointer"
        opacity={opacity}
      />
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
          {fire.properties.title}
        </motion.text>
      )}
    </Marker>
  );
};

export default Wildfire;
