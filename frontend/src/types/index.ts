// ============================================================================
// Core Story Types
// ============================================================================

export type StoryType = 'success' | 'failure' | 'conflict' | 'decision' | 'learning' | 'crisis' | 'innovation';

export interface Story {
  id: string;
  summary: string;
  full_text?: string;
  type: StoryType;
  timestamp: string;
  primary_themes: string[];
  secondary_themes?: string[];
  lessons: string[];
  outcome: string;
  department?: string;
  group?: string;
  protagonists?: string[];
  stakeholders?: string[];
  values_represented?: string[];
  key_quotes?: string[];
  source?: string;
}

// ============================================================================
// Graph Types
// ============================================================================

export type NodeType =
  | 'Story'
  | 'Person'
  | 'Group'
  | 'Theme'
  | 'Event'
  | 'Decision'
  | 'Value'
  | 'AIInitiative'
  | 'AIConcept'
  | 'NarrativeFrame'
  | 'CulturalSignal'
  | 'AdoptionBarrier';

export interface GraphNode {
  id: string;
  type: NodeType;
  label: string;
  properties?: Record<string, any>;
}

export interface GraphLink {
  source: string;
  target: string;
  type: string;
  properties?: Record<string, any>;
}

export interface GraphData {
  nodes: GraphNode[];
  links: GraphLink[];
}

// ============================================================================
// AI Initiative Types
// ============================================================================

export type InitiativeType = 'tool' | 'process' | 'transformation' | 'pilot';
export type InitiativeStatus = 'planned' | 'active' | 'paused' | 'completed' | 'failed';

export interface AIInitiative {
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
}

export interface AIInitiativeWithStories extends AIInitiative {
  official_stories: Story[];
  actual_stories: Story[];
}

// ============================================================================
// AI Concept & Frame Types
// ============================================================================

export type ConceptCategory = 'technology' | 'capability' | 'risk' | 'opportunity';
export type FrameType = 'opportunity' | 'threat' | 'tool' | 'replacement' | 'partner' | 'experiment' | 'mandate';
export type FrameValence = 'positive' | 'negative' | 'mixed' | 'neutral';
export type SophisticationLevel = 'simplistic' | 'nuanced' | 'expert';

export interface AIConcept {
  id: string;
  name: string;
  category: ConceptCategory;
  description?: string;
  mention_count?: number;
}

export interface NarrativeFrame {
  id: string;
  name: string;
  type: FrameType;
  valence: FrameValence;
  sophistication?: SophisticationLevel;
  description?: string;
}

// ============================================================================
// Barrier & Signal Types
// ============================================================================

export type BarrierType = 'cultural' | 'technical' | 'resource' | 'political';
export type SignalType = 'risk_aversion' | 'innovation' | 'skepticism' | 'enthusiasm';

export interface AdoptionBarrier {
  id: string;
  type: BarrierType;
  description: string;
  severity?: number;
  affected_groups?: string[];
}

export interface CulturalSignal {
  id: string;
  type: SignalType;
  description: string;
  strength?: number;
  groups?: string[];
}

// ============================================================================
// Analysis Response Types
// ============================================================================

export interface VocabularyGap {
  term: string;
  group1_usage: number;
  group2_usage: number;
  gap_score: number;
}

export interface FrameDifference {
  group: string;
  dominant_frame: string;
  frame_distribution: Record<string, number>;
}

export interface Question1Response {
  vocabulary_gaps: VocabularyGap[];
  frame_differences: FrameDifference[];
  sentiment_by_group: Record<string, {
    positive: number;
    negative: number;
    neutral: number;
  }>;
  sophistication_by_group: Record<string, SophisticationLevel>;
}

export interface InnovationScore {
  dimension: string;
  score: number;
  evidence: string[];
}

export interface Question2Response {
  overall_score: number;
  dimensions: InnovationScore[];
  risk_aversion_indicators: string[];
  entrepreneurial_indicators: string[];
}

export interface UnifiedNarrative {
  initiative_id: string;
  synthesized_story: string;
  bridging_elements: string[];
  common_ground: string[];
  tensions_addressed: string[];
}

export interface Question3Response extends UnifiedNarrative {}

export interface RiskAversionPattern {
  group: string;
  risk_score: number;
  patterns: string[];
  examples: string[];
}

export interface Question4Response {
  overall_risk_aversion: number;
  patterns_by_group: RiskAversionPattern[];
  hotspots: string[];
}

export interface LanguageVariation {
  context: string;
  language_patterns: string[];
  audience_adaptations: string[];
}

export interface Question5Response {
  variations: LanguageVariation[];
  context_drivers: string[];
  adaptation_strategies: string[];
}

// ============================================================================
// Sub-Agent Analysis Types
// ============================================================================

export interface NarrativeGapAnalysis {
  vocabulary_gaps: VocabularyGap[];
  framing_differences: string[];
  emphasis_gaps: string[];
  sentiment_delta: number;
  belief_contradictions: string[];
}

