import axios from 'axios';
import type {
  Story,
  GraphData,
  GroupPerspective,
  Precedent,
  AIInitiative,
  AIInitiativeWithStories,
  AIConcept,
  NarrativeFrame,
  AdoptionBarrier,
  CulturalSignal,
  Question1Response,
  Question2Response,
  Question3Response,
  Question4Response,
  Question5Response,
  ComprehensiveAnalysisResponse,
  NarrativeGapAnalysis,
  FrameCompetitionAnalysis,
  CulturalSignalAnalysis,
  ResistanceMapping,
  AdoptionReadinessScore,
  SentimentByGroup,
  FrameDistribution,
  TimelineDataPoint,
  GroupConnectivity,
  InfluentialStory,
  SearchFilters,
  InitiativeType,
  InitiativeStatus,
  BarrierType,
  ConceptCategory,
  FrameType,
  ChatRequest,
  ChatResponse,
} from '../types';

const API_BASE = '/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ============================================================================
// Core Narrative API
// ============================================================================

export const narrativeAPI = {
  // Stories
  searchStories: async (params: {
    themes?: string[];
    groups?: string[];
    story_type?: string;
    limit?: number;
  }): Promise<Story[]> => {
    try {
      console.log('🚀 [API] Requesting stories with params:', params);
      const { data } = await api.get('/stories/search', { params });
      console.log('✅ [API] Stories response received:', {
        count: data?.length || 0,
        isArray: Array.isArray(data),
        firstStory: data?.[0] ? {
          id: data[0].id,
          type: data[0].type,
          summary: data[0].summary?.substring(0, 50) + '...'
        } : null
      });
      return Array.isArray(data) ? data : [];
    } catch (error) {
      console.error('❌ [API] Error fetching stories:', {
        error,
        message: error instanceof Error ? error.message : String(error),
        params
      });
      return [];
    }
  },

  getStory: async (id: string): Promise<Story> => {
    try {
      const { data } = await api.get(`/stories/${id}`);
      return data;
    } catch (error) {
      console.error('Error fetching story:', error);
      throw error;
    }
  },

  // Perspectives
  getGroupPerspective: async (groupName: string): Promise<GroupPerspective> => {
    const { data } = await api.get(`/perspectives/group/${encodeURIComponent(groupName)}`);
    return data;
  },

  comparePerspectives: async (eventName: string) => {
    const { data } = await api.get(`/perspectives/compare/${encodeURIComponent(eventName)}`);
    return data;
  },

  // Patterns
  findPrecedents: async (themes: string[], limit = 5): Promise<Precedent[]> => {
    const { data } = await api.get('/patterns/precedents', {
      params: { themes, limit },
    });
    return data;
  },

  findSimilar: async (storyId: string, minShared = 2) => {
    const { data } = await api.get(`/patterns/similar/${storyId}`, {
      params: { min_shared_themes: minShared },
    });
    return data;
  },

  getCautionaryTales: async (themes: string[]) => {
    const { data } = await api.get('/patterns/cautionary', { params: { themes } });
    return data;
  },

  // Graph
  getGraphData: async (limit = 100): Promise<GraphData> => {
    try {
      console.log('🚀 [API] Requesting graph data with limit:', limit);
      const { data } = await api.get('/graph/data', { params: { limit } });
      console.log('✅ [API] Graph data response received:', {
        nodesCount: data?.nodes?.length || 0,
        linksCount: data?.links?.length || 0,
        hasNodes: !!data?.nodes,
        hasLinks: !!data?.links,
        isNodesArray: Array.isArray(data?.nodes),
        isLinksArray: Array.isArray(data?.links),
        sampleNode: data?.nodes?.[0] ? {
          id: data.nodes[0].id,
          type: data.nodes[0].type,
          label: data.nodes[0].label
        } : null,
        sampleLink: data?.links?.[0] ? {
          source: data.links[0].source,
          target: data.links[0].target,
          type: data.links[0].type
        } : null
      });

      // Validate data structure
      if (!data || typeof data !== 'object') {
        console.warn('⚠️ [API] Invalid graph data received - not an object:', data);
        return { nodes: [], links: [] };
      }

      const result = {
        nodes: Array.isArray(data.nodes) ? data.nodes : [],
        links: Array.isArray(data.links) ? data.links : []
      };

      console.log('✅ [API] Returning validated graph data:', {
        nodesCount: result.nodes.length,
        linksCount: result.links.length
      });

      return result;
    } catch (error) {
      console.error('❌ [API] Error fetching graph data:', {
        error,
        message: error instanceof Error ? error.message : String(error),
        limit
      });
      return { nodes: [], links: [] };
    }
  },

  // Index
  getNarrativeIndex: async (dimension: 'theme' | 'group' | 'type' | 'value') => {
    try {
      console.log(`🚀 [API] Requesting narrative index for dimension: ${dimension}`);
      const { data } = await api.get(`/index/${dimension}`);
      console.log(`✅ [API] Narrative index (${dimension}) response:`, {
        count: data?.length || 0,
        isArray: Array.isArray(data),
        sampleItems: data?.slice(0, 3) || []
      });
      return Array.isArray(data) ? data : [];
    } catch (error) {
      console.error(`❌ [API] Error fetching narrative index (${dimension}):`, {
        error,
        message: error instanceof Error ? error.message : String(error),
        dimension
      });
      return [];
    }
  },

  // Analysis
  getGroupValues: async (groupName: string) => {
    const { data } = await api.get(`/analysis/values/${encodeURIComponent(groupName)}`);
    return data;
  },

  getCausality: async (storyId: string) => {
    const { data } = await api.get(`/analysis/causality/${storyId}`);
    return data;
  },

  // Extraction
  extractNarrative: async (params: {
    text: string;
    story_id?: string;
    source?: string;
    context?: string;
  }) => {
    const { data } = await api.post('/extract/narrative', params);
    return data;
  },

  // Examples
  getExamples: async () => {
    const { data } = await api.get('/examples/queries');
    return data;
  },
};

