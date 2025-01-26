import { useAuth0 } from "@auth0/auth0-react";
import { Link } from "react-router-dom";

export default function Nav() {

  const { loginWithRedirect, logout, isAuthenticated, user } = useAuth0();
  return (
    <div className="fixed top-4 right-0 left-0 z-20 px-10">
      <div className="mx-auto flex max-w-6xl items-center justify-between rounded-xl border border-[#dadada] bg-white px-6 py-3 shadow-md">
        <div className="flex items-end gap-6">
          <div className="flex items-center gap-3 text-2xl font-medium">
            <img src="/prometheus.png" alt="Prometheus Logo" className="w-10 h-10 object-contain" />
            <span className="text-gray-800">Prometheus</span>
          </div>
          <ul className="flex gap-4 pb-0.5 items-center">
            <li>
              <Link to={"/dashboard/mapview"} >Cams</Link>
            </li>
            <li>
              <button onClick={() => loginWithRedirect()} className="cursor-pointer">Login</button>
            </li>
            <li>
              <a href="" >Go Live</a>
            </li>
          </ul>
        </div>      
        <Link to={"/dashboard/mapview"} className="block rounded-md bg-red-800 px-8 py-2.5 text-white">
         Try Prometheus {">"}</Link>
      </div>
    </div>
  );
}
