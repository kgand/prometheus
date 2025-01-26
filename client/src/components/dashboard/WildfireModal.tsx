// @ts-nocheck
import React, { useEffect } from "react";
import { FaXmark } from "react-icons/fa6";
import useImgById from "../../hooks/useImgById";

const WildfireModal = ({ setShowWildfireModal, selectedWildfire }) => {
  console.log(selectedWildfire);

  return (
    <div
      className="modal-bg absolute inset-0 z-20 flex items-center justify-center"
      onClick={() => setShowWildfireModal(false)}
    >
      <div
        className="relative max-h-[400px] w-[500px] overflow-y-auto rounded-xl border border-gray-300 bg-white shadow-xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div
          className="absolute top-4 right-4 z-30 cursor-pointer rounded-full border border-gray-300 bg-white p-2 text-xl text-black shadow-xl"
          onClick={() => setShowWildfireModal(false)}
        >
          <FaXmark className="" />
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
      </div>
    </div>
  );
};

export default WildfireModal;
