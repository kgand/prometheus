import { Link } from "react-router-dom";
import { LandingImg } from "./LandingImg";

export default function Hero() {
  return (
    <>
      <div className="relative z-10 min-h-screen px-10 pt-44 pb-20">
        <div className="mx-auto flex max-w-6xl flex-col items-center">
          <h1 className="text-center text-[52px] leading-[1.15] font-medium">
            Unlock Realtime <span className="text-red-800">Wildfire</span>{" "}
            <br /> Detection with Prometheus
          </h1>
          <h2 className="pt-4 text-center text-xl">
            Prometheus brought fire to humanity; we <br /> bring fire detection
            to technology.
          </h2>
          <div className="flex gap-4 pt-6 text-sm">
            <Link
              to={"/dashboard/mapview"}
              className="rounded-md bg-red-800 px-6 py-2 text-white"
            >
              Try Prometheus {">"}
            </Link>
            <a
              href=""
              className="w-[161px] rounded-md border border-[#dadada] py-2 text-center"
            >
              Learn More
            </a>
          </div>
          <div className="relative">
            <div className="bg-opacity-10 relative z-10 mt-20 h-[500px] w-[800px] overflow-hidden rounded-xl bg-white backdrop-blur-md">
              <div className="grad absolute inset-0 z-20"></div>
              <LandingImg />
            </div>
            <img
              src="/blob1.svg"
              alt=""
              className="blob-blur absolute top-5 -right-12 z-0 w-[320px]"
            />
          </div>
        </div>
      </div>
      <img
        src="/blob2.svg"
        alt=""
        className="blob-blur absolute top-40 left-40 z-[1] w-[400px]"
      />
      <Circle diameter={1150} fromTop={45} />
      <Circle diameter={900} fromTop={45} />
      <Circle diameter={1450} fromTop={45} />
    </>
  );
}

type CircleProps = {
  diameter: number;
  fromTop: number;
};
const Circle: React.FC<CircleProps> = ({ diameter, fromTop }) => {
  return (
    <svg
      width="600"
      height="600"
      viewBox="0 0 600 600"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      style={{
        width: diameter,
        height: diameter,
        top: `${fromTop}%`,
        left: "50%",
        transform: "translate(-50%,-50%)",
      }}
      className="absolute z-0"
    >
      <circle cx="300" cy="300" r="299.5" stroke="url(#paint0_linear_3_2)" />
      <defs>
        <linearGradient
          id="paint0_linear_3_2"
          x1="300"
          y1="281.5"
          x2="300"
          y2="600"
          gradientUnits="userSpaceOnUse"
        >
          <stop stop-color="#F6F6F6" />
          <stop offset="0.853313" stop-color="#F6F6F6" stop-opacity="0" />
        </linearGradient>
      </defs>
    </svg>
  );
};
