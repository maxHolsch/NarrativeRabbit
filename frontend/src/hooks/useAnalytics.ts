import { useQuery } from '@tanstack/react-query';
import { aiAnalyticsAPI } from '@/services/api';

export function useSentimentByGroup() {
  return useQuery({
    queryKey: ['analytics', 'sentiment-by-group'],
    queryFn: () => aiAnalyticsAPI.getSentimentByGroup(),
    staleTime: 1000 * 60 * 10, // 10 minutes
  });
}

export function useFrameDistribution() {
  return useQuery({
    queryKey: ['analytics', 'frame-distribution'],
    queryFn: () => aiAnalyticsAPI.getFrameDistribution(),
    staleTime: 1000 * 60 * 10,
  });
}

export function useAdoptionTimeline(params?: { start_date?: string; end_date?: string; group?: string }) {
  return useQuery({
    queryKey: ['analytics', 'adoption-timeline', params],
    queryFn: () => aiAnalyticsAPI.getAdoptionTimeline(params),
    staleTime: 1000 * 60 * 10,
  });
}

export function useGroupConnectivity() {
  return useQuery({
    queryKey: ['analytics', 'group-connectivity'],
    queryFn: () => aiAnalyticsAPI.getGroupConnectivity(),
    staleTime: 1000 * 60 * 10,
  });
}