export interface FrameConflict {
  frame1: string;
  frame2: string;
  groups_involved: string[];
  conflict_description: string;
  severity: number;
}

export interface FrameCompetitionAnalysis {
  competing_frames: NarrativeFrame[];
  conflicts: FrameConflict[];
  common_ground: string[];
  dominant_frames_by_group: Record<string, string>;
}

export interface CulturalDimensionScore {
  dimension: string;
  score: number;
  evidence: string[];
  group_scores?: Record<string, number>;
}

export interface CulturalSignalAnalysis {
  overall_innovation_score: number;
  dimensions: CulturalDimensionScore[];
  signals_detected: CulturalSignal[];
  risk_aversion_score: number;
}

export interface ResistancePattern {
  group: string;
  resistance_level: number;
  patterns: string[];
  root_causes: string[];
  blocking_narratives: string[];
}

export interface ResistanceMapping {
  overall_resistance: number;
  patterns_by_group: ResistancePattern[];
  primary_barriers: AdoptionBarrier[];
  mitigation_strategies: string[];
}

export interface ReadinessDimension {
  name: string;
  score: number;
  description: string;
  strengths: string[];
  weaknesses: string[];
}

export interface AdoptionReadinessScore {
  overall_readiness: number;
  dimensions: ReadinessDimension[];
  ready_groups: string[];
  at_risk_groups: string[];
  recommendations: string[];
}

// ============================================================================
// Comprehensive Analysis Types
// ============================================================================

export interface ExecutiveSummary {
  key_findings: string[];
  health_score: number;
  risk_signals: string[];
  opportunities: string[];
}

export interface ActionItem {
  priority: 'high' | 'medium' | 'low';
  action: string;
  responsible_group?: string;
  timeline?: string;
}

export interface ComprehensiveAnalysisResponse {
  executive_summary: ExecutiveSummary;
  question1: Question1Response;
  question2: Question2Response;
  question3?: Question3Response;
  question4: Question4Response;
  question5: Question5Response;
  action_plan: ActionItem[];
}

// ============================================================================
// Analytics Types
// ============================================================================

export interface SentimentByGroup {
  group: string;
  positive_count: number;
  negative_count: number;
  neutral_count: number;
  mixed_count: number;
}

export interface FrameDistribution {
  frame: string;
  count: number;
  percentage: number;
}

export interface TimelineDataPoint {
  date: string;
  story_count: number;
  positive_sentiment: number;
  negative_sentiment: number;
  neutral_sentiment: number;
}

export interface GroupConnectivity {
  source_group: string;
  target_group: string;
  reference_count: number;
  shared_themes: string[];
}

export interface InfluentialStory extends Story {
  reference_count: number;
  influenced_groups: string[];
}

// ============================================================================
// Perspective & Pattern Types
// ============================================================================

export interface GroupPerspective {
  group: string;
  story_count: number;
  common_themes: [string, number][];
  emphasized_values: [string, number][];
  example_stories: Story[];
}

export interface Precedent {
  story_id: string;
  summary: string;
  type: string;
  theme_matches: number;
  outcome: string;
  lessons: string[];
}

// ============================================================================
// Chat Types
// ============================================================================

export type MessageRole = 'user' | 'assistant' | 'system';

export interface ChatMessage {
  id: string;
  role: MessageRole;
  content: string;
  timestamp: Date;
  agent?: string;
  metadata?: Record<string, any>;
}

export interface ChatConversation {
  id: string;
  title: string;
  messages: ChatMessage[];
  created_at: Date;
  updated_at: Date;
}

export interface ChatSource {
  type: 'story' | 'initiative' | 'analysis';
  id: string;
  label: string;
}

export interface ChatResponse {
  response: string;
  sources: ChatSource[];
  suggested_followups: string[];
  intent: string;
  data_summary: {
    type: string;
    count: number;
    has_analysis: boolean;
  };
  conversation_id: string;
  timestamp: string;
}

export interface ChatRequest {
  message: string;
  conversation_id?: string;
  conversation_history?: Array<{ role: string; content: string }>;
  context?: Record<string, any>;
}

// ============================================================================
// API Request/Response Types
// ============================================================================

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface APIError {
  detail: string;
  status_code: number;
}

export interface SearchFilters {
  themes?: string[];
  groups?: string[];
  types?: StoryType[];
  date_from?: string;
  date_to?: string;
}

// ============================================================================
// UI State Types
// ============================================================================

export interface FilterState {
  search: string;
  themes: string[];
  groups: string[];
  types: StoryType[];
  dateRange: {
    from?: Date;
    to?: Date;
  };
}

export interface GraphFilters {
  nodeTypes: NodeType[];
  showRelationships: string[];
  layout: 'force' | 'hierarchical' | 'radial';
  limit: number;
}
