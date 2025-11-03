import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import type { FilterState, GraphFilters, NodeType, StoryType } from '../types';

// ============================================================================
// App State Interface
// ============================================================================

interface AppState {
  // Theme
  theme: 'light' | 'dark';
  toggleTheme: () => void;
  setTheme: (theme: 'light' | 'dark') => void;

  // Sidebar
  sidebarCollapsed: boolean;
  toggleSidebar: () => void;
  setSidebarCollapsed: (collapsed: boolean) => void;

  // Filters
  filters: FilterState;
  setFilters: (filters: Partial<FilterState>) => void;
  resetFilters: () => void;

  // Graph Filters
  graphFilters: GraphFilters;
  setGraphFilters: (filters: Partial<GraphFilters>) => void;
  resetGraphFilters: () => void;

  // Selected Items
  selectedStoryId: string | null;
  setSelectedStoryId: (id: string | null) => void;

  selectedInitiativeId: string | null;
  setSelectedInitiativeId: (id: string | null) => void;

  // Search
  globalSearch: string;
  setGlobalSearch: (search: string) => void;
}

// ============================================================================
// Default Values
// ============================================================================

const defaultFilters: FilterState = {
  search: '',
  themes: [],
  groups: [],
  types: [],
  dateRange: {},
};

const defaultGraphFilters: GraphFilters = {
  nodeTypes: ['Story', 'Person', 'Group', 'Theme', 'Event'] as NodeType[],
  showRelationships: ['TELLS', 'ABOUT', 'INVOLVES', 'BELONGS_TO', 'EXEMPLIFIES'],
  layout: 'force',
  limit: 150,
};

// ============================================================================
// Store Definition
// ============================================================================

export const useAppStore = create<AppState>()(
  devtools(
    persist(
      (set) => ({
        // Theme
        theme: 'light',
        toggleTheme: () =>
          set((state) => ({ theme: state.theme === 'light' ? 'dark' : 'light' })),
        setTheme: (theme) => set({ theme }),

        // Sidebar
        sidebarCollapsed: false,
        toggleSidebar: () =>
          set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),
        setSidebarCollapsed: (collapsed) => set({ sidebarCollapsed: collapsed }),

        // Filters
        filters: defaultFilters,
        setFilters: (filters) =>
          set((state) => ({
            filters: { ...state.filters, ...filters },
          })),
        resetFilters: () => set({ filters: defaultFilters }),

        // Graph Filters
        graphFilters: defaultGraphFilters,
        setGraphFilters: (filters) =>
          set((state) => ({
            graphFilters: { ...state.graphFilters, ...filters },
          })),
        resetGraphFilters: () => set({ graphFilters: defaultGraphFilters }),

        // Selected Items
        selectedStoryId: null,
        setSelectedStoryId: (id) => set({ selectedStoryId: id }),

        selectedInitiativeId: null,
        setSelectedInitiativeId: (id) => set({ selectedInitiativeId: id }),

        // Search
        globalSearch: '',
        setGlobalSearch: (search) => set({ globalSearch: search }),
      }),
      {
        name: 'narrative-app-storage',
        partialize: (state) => ({
          theme: state.theme,
          sidebarCollapsed: state.sidebarCollapsed,
          filters: state.filters,
          graphFilters: state.graphFilters,
        }),
      }
    ),
    { name: 'NarrativeApp' }
  )
);
