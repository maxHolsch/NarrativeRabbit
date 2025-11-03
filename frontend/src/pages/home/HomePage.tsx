import { Link } from 'react-router-dom';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card';
import { Skeleton } from '../../components/ui/skeleton';
import { Badge } from '../../components/ui/badge';
import { BarChart3, Lightbulb, MessageSquare, Network, Activity, TrendingUp, AlertCircle, CheckCircle2 } from 'lucide-react';
import { useSystemHealth, useInitiatives, useRecentStories } from '../../hooks';

export function HomePage() {
  const { data: health, isLoading: healthLoading } = useSystemHealth();
  const { data: initiatives, isLoading: initiativesLoading } = useInitiatives();
  const { data: stories, isLoading: storiesLoading } = useRecentStories(30); // Increased from 5 to 30

  // Calculate metrics
  const totalStories = stories?.length || 0;
  const totalInitiatives = initiatives?.length || 0;
  const activeInitiatives = initiatives?.filter(i => i.status === 'active').length || 0;

  // Extract unique groups from stories
  const uniqueGroups = stories
    ? new Set(stories.flatMap(s => s.groups || []))
    : new Set();

  const stats = [
    {
      name: 'Total Stories',
      value: healthLoading ? '...' : totalStories.toString(),
      icon: Network,
      color: 'text-blue-500',
      trend: '+12 this week',
      loading: storiesLoading,
    },
    {
      name: 'AI Initiatives',
      value: initiativesLoading ? '...' : totalInitiatives.toString(),
      icon: Lightbulb,
      color: 'text-purple-500',
      trend: `${activeInitiatives} active`,
      loading: initiativesLoading,
    },
    {
      name: 'Active Groups',
      value: storiesLoading ? '...' : uniqueGroups.size.toString(),
      icon: BarChart3,
      color: 'text-green-500',
      trend: 'Across organization',
      loading: storiesLoading,
    },
    {
      name: 'System Status',
      value: healthLoading ? '...' : health?.status === 'healthy' ? 'Healthy' : 'Issues',
      icon: health?.status === 'healthy' ? CheckCircle2 : AlertCircle,
      color: health?.status === 'healthy' ? 'text-green-500' : 'text-yellow-500',
      trend: healthLoading ? '...' : `Neo4j ${health?.neo4j_status === 'connected' ? 'Connected' : 'Disconnected'}`,
      loading: healthLoading,
    },
  ];

  return (
    <div className="p-8 space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold tracking-tight">Narrative Intelligence Dashboard</h1>
        <p className="text-muted-foreground mt-2">
          Analyze organizational stories, AI initiatives, and cultural patterns
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <Card key={stat.name}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{stat.name}</CardTitle>
              <stat.icon className={`h-4 w-4 ${stat.color}`} />
            </CardHeader>
            <CardContent>
              {stat.loading ? (
                <Skeleton className="h-8 w-20" />
              ) : (
                <>
                  <div className="text-2xl font-bold">{stat.value}</div>
                  <p className="text-xs text-muted-foreground mt-1">{stat.trend}</p>
                </>
              )}
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Recent Activity */}
      <div className="grid gap-6 lg:grid-cols-2">
        {/* Recent Stories */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="flex items-center gap-2">
                  <Activity className="h-5 w-5" />
                  Recent Stories
                </CardTitle>
                <CardDescription>Latest narrative entries</CardDescription>
              </div>
              <Link to="/stories">
                <Badge variant="outline" className="cursor-pointer hover:bg-accent">
                  View All
                </Badge>
              </Link>
            </div>
          </CardHeader>
          <CardContent>
            {storiesLoading ? (
              <div className="space-y-3">
                {[...Array(3)].map((_, i) => (
                  <div key={i} className="space-y-2">
                    <Skeleton className="h-4 w-full" />
                    <Skeleton className="h-3 w-3/4" />
                  </div>
                ))}
              </div>
            ) : stories && stories.length > 0 ? (
              <div className="space-y-4">
                {stories.slice(0, 5).map((story) => (
                  <Link
                    key={story.id}
                    to={`/stories/${story.id}`}
                    className="block group"
                  >
                    <div className="flex items-start gap-3 p-3 rounded-lg hover:bg-accent transition-colors">
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium line-clamp-1 group-hover:text-primary">
                          {story.summary}
                        </p>
                        <div className="flex items-center gap-2 mt-1">
                          <Badge variant="secondary" className="text-xs">
                            {story.type}
                          </Badge>
                          {story.primary_themes?.slice(0, 2).map((theme) => (
                            <Badge key={theme} variant="outline" className="text-xs">
                              {theme}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            ) : (
              <p className="text-sm text-muted-foreground">No stories found</p>
            )}
          </CardContent>
        </Card>

        {/* Active Initiatives */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="h-5 w-5" />
                  Active Initiatives
                </CardTitle>
                <CardDescription>Current AI initiatives</CardDescription>
              </div>
              <Link to="/initiatives">
                <Badge variant="outline" className="cursor-pointer hover:bg-accent">
                  View All
                </Badge>
              </Link>
            </div>
          </CardHeader>
          <CardContent>
            {initiativesLoading ? (
              <div className="space-y-3">
                {[...Array(3)].map((_, i) => (
                  <div key={i} className="space-y-2">
                    <Skeleton className="h-4 w-full" />
                    <Skeleton className="h-3 w-2/3" />
                  </div>
                ))}
              </div>
            ) : initiatives && initiatives.length > 0 ? (
              <div className="space-y-4">
                {initiatives
                  .filter(i => i.status === 'active' || i.status === 'planned')
                  .slice(0, 5)
                  .map((initiative) => (
                    <Link
                      key={initiative.id}
                      to={`/initiatives/${initiative.id}`}
                      className="block group"
                    >
                      <div className="flex items-start gap-3 p-3 rounded-lg hover:bg-accent transition-colors">
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium line-clamp-1 group-hover:text-primary">
                            {initiative.name}
                          </p>
                          <div className="flex items-center gap-2 mt-1">
                            <Badge
                              variant={initiative.status === 'active' ? 'default' : 'secondary'}
                              className="text-xs"
                            >
                              {initiative.status}
                            </Badge>
                            <Badge variant="outline" className="text-xs">
                              {initiative.type}
                            </Badge>
                          </div>
                        </div>
                      </div>
                    </Link>
                  ))}
              </div>
            ) : (
              <p className="text-sm text-muted-foreground">No active initiatives</p>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Quick Links */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <Link to="/questions">
          <Card className="hover:shadow-lg transition-shadow cursor-pointer h-full">
            <CardHeader>
              <CardTitle>Strategic Questions</CardTitle>
              <CardDescription>
                Explore 5 core AI adoption questions and comprehensive analysis
              </CardDescription>
            </CardHeader>
          </Card>
        </Link>
        <Link to="/analytics">
          <Card className="hover:shadow-lg transition-shadow cursor-pointer h-full">
            <CardHeader>
              <CardTitle>Analytics Hub</CardTitle>
              <CardDescription>
                View frame competition, adoption timeline, and cultural signals
              </CardDescription>
            </CardHeader>
          </Card>
        </Link>
        <Link to="/graph">
          <Card className="hover:shadow-lg transition-shadow cursor-pointer h-full">
            <CardHeader>
              <CardTitle>Graph Explorer</CardTitle>
              <CardDescription>
                Visualize narrative relationships and AI concepts in Neo4j
              </CardDescription>
            </CardHeader>
          </Card>
        </Link>
      </div>
    </div>
  );
}
