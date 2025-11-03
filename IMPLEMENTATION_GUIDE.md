# Frontend Implementation Guide

## Overview
This document outlines the complete frontend rebuild for the Narrative Analysis Tool, exposing all backend AI features through an enterprise-grade React application.

## Current Status

### ✅ Completed Foundation
1. **Project Structure** - Organized folders for components, features, pages, hooks, lib, store
2. **Dependencies** - All UI libraries, charts, forms, testing tools installed
3. **Design System** - Tailwind CSS with HSL design tokens, dark mode support
4. **TypeScript Types** - 440+ lines covering all backend entities and responses
5. **API Client** - 400+ lines with all backend endpoints typed and organized
6. **Global State** - Zustand store for theme, sidebar, filters
7. **Routing** - React Router with all routes defined
8. **Base Components** - Button, Card, Input, Badge, Skeleton
9. **App Layout** - Sidebar navigation with theme toggle

### 🚧 In Progress
- Page implementations
- Feature components
- Analytics visualizations
- Chat interface

## Implementation Phases

### Phase 2: Core Pages (3-4 days)

#### 2.1 HomePage
**Location**: `src/pages/home/HomePage.tsx`
**Features**:
- Dashboard with key metrics cards
- Quick links to major features
- Recent activity feed
- System health status

**Data Sources**:
- `/health` - System status
- `/ai/health` - AI service status
- `/api/stories/search?limit=5` - Recent stories
- `/ai/initiatives` - Initiative count

#### 2.2 Stories List Page
**Location**: `src/pages/stories/StoriesListPage.tsx`
**Features**:
- Filterable story grid
- Search by themes, groups, types
- Story type badges
- Pagination
- Click to detail view

**Components Needed**:
- `StoryCard` - Reusable story card
- `StoryFilters` - Filter sidebar
- `SearchBar` - Search input with debounce

#### 2.3 Story Detail Page
**Location**: `src/pages/stories/StoryDetailPage.tsx`
**Features**:
- Full story content
- Related entities (people, groups, themes)
- Similar stories
- Causal chain visualization
- Lessons learned section

**API Calls**:
- `/api/stories/{id}`
- `/api/patterns/similar/{id}`
- `/api/analysis/causality/{id}`

### Phase 3: AI Features (5-8 days)

#### 3.1 AI Initiatives
**List Page**: `src/pages/initiatives/InitiativesListPage.tsx`
- Grid of initiative cards
- Filter by type, status
- Create button

**Detail Page**: `src/pages/initiatives/InitiativeDetailPage.tsx`
- Initiative metadata
- Official vs Actual narratives comparison
- Related stories tabs
- Status timeline

**Create Page**: `src/pages/initiatives/InitiativeCreatePage.tsx`
- Multi-step form
- React Hook Form + Zod validation
- Type, goals, stakeholders fields

#### 3.2 Strategic Questions Hub
**Location**: `src/pages/questions/QuestionsHubPage.tsx`
**Features**:
- 5 question cards with descriptions
- Quick insights preview
- Navigate to detailed analysis

#### 3.3 Question Pages

**Q1: How do teams talk about AI differently?**
- Vocabulary gap table
- Frame difference charts
- Sentiment by group bar chart
- Sophistication comparison

**Q2: Entrepreneurial culture?**
- Overall innovation score gauge
- 5 dimension scores (radar chart)
- Risk aversion indicators list
- Entrepreneurial indicators list

**Q3: Unified story design**
- Initiative selector
- Synthesized narrative display
- Bridging elements highlight
- Common ground identification

**Q4: Risk-averse culture?**
- Overall risk-aversion score
- Patterns by group heatmap
- Hotspots list with severity

**Q5: Language variation by context?**
- Context-driven variations list
- Language adaptation strategies
- Audience-specific framing

### Phase 4: Analytics Visualizations (3-4 days)

#### 4.1 Frame Competition Network
**Location**: `src/features/analytics/FrameCompetitionViz.tsx`
**Technology**: D3.js force-directed graph
**Features**:
- Nodes = Narrative frames
- Edges = Conflicts between frames
- Node size = Frame prevalence
- Color = Frame valence
- Click for details

#### 4.2 Adoption Timeline
**Location**: `src/features/analytics/AdoptionTimeline.tsx`
**Technology**: Recharts LineChart
**Features**:
- X-axis: Time
- Y-axis: Story count
- Multiple lines for sentiment
- Filter by group
- Date range selector

#### 4.3 Cultural Signals Dashboard
**Location**: `src/features/analytics/CulturalSignals.tsx`
**Components**:
- Innovation score gauge
- 5 dimension breakdown (radar)
- Risk-aversion heatmap by group
- Signal strength indicators
- Group comparison table

#### 4.4 Analytics Hub
**Location**: `src/pages/analytics/AnalyticsHubPage.tsx`
**Layout**:
- Tab navigation for different analytics
- Frame Competition tab
- Adoption Timeline tab
- Cultural Signals tab
- Sentiment Analysis tab
- Group Connectivity tab

