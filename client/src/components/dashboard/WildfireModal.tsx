// @ts-nocheck
import React from "react";
import { FaXmark } from "react-icons/fa6";
import { motion } from "framer-motion";

const WildfireModal = ({ setShowWildfireModal, selectedWildfire }) => {

  return (
    <div
      className="modal-bg absolute inset-0 z-20 flex items-center justify-center"
      onClick={() => setShowWildfireModal(false)}
    >
      <motion.div
        className="relative max-h-[600px] w-[500px] overflow-y-auto rounded-xl border border-gray-300 bg-white shadow-x cs-scroll"
        onClick={(e) => e.stopPropagation()}
        initial={{ opacity: 0, y: -50 }} // Modal starts invisible and slightly above
        animate={{ opacity: 1, y: 0 }} // Modal fades in and slides to its position
        exit={{ opacity: 0, y: -50 }} // Modal fades out and slides up
        transition={{ duration: 0.3, ease: "easeInOut" }} // Smooth animation
      >
        <div
          className="absolute top-4 right-4 z-30 cursor-pointer rounded-full border border-gray-300 bg-white p-2 text-xl text-black shadow-xl"
          onClick={() => setShowWildfireModal(false)}
        >
          <FaXmark />
        </div>

        <div className="px-4 py-4">
          <p className="text-2xl"> {selectedWildfire.properties.title}</p>
          <p className="pt-2">Size: {selectedWildfire.properties.size} acres</p>
          <p
            className="pt-2"
            dangerouslySetInnerHTML={{
              __html: selectedWildfire.properties.field_incident_overview,
            }}
          ></p>
        </div>
      </motion.div>
    </div>
  );
};

export default WildfireModal;
