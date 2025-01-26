// @ts-nocheck
import React, { useEffect } from "react";
import { FaXmark } from "react-icons/fa6";
import useImgById from "../../hooks/useImgById";
import { FaSpinner } from "react-icons/fa";
import { motion } from "framer-motion";

interface CamData {
  camera_id: string;
  timestamp: string;
  image: string;
}

interface CamModalProps {
  setShowCamModal: (show: boolean) => void;
  selectedCam: CamData | null;
}

const CamModal: React.FC<CamModalProps> = ({
  setShowCamModal,
  selectedCam,
}) => {
  const { data, loading, error } = useImgById(selectedCam?.id || "");

  if (loading) {
    return (
      <div
        className="modal-bg fixed inset-0 z-20 flex items-center justify-center"
        onClick={() => setShowCamModal(false)}
      >
        <span className="text-3xl animate-spin duration-200 text-white">
          <FaSpinner />
        </span>
      </div>
    );
  }

  return (
    <div
      className="modal-bg fixed inset-0 z-20 flex items-center justify-center"
      onClick={() => setShowCamModal(false)}
    >
      <motion.div
        className="relative w-[500px] rounded-xl border border-gray-300 bg-white shadow-xl max-h-[600px] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
        initial={{ opacity: 0, y: -50 }} // Initial state: invisible and shifted upward
        animate={{ opacity: 1, y: 0 }} // Visible and positioned at the center
        exit={{ opacity: 0, y: -50 }} // Exit state: invisible and shifted upward
        transition={{ duration: 0.3, ease: "easeInOut" }} // Smooth transition
      >
        <div
          className="absolute top-4 right-4 z-30 cursor-pointer p-2 text-xl text-black border border-gray-300 shadow-xl rounded-full bg-white"
          onClick={() => setShowCamModal(false)}
        >
          <FaXmark className="" />
        </div>

        <div className="px-4 py-4">
          {loading ? (
            <p className="text-center text-gray-500">Loading...</p>
          ) : error ? (
            <p className="text-center text-red-500">Error: {error}</p>
          ) : data ? (
            <>
              {data.image && (
                <img
                  src={`data:image/jpeg;base64,${data.image}`}
                  alt="Camera Feed"
                  className="mt-4 max-w-full rounded-lg border border-gray-200 shadow-sm"
                />
              )}
              <div className="flex items-center justify-between gap-4 pt-4">
                <p className="text-xl font-semibold">{selectedCam?.name}</p>
                <p className="min-w-32 font-medium">
                  Fire Confidence: {selectedCam.confidence.toFixed(2)}%{" "}
                </p>
              </div>
              <p className="pt-2">{selectedCam.description}</p>
            </>
          ) : (
            <p className="text-center text-gray-500">
              No camera data available.
            </p>
          )}
        </div>
      </motion.div>
    </div>
  );
};

export default CamModal;
