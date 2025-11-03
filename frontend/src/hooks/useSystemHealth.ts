import { useQuery } from '@tanstack/react-query';
import { systemAPI } from '@/services/api';

export function useSystemHealth() {
  return useQuery({
    queryKey: ['system', 'health'],
    queryFn: () => systemAPI.getHealth(),
    staleTime: 1000 * 60, // 1 minute
    refetchInterval: 1000 * 60 * 5, // Refetch every 5 minutes
  });
}

export function useAIHealth() {
  return useQuery({
    queryKey: ['ai', 'health'],
    queryFn: () => systemAPI.getAIHealth(),
    staleTime: 1000 * 60,
    refetchInterval: 1000 * 60 * 5,
  });
}
