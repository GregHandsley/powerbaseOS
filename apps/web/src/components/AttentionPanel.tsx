import { AlertTriangle } from "lucide-react";

export default function AttentionPanel({ children }: { children: React.ReactNode }) {
  return (
    <div className="border border-yellow-300/60 bg-yellow-50 text-yellow-900 rounded-md p-3 flex gap-2">
      <AlertTriangle className="h-4 w-4 mt-0.5" />
      <div className="text-sm">{children}</div>
    </div>
  );
}