import USMap from "../../components/dashboard/USMap";

export default function MapView() {
  return (
    <div className="min-h-[calc(100vh-64px)] px-10 py-8 w-full overflow-y-scroll">
      <h1 className="text-center text-4xl font-medium">
        Wildfire Cams Map View
      </h1>
      <div className="flex mx-auto pt-4 justify-center gap-5">
        <p>Likelihood of fire:</p>
        <p className="flex items-center gap-2.5"><span className="bg-green-400 rounded-full w-4 h-4"/> 0-33</p>
        <p className="flex items-center gap-2.5"><span className="bg-yellow-400 rounded-full w-4 h-4"/> 34-66</p>
        <p className="flex items-center gap-2.5"><span className="bg-red-800 rounded-full w-4 h-4"/> 67-100</p>
      </div>
      <div className="flex h-full w-full items-center justify-center pt-8">
        <USMap />
      </div>
    </div>
  );
}
