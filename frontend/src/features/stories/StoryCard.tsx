import { Link } from 'react-router-dom';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Calendar, Users, Tag } from 'lucide-react';
import { Story } from '@/types';

interface StoryCardProps {
  story: Story;
}

export function StoryCard({ story }: StoryCardProps) {
  return (
    <Link to={`/stories/${story.id}`}>
      <Card className="h-full hover:shadow-lg transition-all duration-200 hover:border-primary/50 cursor-pointer">
        <CardHeader>
          <div className="flex items-start justify-between gap-2 mb-2">
            <Badge variant="secondary" className="capitalize">
              {story.type}
            </Badge>
            {story.timestamp && (
              <span className="text-xs text-muted-foreground flex items-center gap-1">
                <Calendar className="h-3 w-3" />
                {new Date(story.timestamp).toLocaleDateString()}
              </span>
            )}
          </div>
          <CardTitle className="line-clamp-2 text-lg">{story.summary}</CardTitle>
          {story.outcome && (
            <CardDescription className="line-clamp-2">{story.outcome}</CardDescription>
          )}
        </CardHeader>
        <CardContent>
          {/* Themes */}
          {story.primary_themes && story.primary_themes.length > 0 && (
            <div className="flex items-start gap-2 mb-3">
              <Tag className="h-4 w-4 text-muted-foreground mt-0.5 flex-shrink-0" />
              <div className="flex flex-wrap gap-1">
                {story.primary_themes.slice(0, 3).map((theme) => (
                  <Badge key={theme} variant="outline" className="text-xs">
                    {theme}
                  </Badge>
                ))}
                {story.primary_themes.length > 3 && (
                  <Badge variant="outline" className="text-xs">
                    +{story.primary_themes.length - 3}
                  </Badge>
                )}
              </div>
            </div>
          )}

          {/* Groups */}
          {story.groups && story.groups.length > 0 && (
            <div className="flex items-start gap-2">
              <Users className="h-4 w-4 text-muted-foreground mt-0.5 flex-shrink-0" />
              <div className="flex flex-wrap gap-1">
                {story.groups.slice(0, 2).map((group) => (
                  <Badge key={group} variant="outline" className="text-xs bg-primary/5">
                    {group}
                  </Badge>
                ))}
                {story.groups.length > 2 && (
                  <Badge variant="outline" className="text-xs bg-primary/5">
                    +{story.groups.length - 2}
                  </Badge>
                )}
              </div>
            </div>
          )}
        </CardContent>
        {story.lessons && story.lessons.length > 0 && (
          <CardFooter>
            <p className="text-xs text-muted-foreground">
              {story.lessons.length} lesson{story.lessons.length !== 1 ? 's' : ''} learned
            </p>
          </CardFooter>
        )}
      </Card>
    </Link>
  );
}