// ============================================================================
// AI Initiative API
// ============================================================================

export const aiInitiativeAPI = {
  // List all initiatives
  getAllInitiatives: async (): Promise<AIInitiative[]> => {
    const { data } = await api.get('/ai/initiatives');
    return data;
  },

  // Get specific initiative
  getInitiative: async (initiativeId: string): Promise<AIInitiative> => {
    const { data } = await api.get(`/ai/initiatives/${initiativeId}`);
    return data;
  },

  // Create new initiative
  createInitiative: async (initiative: {
    id: string;
    name: string;
    type: InitiativeType;
    description: string;
    goals: string[];
    status: InitiativeStatus;
    start_date?: string;
    completion_date?: string;
    owner?: string;
    stakeholders?: string[];
  }): Promise<AIInitiative> => {
    const { data } = await api.post('/ai/initiatives', initiative);
    return data;
  },

  // Get stories related to initiative
  getInitiativeStories: async (
    initiativeId: string,
    storyType: 'official' | 'actual' | 'all' = 'all'
  ): Promise<AIInitiativeWithStories> => {
    const { data } = await api.get(`/ai/initiatives/${initiativeId}/stories`, {
      params: { story_type: storyType },
    });
    return data;
  },
};

// ============================================================================
// Strategic Questions API
// ============================================================================

export const strategicQuestionsAPI = {
  // Q1: How do different teams talk about AI differently?
  getQuestion1Analysis: async (): Promise<Question1Response> => {
    const { data } = await api.get('/ai/analysis/question1');
    return data;
  },

  // Q2: Do we have entrepreneurial culture?
  getQuestion2Analysis: async (): Promise<Question2Response> => {
    const { data } = await api.get('/ai/analysis/question2');
    return data;
  },

  // Q3: Can you design a unified story?
  getQuestion3Analysis: async (initiativeId: string): Promise<Question3Response> => {
    const { data } = await api.get(`/ai/analysis/question3/${initiativeId}`);
    return data;
  },

  // Q4: Are we risk-averse?
  getQuestion4Analysis: async (): Promise<Question4Response> => {
    const { data } = await api.get('/ai/analysis/question4');
    return data;
  },

  // Q5: Why does language vary by context?
  getQuestion5Analysis: async (): Promise<Question5Response> => {
    const { data } = await api.get('/ai/analysis/question5');
    return data;
  },

  // Comprehensive Analysis
  getComprehensiveAnalysis: async (params?: {
    initiative_id?: string;
    include_recommendations?: boolean;
    generate_action_plan?: boolean;
  }): Promise<ComprehensiveAnalysisResponse> => {
    const { data } = await api.post('/ai/analysis/comprehensive', params || {});
    return data;
  },
};

// ============================================================================
// Sub-Agent Analysis API
// ============================================================================

export const subAgentAPI = {
  // Narrative Gap Analysis
  getGapAnalysis: async (): Promise<NarrativeGapAnalysis> => {
    const { data } = await api.get('/ai/analysis/gaps');
    return data;
  },

  // Frame Competition
  getFrameCompetition: async (): Promise<FrameCompetitionAnalysis> => {
    const { data } = await api.get('/ai/analysis/frames');
    return data;
  },

  getFrameConflicts: async (initiativeId: string) => {
    const { data } = await api.get(`/ai/frames/conflicts/${initiativeId}`);
    return data;
  },

  // Cultural Signals
  getCultureAnalysis: async (): Promise<CulturalSignalAnalysis> => {
    const { data } = await api.get('/ai/analysis/culture');
    return data;
  },

  getCulturalSignals: async (): Promise<CulturalSignal[]> => {
    const { data } = await api.get('/ai/culture/signals');
    return data;
  },

  getRiskAversionPatterns: async () => {
    const { data } = await api.get('/ai/culture/risk-aversion');
    return data;
  },

  // Resistance Mapping
  getResistanceAnalysis: async (): Promise<ResistanceMapping> => {
    const { data } = await api.get('/ai/analysis/resistance');
    return data;
  },

  getResistancePatterns: async () => {
    const { data } = await api.get('/ai/resistance/patterns');
    return data;
  },

  getRootCauses: async (group: string) => {
    const { data } = await api.get(`/ai/resistance/root-causes/${group}`);
    return data;
  },

  // Adoption Readiness
  getReadinessAnalysis: async (): Promise<AdoptionReadinessScore> => {
    const { data } = await api.get('/ai/analysis/readiness');
    return data;
  },
};

