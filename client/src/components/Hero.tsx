import { Link } from "react-router-dom";

export default function Hero() {
  return (
    <>
      <div className="relative z-10 min-h-screen px-10 pt-40 pb-20">
        <div className="mx-auto flex max-w-6xl flex-col items-center">
          <h1 className="text-center text-[52px] leading-[1.15] font-semibold">
            Unlock Realtime <span className="text-red-800">Wildfire</span>{" "}
            <br /> Detection with Prometheus
          </h1>
          <h2 className="pt-4 text-center text-xl">
            Prometheus brought fire to humanity; we <br /> bring fire detection
            to technology.
          </h2>
          <div className="flex gap-4 pt-6 text-sm">
            <Link
              to={"/dashboard"}
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
            <div className="grad relative z-10 mt-16 h-[420px] w-[800px] rounded-xl"></div>
            <img src="/blob1.svg" alt="" className="absolute z-0 w-[320px] top-5 -right-12 blob-blur" />
          </div>
        </div>
      </div>
      <Circle diameter={1000} fromTop={55} />
      <Circle diameter={800} fromTop={55} />
      <Circle diameter={1250} fromTop={55} />
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
      <circle cx="300" cy="300" r="299.5" stroke="#efefef" />
    </svg>
  );
};
