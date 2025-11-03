import { Outlet, Link, useLocation } from 'react-router-dom';
import { useAppStore } from '../store/appStore';
import {
  Home,
  BookOpen,
  Lightbulb,
  HelpCircle,
  BarChart3,
  Network,
  MessageSquare,
  Menu,
  Moon,
  Sun
} from 'lucide-react';
import { Button } from '../components/ui/button';
import { cn } from '../lib/utils';

export function AppLayout() {
  const location = useLocation();
  const { sidebarCollapsed, toggleSidebar, theme, toggleTheme } = useAppStore();

  const navigation = [
    { name: 'Home', href: '/', icon: Home },
    { name: 'Stories', href: '/stories', icon: BookOpen },
    { name: 'AI Initiatives', href: '/initiatives', icon: Lightbulb },
    { name: 'Strategic Questions', href: '/questions', icon: HelpCircle },
    { name: 'Analytics', href: '/analytics', icon: BarChart3 },
    { name: 'Graph Explorer', href: '/graph', icon: Network },
    { name: 'Chat', href: '/chat', icon: MessageSquare },
  ];

  const isActive = (href: string) => {
    if (href === '/') return location.pathname === '/';
    return location.pathname.startsWith(href);
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Sidebar */}
      <aside
        className={cn(
          'fixed left-0 top-0 z-40 h-screen bg-card border-r transition-all duration-300',
          sidebarCollapsed ? 'w-16' : 'w-64'
        )}
      >
        <div className="flex h-full flex-col">
          {/* Logo */}
          <div className="flex h-16 items-center justify-between border-b px-4">
            {!sidebarCollapsed && (
              <Link to="/" className="flex items-center space-x-2">
                <Network className="h-6 w-6 text-primary" />
                <span className="font-semibold text-lg">Narrative AI</span>
              </Link>
            )}
            <Button
              variant="ghost"
              size="icon"
              onClick={toggleSidebar}
              className={cn(sidebarCollapsed && "mx-auto")}
            >
              <Menu className="h-5 w-5" />
            </Button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 space-y-1 p-2">
            {navigation.map((item) => {
              const Icon = item.icon;
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={cn(
                    'flex items-center space-x-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors',
                    isActive(item.href)
                      ? 'bg-primary text-primary-foreground'
                      : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground',
                    sidebarCollapsed && 'justify-center'
                  )}
                  title={sidebarCollapsed ? item.name : ''}
                >
                  <Icon className="h-5 w-5 flex-shrink-0" />
                  {!sidebarCollapsed && <span>{item.name}</span>}
                </Link>
              );
            })}
          </nav>

          {/* Theme Toggle */}
          <div className="border-t p-2">
            <Button
              variant="ghost"
              size="icon"
              onClick={toggleTheme}
              className={cn('w-full', sidebarCollapsed ? 'px-0' : 'justify-start px-3')}
            >
              {theme === 'light' ? (
                <>
                  <Moon className="h-5 w-5" />
                  {!sidebarCollapsed && <span className="ml-3">Dark Mode</span>}
                </>
              ) : (
                <>
                  <Sun className="h-5 w-5" />
                  {!sidebarCollapsed && <span className="ml-3">Light Mode</span>}
                </>
              )}
            </Button>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main
        className={cn(
          'transition-all duration-300',
          sidebarCollapsed ? 'ml-16' : 'ml-64'
        )}
      >
        <Outlet />
      </main>
    </div>
  );
}
