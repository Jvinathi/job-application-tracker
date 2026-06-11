import { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import KanbanBoard from '../components/KanbanBoard';
import StatsPanel from '../components/StatsPanel';
import axiosClient from '../api/axiosClient';

export default function Dashboard() {
  const [stats, setStats] = useState(null);

  const fetchStats = async () => {
    try {
      const res = await axiosClient.get('/stats/');
      setStats(res.data);
    } catch (err) {
      console.error('Stats error:', err);
    }
  };

  useEffect(() => { fetchStats(); }, []);

  return (
    <div className="min-h-screen bg-slate-900">
      <Navbar />
      <div className="max-w-screen-2xl mx-auto px-6 py-8">
        <StatsPanel stats={stats} />
        <KanbanBoard onStatsChange={fetchStats} />
      </div>
    </div>
  );
}