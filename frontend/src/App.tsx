import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useEffect } from 'react';
import { useAppStore } from './store/appStore';
import { AppLayout } from './layouts/AppLayout';

// Pages
import { HomePage } from './pages/home/HomePage';
import { StoriesListPage } from './pages/stories/StoriesListPage';
import { StoryDetailPage } from './pages/stories/StoryDetailPage';
import { InitiativesListPage } from './pages/initiatives/InitiativesListPage';
import { InitiativeDetailPage } from './pages/initiatives/InitiativeDetailPage';
import { InitiativeCreatePage } from './pages/initiatives/InitiativeCreatePage';
import { QuestionsHubPage } from './pages/questions/QuestionsHubPage';
import { Question1Page } from './pages/questions/Question1Page';
import { Question2Page } from './pages/questions/Question2Page';
import { Question3Page } from './pages/questions/Question3Page';
import { Question4Page } from './pages/questions/Question4Page';
import { Question5Page } from './pages/questions/Question5Page';
import { AnalyticsHubPage } from './pages/analytics/AnalyticsHubPage';
import { GraphExplorerPage } from './pages/graph/GraphExplorerPage';
import { ChatPage } from './pages/chat/ChatPage';

function App() {
  const { theme } = useAppStore();

  // Apply theme to document
  useEffect(() => {
    const root = window.document.documentElement;
    root.classList.remove('light', 'dark');
    root.classList.add(theme);
  }, [theme]);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AppLayout />}>
          {/* Home */}
          <Route index element={<HomePage />} />

          {/* Stories */}
          <Route path="stories" element={<StoriesListPage />} />
          <Route path="stories/:id" element={<StoryDetailPage />} />

          {/* AI Initiatives */}
          <Route path="initiatives" element={<InitiativesListPage />} />
          <Route path="initiatives/new" element={<InitiativeCreatePage />} />
          <Route path="initiatives/:id" element={<InitiativeDetailPage />} />

          {/* Strategic Questions */}
          <Route path="questions" element={<QuestionsHubPage />} />
          <Route path="questions/1" element={<Question1Page />} />
          <Route path="questions/2" element={<Question2Page />} />
          <Route path="questions/3" element={<Question3Page />} />
          <Route path="questions/4" element={<Question4Page />} />
          <Route path="questions/5" element={<Question5Page />} />

          {/* Analytics */}
          <Route path="analytics" element={<AnalyticsHubPage />} />

          {/* Graph Explorer */}
          <Route path="graph" element={<GraphExplorerPage />} />

          {/* Chat */}
          <Route path="chat" element={<ChatPage />} />

          {/* 404 redirect */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
