import { useQuery } from '@tanstack/react-query';
import { narrativeAPI } from '@/services/api';

interface UseStoriesParams {
  themes?: string[];
  groups?: string[];
  story_type?: string;
  limit?: number;
}

export function useStories(params?: UseStoriesParams) {
  return useQuery({
    queryKey: ['stories', params],
    queryFn: () => narrativeAPI.searchStories(params || {}),
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
}

export function useStory(storyId: string | undefined) {
  return useQuery({
    queryKey: ['stories', storyId],
    queryFn: () => narrativeAPI.getStory(storyId!),
    enabled: !!storyId,
    staleTime: 1000 * 60 * 5,
  });
}

export function useRecentStories(limit = 5) {
  return useQuery({
    queryKey: ['stories', 'recent', limit],
    queryFn: async () => {
      console.log(`🔍 [useRecentStories] Fetching ${limit} recent stories...`);
      const data = await narrativeAPI.searchStories({ limit });
      console.log(`✅ [useRecentStories] Received ${data?.length || 0} stories`);
      return data;
    },
    staleTime: 0, // Always fetch fresh data
    refetchOnMount: true,
  });
}
