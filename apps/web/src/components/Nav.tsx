import { NavLink } from "react-router-dom";

const linkCls = ({ isActive }: { isActive: boolean }) =>
  `text-sm px-2 py-1 rounded ${isActive ? "text-brand" : "text-muted-foreground hover:text-fg"}`;

export default function Nav() {
  return (
    <div className="flex items-center gap-3">
      <NavLink to="/dashboard" className={linkCls}>Dashboard</NavLink>
      <NavLink to="/book" className={linkCls}>Book</NavLink>
      <NavLink to="/racks" className={linkCls}>Racks</NavLink>
      <NavLink to="/kiosk" className={linkCls}>Kiosk</NavLink>
      <NavLink to="/admin" className={linkCls}>Admin</NavLink>
      <NavLink to="/reports" className={linkCls}>Reports</NavLink>
    </div>
  );
}