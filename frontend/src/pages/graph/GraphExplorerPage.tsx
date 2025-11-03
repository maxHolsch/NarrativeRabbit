import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { narrativeAPI } from '../../services/api';
import { ForceDirectedGraph } from '../../visualizations/ForceDirectedGraph';
import type { GraphNode } from '../../types';

export function GraphExplorerPage() {
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);

  // Graph data query with proper cache key and fresh data settings
  const { data: graphData, isLoading: graphLoading, error: graphError } = useQuery({
    queryKey: ['graphData', { limit: 150 }],
    queryFn: async () => {
      console.log('🔍 [GraphExplorer] Fetching graph data with limit 150...');
      const data = await narrativeAPI.getGraphData(150);
      console.log('✅ [GraphExplorer] Graph data received:', {
        nodes: data?.nodes?.length || 0,
        links: data?.links?.length || 0,
      });
      return data;
    },
    staleTime: 0,
    refetchOnMount: true,
  });

  return (
    <div className="p-8 space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-2">Graph Explorer</h1>
        <p className="text-muted-foreground">
          Visualize narrative relationships with AI nodes
          {graphData && graphData.nodes.length > 0 && (
            <span className="ml-2 text-sm">
              ({graphData.nodes.length} nodes, {graphData.links?.length || 0} connections)
            </span>
          )}
        </p>
      </div>

      {graphLoading ? (
        <div className="flex items-center justify-center h-[600px] border rounded-lg bg-muted/50">
          <div className="text-center space-y-2">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto"></div>
            <p className="text-sm text-muted-foreground">Loading graph data...</p>
          </div>
        </div>
      ) : graphError ? (
        <div className="flex items-center justify-center h-[600px] border rounded-lg bg-destructive/10">
          <div className="text-center space-y-2 p-8">
            <p className="text-sm text-destructive">Error loading graph data</p>
            <p className="text-xs text-muted-foreground">{String(graphError)}</p>
          </div>
        </div>
      ) : graphData && graphData.nodes.length > 0 ? (
        <div className="relative">
          <ForceDirectedGraph
            data={graphData}
            onNodeClick={setSelectedNode}
          />

          {selectedNode && (
            <div className="absolute top-4 right-4 bg-background border rounded-lg shadow-lg p-4 max-w-sm">
              <div className="flex items-start justify-between mb-2">
                <h3 className="font-semibold">{selectedNode.type}</h3>
                <button
                  onClick={() => setSelectedNode(null)}
                  className="text-muted-foreground hover:text-foreground"
                >
                  ✕
                </button>
              </div>
              <p className="text-sm font-medium mb-1">{selectedNode.label}</p>
              <p className="text-xs text-muted-foreground">ID: {selectedNode.id}</p>
            </div>
          )}
        </div>
      ) : (
        <div className="flex items-center justify-center h-[600px] border rounded-lg bg-muted/50">
          <div className="text-center space-y-2 p-8">
            <p className="text-sm text-muted-foreground">No graph data available</p>
            <p className="text-xs text-muted-foreground">Please ensure the database is populated with data</p>
          </div>
        </div>
      )}
    </div>
  );
}
