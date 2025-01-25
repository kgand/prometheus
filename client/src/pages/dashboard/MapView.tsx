import USMap from "../../components/dashboard/USMap";

export default function MapView() {
  return (
    <div className="h-[calc(100vh-64px)] px-10 py-8">
        <h1 className="text-center text-4xl font-medium">Wildfire Cams Map View</h1>
      <div className="flex w-full h-full items-center justify-center">
        <USMap />
      </div>
    </div>
  );
}
