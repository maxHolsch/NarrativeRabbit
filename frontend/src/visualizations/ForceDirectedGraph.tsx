import { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import type { GraphData, GraphNode, GraphLink } from '../types';

interface Props {
  data: GraphData;
  width?: number;
  height?: number;
  onNodeClick?: (node: GraphNode) => void;
}

export const ForceDirectedGraph = ({ data, width = 1200, height = 800, onNodeClick }: Props) => {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    console.log('🎨 [ForceDirectedGraph] Component rendering with props:', {
      hasData: !!data,
      nodesCount: data?.nodes?.length || 0,
      linksCount: data?.links?.length || 0,
      width,
      height,
      svgRefExists: !!svgRef.current
    });

    if (!svgRef.current) {
      console.warn('⚠️ [ForceDirectedGraph] SVG ref is null, cannot render');
      return;
    }

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    // Handle empty data
    if (!data || !data.nodes || data.nodes.length === 0) {
      console.warn('⚠️ [ForceDirectedGraph] No data to display:', {
        data,
        hasNodes: data?.nodes ? 'yes' : 'no',
        nodesLength: data?.nodes?.length
      });
      svg.append('text')
        .attr('x', width / 2)
        .attr('y', height / 2)
        .attr('text-anchor', 'middle')
        .attr('font-size', 16)
        .attr('fill', '#718096')
        .text('No graph data available. Please check if the database is populated.');
      return;
    }

    console.log('✅ [ForceDirectedGraph] Starting graph rendering...', {
      nodes: data.nodes.length,
      links: data.links.length,
      sampleNodes: data.nodes.slice(0, 3).map(n => ({ id: n.id, type: n.type, label: n.label })),
      sampleLinks: data.links.slice(0, 3).map(l => ({ source: l.source, target: l.target, type: l.type }))
    });

    const simulation = d3.forceSimulation(data.nodes as any)
      .force('link', d3.forceLink(data.links).id((d: any) => d.id).distance(100))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide().radius(30));

    const colorScale = d3.scaleOrdinal<string>()
      .domain(['Story', 'Person', 'Group', 'Theme', 'Event'])
      .range(['#6366f1', '#10b981', '#f59e0b', '#8b5cf6', '#ef4444']);

    const g = svg.append('g');

    // Zoom
    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.1, 4])
      .on('zoom', (event) => g.attr('transform', event.transform));
    svg.call(zoom as any);

    // Links
    const link = g.append('g')
      .selectAll('line')
      .data(data.links)
      .join('line')
      .attr('stroke', '#999')
      .attr('stroke-opacity', 0.6)
      .attr('stroke-width', 1.5);

    // Nodes
    const node = g.append('g')
      .selectAll('circle')
      .data(data.nodes)
      .join('circle')
      .attr('r', (d) => d.type === 'Story' ? 8 : 6)
      .attr('fill', (d) => colorScale(d.type))
      .call(d3.drag<any, any>()
        .on('start', dragStarted)
        .on('drag', dragged)
        .on('end', dragEnded) as any)
      .on('click', (_, d) => onNodeClick?.(d));

    // Labels
    const label = g.append('g')
      .selectAll('text')
      .data(data.nodes)
      .join('text')
      .text((d) => d.label)
      .attr('font-size', 10)
      .attr('dx', 12)
      .attr('dy', 4);

    simulation.on('tick', () => {
      link
        .attr('x1', (d: any) => d.source.x)
        .attr('y1', (d: any) => d.source.y)
        .attr('x2', (d: any) => d.target.x)
        .attr('y2', (d: any) => d.target.y);

      node
        .attr('cx', (d: any) => d.x)
        .attr('cy', (d: any) => d.y);

      label
        .attr('x', (d: any) => d.x)
        .attr('y', (d: any) => d.y);
    });

    function dragStarted(event: any) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      event.subject.fx = event.subject.x;
      event.subject.fy = event.subject.y;
    }

    function dragged(event: any) {
      event.subject.fx = event.x;
      event.subject.fy = event.y;
    }

    function dragEnded(event: any) {
      if (!event.active) simulation.alphaTarget(0);
      event.subject.fx = null;
      event.subject.fy = null;
    }

    console.log('✅ [ForceDirectedGraph] Graph successfully rendered:', {
      nodes: data.nodes.length,
      links: data.links.length,
      simulationActive: true
    });

    return () => {
      console.log('🧹 [ForceDirectedGraph] Cleaning up simulation');
      simulation.stop();
    };
  }, [data, width, height, onNodeClick]);

  return (
    <div style={{ border: '1px solid #ddd', borderRadius: 8, overflow: 'hidden', background: 'white' }}>
      <svg ref={svgRef} width={width} height={height} />
      {data && data.nodes && data.nodes.length > 0 && (
        <div style={{
          position: 'absolute',
          bottom: 10,
          left: 10,
          background: 'rgba(255, 255, 255, 0.9)',
          padding: '8px 12px',
          borderRadius: 4,
          fontSize: 12,
          color: '#4a5568'
        }}>
          {data.nodes.length} nodes, {data.links?.length || 0} connections
        </div>
      )}
    </div>
  );
};