### Phase 5: Enhanced Graph Explorer (2-3 days)

**Location**: `src/pages/graph/GraphExplorerPage.tsx`

**Enhancements**:
1. **AI-Specific Nodes**:
   - AIInitiative (violet)
   - AIConcept (pink)
   - NarrativeFrame (teal)
   - CulturalSignal (lime)
   - AdoptionBarrier (rose)

2. **Advanced Filtering**:
   - Multi-select node types
   - Relationship type filter
   - Date range filter
   - Group filter

3. **Layout Options**:
   - Force-directed (default)
   - Hierarchical
   - Radial

4. **Interactive Features**:
   - Double-click to navigate
   - Right-click context menu
   - Path highlighting
   - Minimap for navigation
   - Search nodes by name

**Components**:
- `GraphCanvas` - D3 visualization wrapper
- `GraphControls` - Filter and layout controls
- `GraphLegend` - Dynamic legend
- `GraphSidePanel` - Node details
- `NodeContextMenu` - Right-click menu

### Phase 6: Chat Interface (2-3 days)

**Location**: `src/pages/chat/ChatPage.tsx`

**Layout**:
```
┌─────────────────────────────────────┐
│ Agent Selector (dropdown)           │
├─────────────────────────────────────┤
│                                     │
│  Message History (scrollable)       │
│  - User messages (right)            │
│  - AI messages (left)               │
│  - Rich content (charts, cards)     │
│                                     │
├─────────────────────────────────────┤
│ Input Area + Send Button            │
└─────────────────────────────────────┘
```

**Features**:
1. **Agent Selection**:
   - Gap Analyzer
   - Frame Competition
   - Cultural Signals
   - Resistance Mapper
   - Readiness Scorer
   - Comprehensive (all 5)

2. **Message Types**:
   - Text
   - Code blocks
   - Embedded charts
   - Story cards
   - Action buttons

3. **Quick Actions**:
   - "Analyze this initiative"
   - "Compare frames"
   - "Check readiness"
   - "Find resistance patterns"

4. **History**:
   - Save conversations
   - Load previous chats
   - Export transcript

**Components**:
- `ChatContainer` - Main layout
- `ChatMessage` - Message bubble
- `ChatInput` - Input with send button
- `AgentSelector` - Dropdown selector
- `QuickActions` - Button group
- `MessageContent` - Rich content renderer

### Phase 7: Advanced Features (3-4 days)

#### 7.1 Global Search
**Location**: `src/components/common/GlobalSearch.tsx`
**Features**:
- Search across stories, initiatives, groups
- Keyboard shortcut (Cmd/Ctrl + K)
- Instant results dropdown
- Recent searches
- Search filters

#### 7.2 Data Tables
**Location**: `src/components/common/DataTable.tsx`
**Features**:
- Sortable columns
- Pagination (client + server)
- Row selection
- Column visibility toggle
- Export to CSV
- Responsive design

#### 7.3 Advanced Filters
**Location**: `src/components/common/AdvancedFilters.tsx`
**Features**:
- Multi-select dropdowns
- Date range picker
- Tag input
- Filter chips (removable)
- Save filter presets
- Clear all button

#### 7.4 Detail Pages Enhancement
**Group Detail**: Show group info, members, stories, values, cultural signals
**Theme Detail**: Theme usage, stories, trends over time
**Concept Detail**: AI concept mentions, co-occurrence network

### Phase 8: Enterprise Polish (3-4 days)

#### 8.1 Loading States
**Components**:
- `SkeletonCard` - Card placeholder
- `SkeletonTable` - Table placeholder
- `SkeletonGraph` - Graph placeholder
- `LoadingSpinner` - Inline spinner
- `PageLoader` - Full-page loader

**Pattern**: Use Skeleton on first load, Spinner on refresh

#### 8.2 Error Handling
**Components**:
- `ErrorBoundary` - Catch React errors
- `ErrorPage` - Full-page error
- `ErrorAlert` - Inline error
- `Toast` - Success/error notifications

**Features**:
- Automatic retry with exponential backoff
- User-friendly error messages
- Error reporting (Sentry integration)

#### 8.3 Animations
**Library**: Framer Motion
**Patterns**:
- Page transitions (fade in)
- List animations (stagger)
- Card hover effects
- Modal enter/exit
- Skeleton pulse

#### 8.4 Accessibility
**Standards**: WCAG 2.1 AA
**Features**:
- Proper ARIA labels
- Keyboard navigation
- Focus management
- Screen reader support
- Color contrast (4.5:1 minimum)
- Skip links

#### 8.5 Performance
**Optimizations**:
- Code splitting (React.lazy)
- Image lazy loading
- Virtual scrolling (react-window)
- Memoization (useMemo, useCallback)
- Debounced search
- Request deduplication

