import { useState, useCallback } from 'react';
import { chatAPI } from '../services/api';
import type { ChatMessage, ChatSource } from '../types';

interface UseChatReturn {
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
  sendMessage: (content: string) => Promise<void>;
  clearMessages: () => void;
  sources: ChatSource[];
  suggestedFollowups: string[];
}

export function useChat(): UseChatReturn {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [sources, setSources] = useState<ChatSource[]>([]);
  const [suggestedFollowups, setSuggestedFollowups] = useState<string[]>([]);

  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim()) return;

    // Add user message immediately
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: content.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      console.log('📤 [useChat] Sending message:', content);

      // Build conversation history (last 10 messages)
      const history = messages.slice(-10).map(msg => ({
        role: msg.role,
        content: msg.content
      }));

      // Send to API
      const response = await chatAPI.sendMessage({
        message: content,
        conversation_id: conversationId || undefined,
        conversation_history: history,
      });

      console.log('📥 [useChat] Received response:', response);

      // Update conversation ID
      if (response.conversation_id && !conversationId) {
        setConversationId(response.conversation_id);
      }

      // Add assistant message
      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.response,
        timestamp: new Date(),
        metadata: {
          intent: response.intent,
          dataSummary: response.data_summary,
        },
      };

      setMessages(prev => [...prev, assistantMessage]);

      // Update sources and follow-ups
      setSources(response.sources || []);
      setSuggestedFollowups(response.suggested_followups || []);

    } catch (err) {
      console.error('❌ [useChat] Error sending message:', err);
      const errorMessage = err instanceof Error ? err.message : 'Failed to send message';
      setError(errorMessage);

      // Add error message to chat
      const errorMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `Sorry, I encountered an error: ${errorMessage}. Please try again.`,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  }, [messages, conversationId]);

  const clearMessages = useCallback(() => {
    setMessages([]);
    setConversationId(null);
    setSources([]);
    setSuggestedFollowups([]);
    setError(null);
  }, []);

  return {
    messages,
    isLoading,
    error,
    sendMessage,
    clearMessages,
    sources,
    suggestedFollowups,
  };
}
