// @ts-nocheck
import { FaCamera, FaGithub, FaMapMarked, FaUser } from "react-icons/fa";
import { FiChevronsLeft } from "react-icons/fi";
import { MdFireTruck, MdLogin, MdPark } from "react-icons/md";
import { PiSirenFill } from "react-icons/pi";
import { SiGoogledocs } from "react-icons/si";
import { ComposableMap, Geographies, Geography } from "react-simple-maps";

export const LandingImg: React.FC = ({}) => {
  const geoUrl = "https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json";
  return (
    <div className="flex">
      <div className="sticky top-0 h-screen max-h-screen min-w-48 overflow-y-auto bg-gray-50">
        <div className="py-6 text-xs">
          <div className="border-b border-gray-300 px-6 pb-3">
            <p className="flex items-center overflow-x-hidden text-lg font-semibold whitespace-nowrap">
              <MdFireTruck className="text-red-800" />
              <span className="pl-2.5">Prometheus</span>
            </p>
            <div className="flex items-end justify-between pt-6">
              <p className="text-sm font-medium">Dashboard</p>
              <div className="flex gap-2">
                <div className="group flex h-6 w-6 cursor-pointer items-center justify-center rounded-lg bg-gray-300 transition-all hover:bg-gray-400">
                  <FiChevronsLeft className="text-gray-600 group-hover:text-gray-700" />
                </div>
              </div>
            </div>
          </div>
          <div className="border-b border-gray-300 px-3 pt-4 pb-3">
            <p className="px-3 font-medium text-[#808080]">Views</p>
            <ul className="mt-2 grid gap-1 text-[#404040]">
              <div className="flex cursor-pointer items-center gap-2 overflow-x-hidden rounded-md px-3 py-1 whitespace-nowrap transition-all hover:bg-gray-200">
                <FaMapMarked /> Map View
              </div>
              <div className="flex cursor-pointer items-center gap-2 overflow-x-hidden rounded-md px-3 py-1 whitespace-nowrap transition-all hover:bg-gray-200">
                <MdPark /> Park Cams
              </div>
              <div className="flex cursor-pointer items-center gap-2 overflow-x-hidden rounded-md px-3 py-1 whitespace-nowrap transition-all hover:bg-gray-200">
                <FaCamera /> Your Cams
              </div>
              <div className="flex cursor-pointer items-center gap-2 overflow-x-hidden rounded-md px-3 py-1 whitespace-nowrap transition-all hover:bg-gray-200">
                <PiSirenFill /> Alerts
              </div>
            </ul>
          </div>
          <div className="border-b border-gray-300 px-3 pt-4 pb-3">
            <p className="px-3 font-medium text-[#808080]">Account</p>
            <ul className="mt-2 grid gap-1 text-[#404040]">
              <div className="flex cursor-pointer items-center gap-2 overflow-x-hidden rounded-md px-3 py-1 whitespace-nowrap transition-all hover:bg-gray-200">
                <MdLogin /> Sign In
              </div>
              <div className="flex cursor-pointer items-center gap-2 overflow-x-hidden rounded-md px-3 py-1 whitespace-nowrap transition-all hover:bg-gray-200">
                <FaUser /> Account Details
              </div>
            </ul>
          </div>
          <div className="border-b border-gray-300 px-3 pt-4 pb-3">
            <p className="px-3 font-medium text-[#808080]">Developers</p>
            <ul className="mt-2 grid gap-1 text-[#404040]">
              <div className="flex cursor-pointer items-center gap-2 overflow-x-hidden rounded-md px-3 py-1 whitespace-nowrap transition-all hover:bg-gray-200">
                <SiGoogledocs /> Documentation
              </div>
              <div className="flex cursor-pointer items-center gap-2 overflow-x-hidden rounded-md px-3 py-1 whitespace-nowrap transition-all hover:bg-gray-200">
                <FaGithub /> Source Code
              </div>
            </ul>
          </div>
        </div>
      </div>
      <div className="flex w-full flex-col py-8">
        <p className="text-center text-2xl opacity-60">View Live Cams</p>
        <p className="pt-2 text-center opacity-60">
          View live fire detection across the USA{" "}
        </p>
        <div className="px-12 pt-12">
          <ComposableMap
            projection="geoAlbersUsa" // Projection for USA
            width={800}
            height={500}
          >
            <Geographies geography={geoUrl}>
              {({ geographies }) =>
                geographies.map((geo) => (
                  <Geography
                    key={geo.rsmKey}
                    geography={geo}
                    style={{
                      default: {
                        fill: "#D6D6DA",
                        outline: "none",
                      },
                      hover: {
                        fill: "#F53",
                        outline: "none",
                      },
                      pressed: {
                        fill: "#E42",
                        outline: "none",
                      },
                    }}
                  />
                ))
              }
            </Geographies>
          </ComposableMap>
        </div>
      </div>
    </div>
  );
};
