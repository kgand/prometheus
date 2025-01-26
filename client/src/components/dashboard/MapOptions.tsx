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
      <div className="w-60 rounded-xl border border-gray-200 bg-white shadow-xl p-5">
        <p className="text-lg font-semibold">Options</p>
        <div className="mt-4">
          <div className="flex items-center gap-4">
            <input
              type="checkbox"
              checked={showWildfires}
              onChange={() => setShowWildfires((prev) => !prev)}
              className="w-4 h-4"
            />
            <p>Show Historical Fires</p>
          </div>
          <div className="flex items-center gap-4 mt-2">
            <input
              type="checkbox"
              checked={showPins}
              onChange={() => setShowPins((prev) => !prev)}
              className="w-4 h-4"
            />
            <p>Show Live Cams</p>
          </div>
        </div>
      </div>
    );
  }
  