import { useState } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import axios from "axios";
import { useUserCams } from "../../hooks/useCams";
import { FaPlus, FaLock } from "react-icons/fa";

interface AddCameraForm {
  ip_address: string;
  latitude: number;
  longitude: number;
}

export default function YourCams() {
  const { user, isAuthenticated, loginWithRedirect } = useAuth0();
  const { data: cameras, loading, error } = useUserCams();
  const [showAddForm, setShowAddForm] = useState(false);
  const [formData, setFormData] = useState<AddCameraForm>({
    ip_address: "",
    latitude: 0,
    longitude: 0,
  });

  const handleAddCamera = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axios.post("http://localhost:8000/addcam", {
        ...formData,
        email: user?.email,
        name: `Camera at ${formData.latitude}, ${formData.longitude}`,
      });
      setShowAddForm(false);
      setFormData({ ip_address: "", latitude: 0, longitude: 0 });
      window.location.reload();
    } catch (error) {
      console.error("Error adding camera:", error);
    }
  };

  const handleCameraClick = () => {
    if (!isAuthenticated) {
      loginWithRedirect();
    }
  };

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

  // Filter cameras based on authentication
  const displayCameras = isAuthenticated ? cameras.filter(cam => cam.email === user?.email) : cameras;

  return (
    <div className="p-6">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Your Cameras</h1>
          {!isAuthenticated && (
            <p className="mt-2 text-gray-600">Sign in to manage these cameras or add your own</p>
          )}
        </div>
        {isAuthenticated ? (
          <button
            onClick={() => setShowAddForm(true)}
            className="flex items-center gap-2 rounded-lg bg-red-800 px-4 py-2 text-white hover:bg-red-900"
          >
            <FaPlus /> Add Camera
          </button>
        ) : (
          <button
            onClick={() => loginWithRedirect()}
            className="flex items-center gap-2 rounded-lg bg-red-800 px-4 py-2 text-white hover:bg-red-900"
          >
            <FaLock /> Sign in to Add Camera
          </button>
        )}
      </div>

      {showAddForm && isAuthenticated && (
        <div className="mb-6 rounded-lg border border-gray-200 p-4">
          <h2 className="mb-4 text-xl font-semibold">Add New Camera</h2>
          <form onSubmit={handleAddCamera} className="grid gap-4">
            <div>
              <label className="mb-1 block">IP Address</label>
              <input
                type="text"
                value={formData.ip_address}
                onChange={(e) =>
                  setFormData({ ...formData, ip_address: e.target.value })
                }
                className="w-full rounded-lg border border-gray-300 p-2"
                required
              />
            </div>
            <div>
              <label className="mb-1 block">Latitude</label>
              <input
                type="number"
                step="any"
                value={formData.latitude}
                onChange={(e) =>
                  setFormData({ ...formData, latitude: parseFloat(e.target.value) })
                }
                className="w-full rounded-lg border border-gray-300 p-2"
                required
              />
            </div>
            <div>
              <label className="mb-1 block">Longitude</label>
              <input
                type="number"
                step="any"
                value={formData.longitude}
                onChange={(e) =>
                  setFormData({ ...formData, longitude: parseFloat(e.target.value) })
                }
                className="w-full rounded-lg border border-gray-300 p-2"
                required
              />
            </div>
            <div className="flex gap-2">
              <button
                type="submit"
                className="rounded-lg bg-red-800 px-4 py-2 text-white hover:bg-red-900"
              >
                Add Camera
              </button>
              <button
                type="button"
                onClick={() => setShowAddForm(false)}
                className="rounded-lg bg-gray-500 px-4 py-2 text-white hover:bg-gray-600"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {displayCameras.map((camera) => (
          <div
            key={camera._id}
            className={`relative rounded-lg border border-gray-200 p-4 shadow-sm ${
              !isAuthenticated ? "cursor-pointer hover:shadow-md" : ""
            }`}
            onClick={!isAuthenticated ? handleCameraClick : undefined}
          >
            {!isAuthenticated && (
              <div className="absolute top-2 right-2">
                <FaLock className="text-gray-400" />
              </div>
            )}
            <h3 className="mb-2 text-lg font-semibold">{camera.name}</h3>
            <p>IP: {camera.ip_address}</p>
            <p>Status: {camera.status}</p>
            <p>Location: {camera.latitude}, {camera.longitude}</p>
            <p>Last Connected: {new Date(camera.last_connected).toLocaleString()}</p>
            {camera.fire_detected && (
              <p className="mt-2 text-red-500">⚠️ Fire Detected!</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
} 