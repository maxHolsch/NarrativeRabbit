import { useQuery } from '@tanstack/react-query';
import { aiInitiativeAPI } from '@/services/api';

export function useInitiatives() {
  return useQuery({
    queryKey: ['initiatives'],
    queryFn: () => aiInitiativeAPI.getAllInitiatives(),
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
}

export function useInitiative(initiativeId: string | undefined) {
  return useQuery({
    queryKey: ['initiatives', initiativeId],
    queryFn: () => aiInitiativeAPI.getInitiative(initiativeId!),
    enabled: !!initiativeId,
    staleTime: 1000 * 60 * 5,
  });
}
