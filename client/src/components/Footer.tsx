import { FaGithub } from "react-icons/fa";
import { Link } from "react-router-dom";

export default function Footer() {
  return (
    <footer className='border-t border-[#f5f5f5] py-20 bg-white relative z-10'>
         <div className="flex flex-col-reverse items-center lg:justify-center lg:flex-row">
        <div className="flex flex-col items-center  border-r-none border-[#f5f5f5] mt-12 lg:max-w-[320px] lg:border-r lg:mt-0 lg:items-start lg:pr-16">
          <p className="text-xl flex font-medium items-center gap-0.5">
            <img src="/prometheus.png" alt="Prometheus Logo" className="w-12 h-12 object-contain" />
            <span className="text-gray-800">Prometheus</span>
          </p>
          <a href="https://github.com/kgand/prometheus" target="_blank" className="flex items-center  mt-4 text-lg">
            <span className="mr-2">
              <FaGithub />
            </span>
            Github
          </a>
          <p className="mt-3 text-sm text-center lg:text-left">
            © Copyright 2025 Prometheus. All 
            Commercial Rights Reserved.
          </p>
        </div>
        <div className="flex max-w-[730px] w-full justify-center lg:pl-12 sm:justify-around ">
            <div className="mr-16 sm:mr-0">
                <p className="text-semibold">Features</p>
                <ul className="text-sm">
                    <a href="#toc"><li className="mt-4">Cams</li></a>
                    <a href="#about"><li className="mt-4">Alerts</li></a>
                </ul>
            </div>
            <div className="hidden md:block">
                <p className="text-semibold">About</p>
                <ul className="text-sm">
                    <li className="mt-4 cursor-not-allowed">Team</li>
                    <li className="mt-4 cursor-not-allowed">Info</li>
                </ul>
            </div>
            <div className="">
                <p className="text-semibold">Features</p>
                <ul className="text-sm">
                    <li className="mt-4"><Link to={"/code"}>Dashboard</Link></li>
                    <li className="mt-4"><Link to={"/account"}>Go Live</Link></li>
                </ul>
            </div>
        </div>
      </div>
    </footer>
  )
}
