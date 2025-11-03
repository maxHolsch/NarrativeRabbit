import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { narrativeAPI } from '../services/api';
import { ForceDirectedGraph } from '../visualizations/ForceDirectedGraph';
import type { GraphNode, Story } from '../types';

export const Dashboard = () => {
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);
  const [activeTab, setActiveTab] = useState<'graph' | 'stories' | 'perspectives' | 'insights'>('graph');
  const [showDebug, setShowDebug] = useState(false);

  // Graph data query with proper cache key and fresh data settings
  const { data: graphData, isLoading: graphLoading, error: graphError } = useQuery({
    queryKey: ['graphData', { limit: 150 }],
    queryFn: async () => {
      console.log('🔍 [Dashboard] Fetching graph data with limit 150...');
      const data = await narrativeAPI.getGraphData(150);
      console.log('✅ [Dashboard] Graph data received:', {
        nodes: data?.nodes?.length || 0,
        links: data?.links?.length || 0,
        sampleNode: data?.nodes?.[0],
        sampleLink: data?.links?.[0]
      });
      return data;
    },
    staleTime: 0, // Always fetch fresh data
    refetchOnMount: true,
  });

  // Stories query with proper cache key and fresh data settings
  const { data: stories, error: storiesError } = useQuery({
    queryKey: ['stories', { limit: 30 }],
    queryFn: async () => {
      console.log('🔍 [Dashboard] Fetching stories with limit 30...');
      const data = await narrativeAPI.searchStories({ limit: 30 });
      console.log('✅ [Dashboard] Stories received:', {
        count: data?.length || 0,
        sampleStory: data?.[0],
        allStoryIds: data?.map(s => s.id) || []
      });
      return data;
    },
    staleTime: 0, // Always fetch fresh data
    refetchOnMount: true,
  });

  // Theme index query with proper cache key
  const { data: themeIndex } = useQuery({
    queryKey: ['themeIndex', { dimension: 'theme' }],
    queryFn: async () => {
      console.log('🔍 [Dashboard] Fetching theme index...');
      const data = await narrativeAPI.getNarrativeIndex('theme');
      console.log('✅ [Dashboard] Theme index received:', data?.length || 0, 'themes');
      return data;
    },
    staleTime: 0,
    refetchOnMount: true,
  });

  // Group index query with proper cache key
  const { data: groupIndex } = useQuery({
    queryKey: ['groupIndex', { dimension: 'group' }],
    queryFn: async () => {
      console.log('🔍 [Dashboard] Fetching group index...');
      const data = await narrativeAPI.getNarrativeIndex('group');
      console.log('✅ [Dashboard] Group index received:', data?.length || 0, 'groups');
      return data;
    },
    staleTime: 0,
    refetchOnMount: true,
  });

  return (
    <div className="dashboard">
      <header className="header">
        <h1>📖 Narrative Knowledge Graph</h1>
        <p>Explore organizational stories, patterns, and perspectives</p>
      </header>

      <nav className="tabs">
        {(['graph', 'stories', 'perspectives', 'insights'] as const).map((tab) => (
          <button
            key={tab}
            className={`tab ${activeTab === tab ? 'active' : ''}`}
            onClick={() => setActiveTab(tab)}
          >
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
        <button
          className="tab"
          onClick={() => setShowDebug(!showDebug)}
          style={{ marginLeft: 'auto', fontSize: '12px' }}
        >
          {showDebug ? '🔍 Hide Debug' : '🔍 Debug Info'}
        </button>
      </nav>

      {/* Debug Panel */}
      {showDebug && (
        <div style={{
          margin: '20px',
          padding: '20px',
          background: '#f8f9fa',
          border: '1px solid #dee2e6',
          borderRadius: '8px',
          fontSize: '13px',
          fontFamily: 'monospace'
        }}>
          <h3 style={{ marginTop: 0, fontSize: '16px', fontWeight: 'bold' }}>Debug Information</h3>

          <div style={{ marginBottom: '15px' }}>
            <strong>📊 Stories Query:</strong>
            <div style={{ marginLeft: '10px', marginTop: '5px' }}>
              • Status: {stories ? '✅ Success' : storiesError ? '❌ Error' : '⏳ Loading'}<br/>
              • Count: {stories?.length || 0}<br/>
              • Error: {storiesError ? String(storiesError) : 'None'}<br/>
              • Sample IDs: {stories?.slice(0, 5).map(s => s.id).join(', ') || 'N/A'}
            </div>
          </div>

          <div style={{ marginBottom: '15px' }}>
            <strong>🌐 Graph Query:</strong>
            <div style={{ marginLeft: '10px', marginTop: '5px' }}>
              • Status: {graphData ? '✅ Success' : graphError ? '❌ Error' : graphLoading ? '⏳ Loading' : '❓ Unknown'}<br/>
              • Nodes: {graphData?.nodes?.length || 0}<br/>
              • Links: {graphData?.links?.length || 0}<br/>
              • Error: {graphError ? String(graphError) : 'None'}
            </div>
          </div>

          <div style={{ marginBottom: '15px' }}>
            <strong>🏷️ Theme Index Query:</strong>
            <div style={{ marginLeft: '10px', marginTop: '5px' }}>
              • Count: {themeIndex?.length || 0}<br/>
              • Top Themes: {themeIndex?.slice(0, 3).map((t: any) => t.theme).join(', ') || 'N/A'}
            </div>
          </div>

          <div style={{ marginBottom: '15px' }}>
            <strong>👥 Group Index Query:</strong>
            <div style={{ marginLeft: '10px', marginTop: '5px' }}>
              • Count: {groupIndex?.length || 0}<br/>
              • Groups: {groupIndex?.slice(0, 3).map((g: any) => g.group).join(', ') || 'N/A'}
            </div>
          </div>

          <div style={{
            marginTop: '15px',
            padding: '10px',
            background: '#e7f3ff',
            borderRadius: '4px',
            fontSize: '12px'
          }}>
            <strong>ℹ️ Tips:</strong><br/>
            • If data is not updating, try hard refresh (Cmd+Shift+R / Ctrl+Shift+R)<br/>
            • Check browser console for detailed logs<br/>
            • Neo4j Browser: <a href="http://localhost:7474" target="_blank" rel="noopener noreferrer">http://localhost:7474</a> (not bolt://)<br/>
            • Check Network tab in DevTools to see actual API responses
          </div>
        </div>
      )}

      <div className="content">
        {activeTab === 'graph' && (
          <div className="graph-view">
            <div className="graph-container">
              {graphLoading ? (
                <div className="loading">Loading graph...</div>
              ) : graphData ? (
                <ForceDirectedGraph
                  data={graphData}
                  onNodeClick={setSelectedNode}
                />
              ) : null}
            </div>

            {selectedNode && (
              <div className="side-panel">
                <h3>{selectedNode.type}: {selectedNode.label}</h3>
                <p className="node-id">ID: {selectedNode.id}</p>
                <button onClick={() => setSelectedNode(null)}>Close</button>
              </div>
            )}

            <div className="legend">
              <h4>Legend</h4>
              <div className="legend-item"><span className="dot story"></span> Story</div>
              <div className="legend-item"><span className="dot person"></span> Person</div>
              <div className="legend-item"><span className="dot group"></span> Group</div>
              <div className="legend-item"><span className="dot theme"></span> Theme</div>
              <div className="legend-item"><span className="dot event"></span> Event</div>
            </div>
          </div>
        )}

        {activeTab === 'stories' && (
          <div className="stories-view">
            <h2>Recent Stories {stories && stories.length > 0 && (
              <span style={{ fontSize: '16px', color: '#718096', fontWeight: 'normal' }}>
                ({stories.length} stories loaded)
              </span>
            )}</h2>
            {!stories || stories.length === 0 ? (
              <div className="empty-state">
                <p>No stories found. Please ensure the database is populated with data.</p>
                <p style={{ fontSize: '14px', color: '#718096', marginTop: '8px' }}>
                  You may need to run the data generation script or import stories.
                </p>
              </div>
            ) : (
              <div className="story-grid">
                {stories.map((story: Story) => (
                  <div key={story.id} className="story-card">
                    <div className="story-header">
                      <span className={`story-type ${story.type}`}>{story.type}</span>
                      <span className="story-date">
                        {new Date(story.timestamp).toLocaleDateString()}
                      </span>
                    </div>
                    <p className="story-summary">{story.summary || 'No summary available'}</p>
                    {story.primary_themes && story.primary_themes.length > 0 && (
                      <div className="story-themes">
                        {story.primary_themes.slice(0, 3).map((theme, idx) => (
                          <span key={`${story.id}-${theme}-${idx}`} className="theme-tag">{theme}</span>
                        ))}
                      </div>
                    )}
                    {story.lessons && story.lessons.length > 0 && (
                      <div className="story-lessons">
                        <strong>Lessons:</strong>
                        <ul>
                          {story.lessons.slice(0, 2).map((lesson, i) => (
                            <li key={i}>{lesson}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'perspectives' && (
          <div className="perspectives-view">
            <h2>Group Perspectives</h2>
            {!groupIndex || groupIndex.length === 0 ? (
              <div className="empty-state">
                <p>No group data available.</p>
              </div>
            ) : (
              <div className="groups-grid">
                {groupIndex.map((item: any) => (
                  <div key={item.group} className="group-card">
                    <h3>{item.group}</h3>
                    <p className="story-count">{item.story_count} stories</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'insights' && (
          <div className="insights-view">
            <h2>Narrative Insights</h2>

            <div className="insights-grid">
              <div className="insight-card">
                <h3>Top Themes</h3>
                {!themeIndex || themeIndex.length === 0 ? (
                  <p style={{ color: '#718096', fontSize: '14px' }}>No theme data available</p>
                ) : (
                  themeIndex.slice(0, 8).map((item: any) => (
                    <div key={item.theme} className="insight-item">
                      <span>{item.theme}</span>
                      <span className="count">{item.story_count}</span>
                    </div>
                  ))
                )}
              </div>

              <div className="insight-card">
                <h3>Story Distribution</h3>
                <p>Total Stories: {stories?.length || 0}</p>
                <div className="type-distribution">
                  {['success', 'failure', 'learning', 'decision', 'crisis'].map(type => {
                    const count = stories?.filter((s: Story) => s.type === type).length || 0;
                    return (
                      <div key={type} className="type-bar">
                        <span>{type}</span>
                        <div className="bar" style={{ width: `${(count / (stories?.length || 1)) * 100}%` }} />
                        <span>{count}</span>
                      </div>
                    );
                  })}
                </div>
              </div>

              <div className="insight-card">
                <h3>Active Groups</h3>
                {groupIndex?.slice(0, 5).map((item: any) => (
                  <div key={item.group} className="insight-item">
                    <span>{item.group}</span>
                    <span className="count">{item.story_count} stories</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
