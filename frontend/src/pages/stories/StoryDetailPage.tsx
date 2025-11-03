import { useParams, Link } from 'react-router-dom';
import { useStory } from '@/hooks';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import {
  ArrowLeft,
  Calendar,
  Users,
  Tag,
  Lightbulb,
  AlertCircle,
  BookOpen,
  Target,
} from 'lucide-react';

export function StoryDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { data: story, isLoading, error } = useStory(id);

  if (error) {
    return (
      <div className="p-8">
        <div className="flex flex-col items-center justify-center min-h-[400px] text-center">
          <AlertCircle className="h-12 w-12 text-destructive mb-4" />
          <h2 className="text-2xl font-bold mb-2">Error Loading Story</h2>
          <p className="text-muted-foreground mb-4">
            {error instanceof Error ? error.message : 'Failed to load story'}
          </p>
          <Link to="/stories">
            <Button>Back to Stories</Button>
          </Link>
        </div>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="p-8">
        <Skeleton className="h-8 w-32 mb-6" />
        <div className="space-y-6">
          <Skeleton className="h-64" />
          <Skeleton className="h-48" />
          <Skeleton className="h-48" />
        </div>
      </div>
    );
  }

  if (!story) {
    return (
      <div className="p-8">
        <div className="flex flex-col items-center justify-center min-h-[400px] text-center">
          <BookOpen className="h-12 w-12 text-muted-foreground mb-4" />
          <h2 className="text-2xl font-bold mb-2">Story Not Found</h2>
          <p className="text-muted-foreground mb-4">
            The story you're looking for doesn't exist or has been removed.
          </p>
          <Link to="/stories">
            <Button>Back to Stories</Button>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8 max-w-6xl mx-auto">
      {/* Back Button */}
      <Link to="/stories">
        <Button variant="ghost" className="mb-6">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Stories
        </Button>
      </Link>

      {/* Header */}
      <div className="mb-8">
        <div className="flex items-start justify-between gap-4 mb-4">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <Badge variant="secondary" className="capitalize">
                {story.type}
              </Badge>
              {story.timestamp && (
                <span className="text-sm text-muted-foreground flex items-center gap-1">
                  <Calendar className="h-4 w-4" />
                  {new Date(story.timestamp).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                  })}
                </span>
              )}
            </div>
            <h1 className="text-4xl font-bold tracking-tight mb-2">{story.summary}</h1>
            {story.outcome && (
              <p className="text-lg text-muted-foreground">{story.outcome}</p>
            )}
          </div>
        </div>

        {/* Metadata Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
          {/* Themes */}
          {story.primary_themes && story.primary_themes.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center gap-2">
                  <Tag className="h-4 w-4" />
                  Themes
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {story.primary_themes.map((theme) => (
                    <Badge key={theme} variant="outline">
                      {theme}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Groups */}
          {story.groups && story.groups.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center gap-2">
                  <Users className="h-4 w-4" />
                  Groups
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {story.groups.map((group) => (
                    <Badge key={group} variant="outline" className="bg-primary/5">
                      {group}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>

      {/* Full Text */}
      {story.full_text && (
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Full Story</CardTitle>
            <CardDescription>Complete narrative details</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-base leading-relaxed whitespace-pre-wrap">{story.full_text}</p>
          </CardContent>
        </Card>
      )}

      {/* Lessons Learned */}
      {story.lessons && story.lessons.length > 0 && (
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Lightbulb className="h-5 w-5" />
              Lessons Learned
            </CardTitle>
            <CardDescription>{story.lessons.length} key takeaways</CardDescription>
          </CardHeader>
          <CardContent>
            <ul className="space-y-3">
              {story.lessons.map((lesson, index) => (
                <li key={index} className="flex items-start gap-3">
                  <span className="flex-shrink-0 w-6 h-6 rounded-full bg-primary/10 text-primary flex items-center justify-center text-sm font-medium">
                    {index + 1}
                  </span>
                  <p className="text-base pt-0.5">{lesson}</p>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}

      {/* Context and Outcome Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        {/* Context */}
        {story.context && (
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Context</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">{story.context}</p>
            </CardContent>
          </Card>
        )}

        {/* Decision Made */}
        {story.decision_made && (
          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <Target className="h-4 w-4" />
                Decision Made
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">{story.decision_made}</p>
            </CardContent>
          </Card>
        )}
      </div>

      {/* Related Entities */}
      {((story.people && story.people.length > 0) ||
        (story.events && story.events.length > 0) ||
        (story.values && story.values.length > 0)) && (
        <Card>
          <CardHeader>
            <CardTitle>Related Entities</CardTitle>
            <CardDescription>People, events, and values connected to this story</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {story.people && story.people.length > 0 && (
                <div>
                  <h4 className="text-sm font-medium mb-2">People</h4>
                  <div className="flex flex-wrap gap-2">
                    {story.people.map((person) => (
                      <Badge key={person} variant="secondary">
                        {person}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}

              {story.events && story.events.length > 0 && (
                <div>
                  <h4 className="text-sm font-medium mb-2">Events</h4>
                  <div className="flex flex-wrap gap-2">
                    {story.events.map((event) => (
                      <Badge key={event} variant="secondary">
                        {event}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}

              {story.values && story.values.length > 0 && (
                <div>
                  <h4 className="text-sm font-medium mb-2">Values</h4>
                  <div className="flex flex-wrap gap-2">
                    {story.values.map((value) => (
                      <Badge key={value} variant="secondary">
                        {value}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
