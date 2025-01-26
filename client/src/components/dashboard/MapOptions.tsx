type MapOptionsProps = {
  setShowPins: React.Dispatch<React.SetStateAction<boolean>>;
  setShowWildfires: React.Dispatch<React.SetStateAction<boolean>>;
  showPins: boolean;
  showWildfires: boolean;
};

export default function MapOptions({
  setShowPins,
  setShowWildfires,
  showPins,
  showWildfires,
}: MapOptionsProps) {
  return (
    <div className="w-60 rounded-xl border border-gray-200 bg-white p-5 shadow-xl">
      <p className="text-lg font-semibold">Options</p>
      <div className="mt-4">
        <div className="flex items-center gap-4">
          <input
            type="checkbox"
            checked={showWildfires}
            onChange={() => setShowWildfires((prev) => !prev)}
            className="h-4 w-4"
          />
          <p>Show Historical Fires</p>
        </div>
        <div className="mt-2 flex items-center gap-4">
          <input
            type="checkbox"
            checked={showPins}
            onChange={() => setShowPins((prev) => !prev)}
            className="h-4 w-4"
          />
          <p>Show Live Cams</p>
        </div>
        <div className="mt-4 font-semibold">Legend</div>
        <p className="mt-4">Live Cam Fire Confidence:</p>
        <div className="grid gap-2 pt-2">
          <p className="flex items-center gap-2.5">
            <span className="h-4 w-4 rounded-full bg-green-400" /> 0-33
          </p>
          <p className="flex items-center gap-2.5">
            <span className="h-4 w-4 rounded-full bg-yellow-400" /> 34-66
          </p>
          <p className="flex items-center gap-2.5">
            <span className="h-4 w-4 rounded-full bg-red-800" /> 67-100
          </p>
        </div>
        <div className="mt-4 flex items-center gap-2">
          Historical Fires:{" "}
          <span className="h-4 w-4 rounded-full bg-blue-500" />
        </div>
        <p className="pt-2">Bigger circle = larger fire</p>
      </div>
    </div>
  );
}