#### 8.6 Testing
**Framework**: Vitest + React Testing Library
**Coverage**:
- Unit tests for utilities
- Component tests for UI
- Integration tests for features
- E2E tests for critical flows

**Example test structure**:
```typescript
describe('StoryCard', () => {
  it('renders story information', () => {
    // Test implementation
  });

  it('handles click events', () => {
    // Test implementation
  });
});
```

### Phase 9: Documentation (1 day)

#### 9.1 User Guide
- Getting started
- Feature overview
- How-to guides
- FAQ

#### 9.2 Developer Docs
- Architecture overview
- Component API docs
- State management guide
- API integration guide
- Testing guide
- Deployment guide

#### 9.3 Storybook
- Component documentation
- Interactive examples
- Props documentation
- Design system showcase

## Technology Stack

### Core
- **React 18** - UI library
- **TypeScript 5** - Type safety
- **Vite 5** - Build tool
- **React Router 6** - Routing

### State Management
- **Zustand** - Global state
- **TanStack React Query** - Server state
- **React Hook Form** - Form state

### UI & Styling
- **Tailwind CSS** - Utility-first CSS
- **Radix UI** - Accessible primitives
- **Lucide React** - Icons
- **Framer Motion** - Animations

### Data Visualization
- **D3.js** - Custom graphs
- **Recharts** - Standard charts

### Testing
- **Vitest** - Test runner
- **React Testing Library** - Component testing
- **MSW** - API mocking

## File Structure

```
frontend/src/
├── components/
│   ├── ui/              # Base components (Button, Card, etc.)
│   ├── layout/          # Layout components (Header, Sidebar, etc.)
│   └── common/          # Shared components (Search, Filters, etc.)
├── features/
│   ├── ai/              # AI-related features
│   ├── stories/         # Story features
│   ├── analytics/       # Analytics visualizations
│   ├── graph/           # Graph components
│   └── chat/            # Chat components
├── pages/
│   ├── home/            # Home page
│   ├── stories/         # Story pages
│   ├── initiatives/     # Initiative pages
│   ├── questions/       # Question pages
│   ├── analytics/       # Analytics pages
│   ├── graph/           # Graph explorer
│   └── chat/            # Chat page
├── hooks/               # Custom React hooks
├── lib/
│   ├── utils.ts         # Utility functions
│   └── constants.ts     # Constants
├── services/
│   └── api.ts           # API client
├── store/
│   └── appStore.ts      # Zustand store
├── types/
│   └── index.ts         # TypeScript types
├── styles/
│   └── globals.css      # Global styles
└── layouts/
    └── AppLayout.tsx    # Main layout

## Key Patterns

### API Query Hook Pattern
```typescript
export function useStories(filters?: SearchFilters) {
  return useQuery({
    queryKey: ['stories', filters],
    queryFn: () => narrativeAPI.searchStories(filters),
  });
}
```

### Page Component Pattern
```typescript
export function SomePage() {
  const { data, isLoading, error } = useSomeData();

  if (isLoading) return <PageLoader />;
  if (error) return <ErrorPage error={error} />;
  if (!data) return <EmptyState />;

  return (
    <div className="p-8">
      <h1>Page Title</h1>
      {/* Content */}
    </div>
  );
}
```

### Feature Component Pattern
```typescript
export function SomeFeature({ data }: Props) {
  const [localState, setLocalState] = useState();

  return (
    <Card>
      <CardHeader>
        <CardTitle>Feature Title</CardTitle>
      </CardHeader>
      <CardContent>
        {/* Feature content */}
      </CardContent>
    </Card>
  );
}
```

## Next Steps

1. **Complete all page placeholders** with proper exports
2. **Implement HomePage** with real data hooks
3. **Build Stories pages** with full functionality
4. **Implement AI Initiatives** management
5. **Build Strategic Questions** one by one
6. **Create Analytics visualizations**
7. **Build Graph Explorer** enhancements
8. **Implement Chat Interface**
9. **Add advanced features**
10. **Apply polish and testing**

## Estimated Timeline

- **Phase 2**: 3-4 days (Core Pages)
- **Phase 3**: 5-8 days (AI Features)
- **Phase 4**: 3-4 days (Analytics)
- **Phase 5**: 2-3 days (Graph)
- **Phase 6**: 2-3 days (Chat)
- **Phase 7**: 3-4 days (Advanced)
- **Phase 8**: 3-4 days (Polish)
- **Phase 9**: 1 day (Docs)

**Total**: 22-31 days for complete implementation

## Success Criteria

1. ✅ All backend endpoints integrated
2. ✅ All AI features accessible
3. ✅ Analytics visualizations functional
4. ✅ Chat interface working
5. ✅ Enterprise-grade UX
6. ✅ Accessibility compliant
7. ✅ Performance optimized
8. ✅ Fully tested
9. ✅ Well documented

---

This guide provides the complete roadmap for transforming the basic MVP into an enterprise-grade application that fully exposes the sophisticated AI narrative intelligence capabilities of the backend.
