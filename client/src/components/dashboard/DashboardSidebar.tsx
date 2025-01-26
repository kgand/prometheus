import {  useEffect, useState } from "react";
import { motion } from "framer-motion";
import {
  FaCamera,
  FaGithub,
  FaHome,
  FaMapMarked,
  FaUser,
} from "react-icons/fa";
import { FiChevronsLeft, FiChevronsRight } from "react-icons/fi";
import { MdFireTruck, MdLogin, MdPark } from "react-icons/md";
import { Link } from "react-router-dom";
import { PiSirenFill } from "react-icons/pi";
import { SiGoogledocs } from "react-icons/si";
import { useAuth0 } from "@auth0/auth0-react";

export default function DashboardSidebar() {
  const [isOpen, setIsOpen] = useState<boolean>(true);

  const { loginWithRedirect, logout, isAuthenticated, user } = useAuth0();


  // Add user profile section if authenticated
  const userEmail = user?.email;

  return (
    <>
      <motion.div
        className={`custom-scrollbar h-screen max-h-screen overflow-y-auto bg-gray-100 ${isOpen ? "min-w-60" : "min-w-0"} sticky top-0`}
        animate={{ width: isOpen ? 240 : 0, opacity: isOpen ? 1 : 0 }} // Animate width
        initial={{ width: 240, opacity: 0 }} // Initial width
        transition={{ duration: 0.2, ease: "easeInOut" }} // Smooth transition
      >
        {isOpen && (
          <div className="py-6 text-sm">
            <div className="border-b border-gray-300 px-6 pb-3">
              <p className="flex items-center overflow-x-hidden text-xl font-semibold whitespace-nowrap">
                <MdFireTruck className="text-red-800" />{" "}
                <span className="pl-2.5">Prometheus</span>
              </p>
              <div className="flex items-center justify-between pt-6">
                <p className="font-medium">Dashboard</p>
                <div className="flex gap-2">
                  <Link
                    to="/"
                    className="group flex h-7 w-7 items-center justify-center rounded-lg bg-gray-300 transition-all hover:bg-gray-400"
                  >
                    <FaHome className="text-gray-600 group-hover:text-gray-700" />
                  </Link>
                  <button
                    className="group flex h-7 w-7 cursor-pointer items-center justify-center rounded-lg bg-gray-300 transition-all hover:bg-gray-400"
                    onClick={() => setIsOpen(false)}
                  >
                    <FiChevronsLeft className="text-gray-600 group-hover:text-gray-700" />
                  </button>
                </div>
              </div>
            </div>
            <div className="border-b border-gray-300 px-3 pt-4 pb-3">
              <p className="px-3 font-medium text-[#808080]">Views</p>
              <ul className="mt-2 grid gap-1 text-[#404040]">
                <Link
                  to={"/dashboard/mapview"}
                  className="flex cursor-pointer items-center gap-2 overflow-x-hidden rounded-md px-3 py-1 whitespace-nowrap transition-all hover:bg-gray-200"
                >
                  <FaMapMarked /> Map View
                </Link>
                <Link
                  to="/dashboard/parkcams"
                  className="flex cursor-pointer items-center gap-2 overflow-x-hidden rounded-md px-3 py-1 whitespace-nowrap transition-all hover:bg-gray-200"
                >
                  <MdPark /> Park Cams
                </Link>
                {isAuthenticated && (
                  <Link
                    to="/dashboard/yourcams"
                    className="flex cursor-pointer items-center gap-2 overflow-x-hidden rounded-md px-3 py-1 whitespace-nowrap transition-all hover:bg-gray-200"
                  >
                    <FaCamera /> Your Cams
                  </Link>
                )}
                <Link
                  to="/dashboard/alerts"
                  className="flex cursor-pointer items-center gap-2 overflow-x-hidden rounded-md px-3 py-1 whitespace-nowrap transition-all hover:bg-gray-200"
                >
                  <PiSirenFill /> Alerts
                </Link>
              </ul>
            </div>
            <div className="border-b border-gray-300 px-3 pt-4 pb-3">
              <p className="px-3 font-medium text-[#808080]">Account</p>
              <ul className="mt-2 grid gap-1 text-[#404040]">
                {!isAuthenticated ? (
                  <li
                    className="flex cursor-pointer items-center gap-2 overflow-x-hidden rounded-md px-3 py-1 whitespace-nowrap transition-all hover:bg-gray-200"
                    onClick={() => loginWithRedirect()}
                  >
                    <MdLogin /> Sign In
                  </li>
                ) : (
                  <li
                    className="flex cursor-pointer items-center gap-2 overflow-x-hidden rounded-md px-3 py-1 whitespace-nowrap transition-all hover:bg-gray-200"
                    onClick={() =>
                      logout({
                        logoutParams: { returnTo: window.location.origin },
                      })
                    }
                  >
                    <MdLogin /> Sign Out
                  </li>
                )}
                <li className="flex cursor-pointer items-center gap-2 overflow-x-hidden rounded-md px-3 py-1 whitespace-nowrap transition-all hover:bg-gray-200">
                  <FaUser /> Accout Details
                </li>
              </ul>
            </div>
            <div className="border-b border-gray-300 px-3 pt-4 pb-3">
              <p className="px-3 font-medium text-[#808080]">Developers</p>
              <ul className="mt-2 grid gap-1 text-[#404040]">
                <li className="flex cursor-pointer items-center gap-2 overflow-x-hidden rounded-md px-3 py-1 whitespace-nowrap transition-all hover:bg-gray-200">
                  <SiGoogledocs /> Documentation
                </li>
                <a
                  href={"https://github.com/kgand/prometheus"}
                  target="_blank"
                  className="flex cursor-pointer items-center gap-2 overflow-x-hidden rounded-md px-3 py-1 whitespace-nowrap transition-all hover:bg-gray-200"
                >
                  <FaGithub /> Source Code
                </a>
              </ul>
            </div>
          </div>
        )}
      </motion.div>
      <>
        {!isOpen && (
          <div
            className="group absolute top-0 left-0 z-10 m-3 flex cursor-pointer items-center justify-center rounded-lg bg-gray-300 p-2 transition-all hover:bg-gray-400"
            onClick={() => setIsOpen(true)}
          >
            <FiChevronsRight className="text-xl text-gray-600 group-hover:text-gray-700" />
          </div>
        )}
      </>
    </>
  );
}
