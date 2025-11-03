import { useState, useMemo, useCallback } from 'react';
import { useStories } from '@/hooks';
import { StoryCard, StoryFilters } from '@/features/stories';
import { Skeleton } from '@/components/ui/skeleton';
import { Button } from '@/components/ui/button';
import { BookOpen, AlertCircle } from 'lucide-react';

export function StoriesListPage() {
  const [filters, setFilters] = useState({
    search: '',
    themes: [] as string[],
    groups: [] as string[],
    types: [] as string[],
  });

  // Fetch all stories (we'll filter client-side for better UX)
  const { data: stories, isLoading, error } = useStories({ limit: 100 });

  // Extract available themes and groups
  const { availableThemes, availableGroups } = useMemo(() => {
    if (!stories) return { availableThemes: [], availableGroups: [] };

    const themes = new Set<string>();
    const groups = new Set<string>();

    stories.forEach(story => {
      story.primary_themes?.forEach(theme => themes.add(theme));
      story.groups?.forEach(group => groups.add(group));
    });

    return {
      availableThemes: Array.from(themes).sort(),
      availableGroups: Array.from(groups).sort(),
    };
  }, [stories]);

  // Filter stories based on current filters
  const filteredStories = useMemo(() => {
    if (!stories) return [];

    return stories.filter(story => {
      // Search filter
      if (filters.search) {
        const searchLower = filters.search.toLowerCase();
        const matchesSearch =
          story.summary?.toLowerCase().includes(searchLower) ||
          story.outcome?.toLowerCase().includes(searchLower) ||
          story.full_text?.toLowerCase().includes(searchLower);
        if (!matchesSearch) return false;
      }

      // Type filter
      if (filters.types.length > 0 && !filters.types.includes(story.type)) {
        return false;
      }

      // Theme filter
      if (filters.themes.length > 0) {
        const hasTheme = story.primary_themes?.some(theme =>
          filters.themes.includes(theme)
        );
        if (!hasTheme) return false;
      }

      // Group filter
      if (filters.groups.length > 0) {
        const hasGroup = story.groups?.some(group =>
          filters.groups.includes(group)
        );
        if (!hasGroup) return false;
      }

      return true;
    });
  }, [stories, filters]);

  const handleFilterChange = useCallback((newFilters: typeof filters) => {
    setFilters(newFilters);
  }, []);

  if (error) {
    return (
      <div className="p-8">
        <div className="flex flex-col items-center justify-center min-h-[400px] text-center">
          <AlertCircle className="h-12 w-12 text-destructive mb-4" />
          <h2 className="text-2xl font-bold mb-2">Error Loading Stories</h2>
          <p className="text-muted-foreground mb-4">
            {error instanceof Error ? error.message : 'Failed to load stories'}
          </p>
          <Button onClick={() => window.location.reload()}>Retry</Button>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-2 mb-2">
          <BookOpen className="h-8 w-8" />
          <h1 className="text-4xl font-bold tracking-tight">Stories</h1>
        </div>
        <p className="text-muted-foreground">
          Browse and search organizational narratives
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Filters Sidebar */}
        <div className="lg:col-span-1">
          <div className="sticky top-8">
            {isLoading ? (
              <Skeleton className="h-96" />
            ) : (
              <StoryFilters
                onFilterChange={handleFilterChange}
                availableThemes={availableThemes}
                availableGroups={availableGroups}
              />
            )}
          </div>
        </div>

        {/* Stories Grid */}
        <div className="lg:col-span-3">
          {/* Results Count */}
          {!isLoading && (
            <div className="mb-4 flex items-center justify-between">
              <p className="text-sm text-muted-foreground">
                {filteredStories.length} {filteredStories.length === 1 ? 'story' : 'stories'} found
              </p>
            </div>
          )}

          {/* Loading State */}
          {isLoading && (
            <div className="grid gap-6 md:grid-cols-2">
              {[...Array(6)].map((_, i) => (
                <Skeleton key={i} className="h-64" />
              ))}
            </div>
          )}

          {/* Stories Grid */}
          {!isLoading && filteredStories.length > 0 && (
            <div className="grid gap-6 md:grid-cols-2">
              {filteredStories.map((story) => (
                <StoryCard key={story.id} story={story} />
              ))}
            </div>
          )}

          {/* Empty State */}
          {!isLoading && filteredStories.length === 0 && (
            <div className="flex flex-col items-center justify-center min-h-[400px] text-center border-2 border-dashed rounded-lg p-8">
              <BookOpen className="h-12 w-12 text-muted-foreground mb-4" />
              <h3 className="text-xl font-semibold mb-2">No stories found</h3>
              <p className="text-muted-foreground mb-4">
                {filters.search || filters.themes.length > 0 || filters.groups.length > 0 || filters.types.length > 0
                  ? 'Try adjusting your filters to see more results'
                  : 'No stories available in the database'}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
