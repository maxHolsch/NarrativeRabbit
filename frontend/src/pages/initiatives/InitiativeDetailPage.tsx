import { useParams } from 'react-router-dom';

export function InitiativeDetailPage() {
  const { id } = useParams();
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-4">Initiative Detail: {id}</h1>
      <p className="text-muted-foreground">View official vs actual narratives</p>
      {/* TODO: Implement initiative detail */}
    </div>
  );
}
