import { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Send, Trash2, MessageSquare, Loader2, ExternalLink } from 'lucide-react';
import { useChat } from '../../hooks';
import { Card, CardContent } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';

export function ChatPage() {
  const { messages, isLoading, sendMessage, clearMessages, sources, suggestedFollowups } = useChat();
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Focus input on mount
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const message = input;
    setInput('');
    await sendMessage(message);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleFollowupClick = (followup: string) => {
    setInput(followup);
    inputRef.current?.focus();
  };

  // Quick action buttons
  const quickActions = [
    "Show me recent AI stories",
    "Are we risk-averse?",
    "Tell me about active initiatives",
    "How do different teams view AI?",
  ];

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)] p-4 max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-2">
            <MessageSquare className="h-8 w-8" />
            AI Chat Interface
          </h1>
          <p className="text-muted-foreground mt-1">
            Ask questions about the narrative knowledge graph
          </p>
        </div>
        {messages.length > 0 && (
          <Button
            onClick={clearMessages}
            variant="outline"
            size="sm"
            className="flex items-center gap-2"
          >
            <Trash2 className="h-4 w-4" />
            Clear Chat
          </Button>
        )}
      </div>

      {/* Messages Container */}
      <Card className="flex-1 flex flex-col overflow-hidden">
        <CardContent className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center space-y-6">
              <div className="space-y-2">
                <h2 className="text-2xl font-semibold">Welcome to the Narrative Intelligence Chat</h2>
                <p className="text-muted-foreground max-w-md">
                  I can help you explore stories, analyze patterns, and answer questions about your organization's
                  narrative graph.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 w-full max-w-2xl">
                {quickActions.map((action, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleFollowupClick(action)}
                    className="p-4 text-left border rounded-lg hover:bg-accent transition-colors"
                  >
                    <p className="text-sm font-medium">{action}</p>
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <>
              {messages.map((message, idx) => (
                <div
                  key={message.id}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[80%] rounded-lg px-4 py-3 ${
                      message.role === 'user'
                        ? 'bg-primary text-primary-foreground'
                        : 'bg-muted'
                    }`}
                  >
                    <p className="whitespace-pre-wrap text-sm">{message.content}</p>
                    <p className="text-xs mt-2 opacity-70">
                      {message.timestamp.toLocaleTimeString()}
                    </p>
                  </div>
                </div>
              ))}

              {/* Loading Indicator */}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-muted rounded-lg px-4 py-3 flex items-center gap-2">
                    <Loader2 className="h-4 w-4 animate-spin" />
                    <span className="text-sm text-muted-foreground">Thinking...</span>
                  </div>
                </div>
              )}

              {/* Sources Section */}
              {!isLoading && sources.length > 0 && (
                <div className="flex justify-start">
                  <Card className="max-w-[80%] bg-accent/50">
                    <CardContent className="p-4 space-y-2">
                      <h4 className="text-sm font-semibold flex items-center gap-2">
                        <ExternalLink className="h-4 w-4" />
                        Sources
                      </h4>
                      <div className="space-y-1">
                        {sources.map((source, idx) => (
                          <Link
                            key={idx}
                            to={source.type === 'story' ? `/stories/${source.id}` : `/initiatives/${source.id}`}
                            className="block text-xs text-primary hover:underline"
                          >
                            [{source.type}] {source.label}
                          </Link>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                </div>
              )}

              {/* Follow-up Suggestions */}
              {!isLoading && suggestedFollowups.length > 0 && (
                <div className="flex flex-wrap gap-2 justify-start">
                  {suggestedFollowups.map((followup, idx) => (
                    <button
                      key={idx}
                      onClick={() => handleFollowupClick(followup)}
                      className="text-xs px-3 py-1.5 rounded-full border hover:bg-accent transition-colors"
                    >
                      {followup}
                    </button>
                  ))}
                </div>
              )}

              <div ref={messagesEndRef} />
            </>
          )}
        </CardContent>
      </Card>

      {/* Input Area */}
      <div className="mt-4 flex gap-2">
        <div className="flex-1 relative">
          <textarea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask a question about the narrative graph... (Shift+Enter for new line)"
            disabled={isLoading}
            className="w-full min-h-[60px] max-h-[200px] resize-y px-4 py-3 rounded-lg border bg-background focus:outline-none focus:ring-2 focus:ring-ring disabled:opacity-50"
            rows={2}
          />
        </div>
        <Button
          onClick={handleSend}
          disabled={!input.trim() || isLoading}
          size="lg"
          className="h-[60px] px-6"
        >
          {isLoading ? (
            <Loader2 className="h-5 w-5 animate-spin" />
          ) : (
            <Send className="h-5 w-5" />
          )}
        </Button>
      </div>

      {/* Tips */}
      <div className="mt-3 text-xs text-muted-foreground text-center">
        <p>
          Press <Badge variant="outline" className="mx-1">Enter</Badge> to send •{' '}
          <Badge variant="outline" className="mx-1">Shift+Enter</Badge> for new line
        </p>
      </div>
    </div>
  );
}
