import { MdFireTruck } from "react-icons/md";
import { Link } from "react-router-dom";

export default function Nav() {
  return (
    <div className="fixed top-4 right-0 left-0 z-20 px-10">
      <div className="mx-auto flex max-w-6xl items-center justify-between rounded-xl border border-[#dadada] bg-white px-6 py-3 shadow-md">
        <div className="flex items-end gap-6">
          <div className="flex items-center gap-2.5 text-2xl font-semibold">
            <MdFireTruck className="text-red-800" /> <span>Prometheus</span>
          </div>
          <ul className="flex gap-6 pb-0.5">
            <li>
              <a href="">Cams</a>
            </li>
            <li>
              <a href="">Alerts</a>
            </li>
            <li>
              <a href="">Go Live</a>
            </li>
          </ul>
        </div>      
        <Link to={"/dashboard"} className="block rounded-md bg-red-800 px-8 py-2.5 text-white">
         Try Prometheus {">"}</Link>
      </div>
    </div>
  );
}
