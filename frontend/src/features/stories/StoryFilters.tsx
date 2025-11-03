import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Search, X, Filter } from 'lucide-react';
import { STORY_TYPES } from '@/lib/constants';

interface StoryFiltersProps {
  onFilterChange: (filters: {
    search: string;
    themes: string[];
    groups: string[];
    types: string[];
  }) => void;
  availableThemes?: string[];
  availableGroups?: string[];
}

export function StoryFilters({ onFilterChange, availableThemes = [], availableGroups = [] }: StoryFiltersProps) {
  const [search, setSearch] = useState('');
  const [selectedThemes, setSelectedThemes] = useState<string[]>([]);
  const [selectedGroups, setSelectedGroups] = useState<string[]>([]);
  const [selectedTypes, setSelectedTypes] = useState<string[]>([]);

  useEffect(() => {
    onFilterChange({
      search,
      themes: selectedThemes,
      groups: selectedGroups,
      types: selectedTypes,
    });
  }, [search, selectedThemes, selectedGroups, selectedTypes, onFilterChange]);

  const toggleTheme = (theme: string) => {
    setSelectedThemes(prev =>
      prev.includes(theme) ? prev.filter(t => t !== theme) : [...prev, theme]
    );
  };

  const toggleGroup = (group: string) => {
    setSelectedGroups(prev =>
      prev.includes(group) ? prev.filter(g => g !== group) : [...prev, group]
    );
  };

  const toggleType = (type: string) => {
    setSelectedTypes(prev =>
      prev.includes(type) ? prev.filter(t => t !== type) : [...prev, type]
    );
  };

  const clearAll = () => {
    setSearch('');
    setSelectedThemes([]);
    setSelectedGroups([]);
    setSelectedTypes([]);
  };

  const hasActiveFilters = search || selectedThemes.length > 0 || selectedGroups.length > 0 || selectedTypes.length > 0;

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Filter className="h-5 w-5" />
            <CardTitle>Filters</CardTitle>
          </div>
          {hasActiveFilters && (
            <Button variant="ghost" size="sm" onClick={clearAll}>
              <X className="h-4 w-4 mr-1" />
              Clear
            </Button>
          )}
        </div>
        <CardDescription>Filter stories by type, theme, or group</CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Search */}
        <div>
          <label className="text-sm font-medium mb-2 block">Search</label>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search stories..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-9"
            />
          </div>
        </div>

        {/* Story Types */}
        <div>
          <label className="text-sm font-medium mb-2 block">Story Type</label>
          <div className="flex flex-wrap gap-2">
            {STORY_TYPES.map((type) => (
              <Badge
                key={type}
                variant={selectedTypes.includes(type) ? 'default' : 'outline'}
                className="cursor-pointer capitalize"
                onClick={() => toggleType(type)}
              >
                {type}
              </Badge>
            ))}
          </div>
        </div>

        {/* Themes */}
        {availableThemes.length > 0 && (
          <div>
            <label className="text-sm font-medium mb-2 block">
              Themes ({availableThemes.length})
            </label>
            <div className="flex flex-wrap gap-2 max-h-48 overflow-y-auto">
              {availableThemes.map((theme) => (
                <Badge
                  key={theme}
                  variant={selectedThemes.includes(theme) ? 'default' : 'outline'}
                  className="cursor-pointer"
                  onClick={() => toggleTheme(theme)}
                >
                  {theme}
                </Badge>
              ))}
            </div>
          </div>
        )}

        {/* Groups */}
        {availableGroups.length > 0 && (
          <div>
            <label className="text-sm font-medium mb-2 block">
              Groups ({availableGroups.length})
            </label>
            <div className="flex flex-wrap gap-2 max-h-48 overflow-y-auto">
              {availableGroups.map((group) => (
                <Badge
                  key={group}
                  variant={selectedGroups.includes(group) ? 'default' : 'outline'}
                  className="cursor-pointer"
                  onClick={() => toggleGroup(group)}
                >
                  {group}
                </Badge>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
