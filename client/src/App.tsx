import { Outlet, Route, BrowserRouter as Router, Routes } from "react-router-dom";
import Home from "./pages/Home";
import DashboardSidebar from "./components/dashboard/DashboardSidebar";
import MapView from "./pages/dashboard/MapView";




const DashboardLayout = () => {
  return (
    <div className="flex">
      <DashboardSidebar />
      <div className="w-full">
        <Outlet />
      </div>
    </div>
  );
};

const App: React.FC = () => {
  
  return (
    <Router>
      <Routes>
        <Route path="/dashboard" element={<DashboardLayout />}>
          <Route index element={<div />} />
          <Route path="mapview" element={<MapView />} /> 
        </Route>
        <Route path="/" element={<Home />} />
      </Routes>
    </Router>
  );
};

export default App;
