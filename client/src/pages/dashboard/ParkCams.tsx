import { useState } from "react";
import { useCams } from "../../hooks/useCams";
import CamModal from "../../components/dashboard/CamModal";

export default function ParkCams() {
  const { data: cameras, loading, error } = useCams();
  const [selectedCam, setSelectedCam] = useState<any>(null);
  const [showCamModal, setShowCamModal] = useState(false);

  // Filter out user cameras (those without NPS data)
  const parkCameras = cameras.filter(cam => cam.url?.startsWith("https://www.nps.gov/media/webcam"));

  if (loading) {
    return (
      <div className="flex h-full items-center justify-center">
        <p className="text-lg">Loading cameras...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex h-full items-center justify-center">
        <p className="text-lg text-red-500">Error loading cameras</p>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold">National Park Cameras</h1>
        <p className="text-gray-600 mt-2">Live feeds from National Parks across the United States</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {parkCameras.map((camera) => (
          <div
            key={camera._id}
            className="rounded-lg border border-gray-200 p-4 shadow-sm hover:shadow-md transition-shadow cursor-pointer"
            onClick={() => {
              setSelectedCam(camera);
              setShowCamModal(true);
            }}
          >
            <h3 className="mb-2 text-lg font-semibold">{camera.title}</h3>
            <p className="text-sm text-gray-600 mb-2">{camera.relatedParks[0]?.fullName}</p>
            <p className="text-sm">Location: {camera.latitude.toFixed(3)}, {camera.longitude.toFixed(3)}</p>
            <p className="text-sm">Status: {camera.status}</p>
          </div>
        ))}
      </div>

      {showCamModal && selectedCam && (
        <CamModal
          setShowCamModal={setShowCamModal}
          selectedCam={selectedCam}
        />
      )}
    </div>
  );
}