// ============================================================================
// AI Analytics API
// ============================================================================

export const aiAnalyticsAPI = {
  // AI Stories
  getAIStories: async (params?: {
    group?: string;
    sentiment?: 'positive' | 'negative' | 'mixed' | 'neutral';
    frame?: FrameType;
    sophistication?: 'simplistic' | 'nuanced' | 'expert';
    limit?: number;
  }): Promise<Story[]> => {
    const { data } = await api.get('/ai/stories/ai', { params });
    return data;
  },

  // Sentiment Analytics
  getSentimentByGroup: async (): Promise<SentimentByGroup[]> => {
    const { data } = await api.get('/ai/analytics/sentiment-by-group');
    return data;
  },

  // Frame Distribution
  getFrameDistribution: async (): Promise<FrameDistribution[]> => {
    const { data } = await api.get('/ai/analytics/frame-distribution');
    return data;
  },

  // Adoption Timeline
  getAdoptionTimeline: async (params?: {
    start_date?: string;
    end_date?: string;
    group?: string;
  }): Promise<TimelineDataPoint[]> => {
    const { data } = await api.get('/ai/analytics/adoption-timeline', { params });
    return data;
  },

  // Influential Stories
  getInfluentialStories: async (limit = 10): Promise<InfluentialStory[]> => {
    const { data } = await api.get('/ai/analytics/influential-stories', {
      params: { limit },
    });
    return data;
  },

  // Group Connectivity
  getGroupConnectivity: async (): Promise<GroupConnectivity[]> => {
    const { data } = await api.get('/ai/analytics/group-connectivity');
    return data;
  },
};

// ============================================================================
// AI Data API (Barriers, Concepts, Frames)
// ============================================================================

export const aiDataAPI = {
  // Barriers
  getAllBarriers: async (params?: {
    type?: BarrierType;
    group?: string;
  }): Promise<AdoptionBarrier[]> => {
    const { data } = await api.get('/ai/barriers', { params });
    return data;
  },

  // Concepts
  getAllConcepts: async (params?: {
    category?: ConceptCategory;
    limit?: number;
  }): Promise<AIConcept[]> => {
    const { data } = await api.get('/ai/concepts', { params });
    return data;
  },

  getConceptCoOccurrence: async (conceptId: string) => {
    const { data } = await api.get(`/ai/concepts/${conceptId}/co-occurrence`);
    return data;
  },

  // Frames
  getAllFrames: async (): Promise<NarrativeFrame[]> => {
    const { data } = await api.get('/ai/frames');
    return data;
  },
};

// ============================================================================
// Health & System API
// ============================================================================

export const systemAPI = {
  getHealth: async () => {
    const { data } = await api.get('/health');
    return data;
  },

  getAIHealth: async () => {
    const { data } = await api.get('/ai/health');
    return data;
  },

  getAIExamples: async () => {
    const { data } = await api.get('/ai/examples');
    return data;
  },
};

// ============================================================================
// Chat API
// ============================================================================

export const chatAPI = {
  sendMessage: async (request: ChatRequest): Promise<ChatResponse> => {
    try {
      console.log('🚀 [API] Sending chat message:', request.message);
      const { data } = await api.post('/ai/chat', request);
      console.log('✅ [API] Chat response received:', {
        hasResponse: !!data.response,
        sourcesCount: data.sources?.length || 0,
        followupsCount: data.suggested_followups?.length || 0,
        intent: data.intent
      });
      return data;
    } catch (error) {
      console.error('❌ [API] Error sending chat message:', {
        error,
        message: error instanceof Error ? error.message : String(error),
        request
      });
      throw error;
    }
  },
};

// ============================================================================
// Combined Export
// ============================================================================

export const apiClient = {
  narrative: narrativeAPI,
  initiatives: aiInitiativeAPI,
  questions: strategicQuestionsAPI,
  subAgents: subAgentAPI,
  analytics: aiAnalyticsAPI,
  aiData: aiDataAPI,
  system: systemAPI,
  chat: chatAPI,
};

export default api;
