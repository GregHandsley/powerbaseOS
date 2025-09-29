import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export function KPITile({ title, value }: { title: string; value: string | number }) {
  return (
    <Card>
      <CardHeader><CardTitle className="text-sm text-muted-foreground">{title}</CardTitle></CardHeader>
      <CardContent><div className="text-2xl font-semibold">{value}</div></CardContent>
    </Card>
  );
}