import { NavLink } from "react-router-dom";
import { Map, Dumbbell, LayoutDashboard, CalendarCheck, BarChart3, Settings } from "lucide-react";

const item = "flex items-center gap-2 px-4 py-2 rounded hover:bg-muted";
const active = "bg-muted";

export default function Sidebar() {
  return (
    <div className="p-4 space-y-2">
      <div className="text-xl font-semibold px-2 mb-2">Powerbase</div>
      <NavLink to="/dashboard" className={({isActive})=>`${item} ${isActive?active:""}`}>
        <LayoutDashboard className="h-4 w-4" /> Dashboard
      </NavLink>
      <NavLink to="/book" className={({isActive})=>`${item} ${isActive?active:""}`}>
        <CalendarCheck className="h-4 w-4" /> Book
      </NavLink>
      <NavLink to="/racks" className={({isActive})=>`${item} ${isActive?active:""}`}>
        <Dumbbell className="h-4 w-4" /> Racks
      </NavLink>
      <NavLink to="/admin/floorplan" className="sidebar-link">
        <Map className="h-4 w-4" />
        <span>Floorplan</span>
      </NavLink>
      <NavLink to="/reports" className={({isActive})=>`${item} ${isActive?active:""}`}>
        <BarChart3 className="h-4 w-4" /> Reports
      </NavLink>
      <NavLink to="/settings" className={({isActive})=>`${item} ${isActive?active:""}`}>
        <Settings className="h-4 w-4" /> Settings
      </NavLink>
    </div>
  );
}