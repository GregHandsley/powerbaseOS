import { KPITile } from "@/components/KPITile";
import AttentionPanel from "@/components/AttentionPanel";
import { Button } from "@/components/ui/button";

export default function DashboardPage() {
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold">Dashboard</h2>
        <Button>Primary Action</Button>
      </div>
      <AttentionPanel>Demo of tokenized panel using Tailwind variables.</AttentionPanel>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <KPITile title="Bookings Today" value="—" />
        <KPITile title="Active Holds" value="—" />
        <KPITile title="Rack Utilisation" value="—" />
        <KPITile title="Incidents" value="—" />
      </div>
    </div>
  );
}