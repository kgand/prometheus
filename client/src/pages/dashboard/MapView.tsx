import USMap from "../../components/dashboard/USMap";

export default function MapView() {
  return (
    <div className="min-h-[calc(100vh-64px)] w-full overflow-y-scroll px-10 py-8">
      <h1 className="text-center text-4xl font-medium">
        Wildfire Cams Map View
      </h1>

      <p className="pt-4 text-center text-sm">
        Click a pin for more information.
      </p>
      <div className="flex h-full w-full items-center justify-center overflow-x-hidden mt-4">
        <USMap />
      </div>
    </div>
  );
}
