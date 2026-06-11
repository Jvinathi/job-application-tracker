import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

export default function StatsPanel({ stats }) {
  if (!stats) return null;

  const statCards = [
    { label: 'Total Applied', value: stats.total, color: 'text-blue-400' },
    { label: 'Response Rate', value: `${stats.response_rate}%`, color: 'text-yellow-400' },
    { label: 'Offer Rate', value: `${stats.offer_rate}%`, color: 'text-green-400' },
    { label: 'Interviews', value: stats.interview, color: 'text-purple-400' },
  ];

  const COLORS = ['#3b82f6', '#eab308', '#a855f7', '#22c55e', '#ef4444'];

  const pipelineData = [
    { name: 'Applied', value: stats.applied },
    { name: 'Shortlisted', value: stats.shortlisted },
    { name: 'Interview', value: stats.interview },
    { name: 'Offer', value: stats.offer },
    { name: 'Rejected', value: stats.rejected },
  ];

  return (
    <div className="bg-slate-800 rounded-2xl p-6 mb-6">
      <h2 className="text-lg font-semibold text-white mb-4">Pipeline Overview</h2>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        {statCards.map((card) => (
          <div key={card.label} className="bg-slate-700 rounded-xl p-4">
            <p className="text-slate-400 text-xs mb-1">{card.label}</p>
            <p className={`text-2xl font-bold ${card.color}`}>{card.value}</p>
          </div>
        ))}
      </div>
      <ResponsiveContainer width="100%" height={160}>
        <BarChart data={pipelineData}>
          <XAxis dataKey="name" tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={false} tickLine={false} />
          <YAxis tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={false} tickLine={false} />
          <Tooltip
            contentStyle={{ background: '#1e293b', border: 'none', borderRadius: '8px', color: '#f1f5f9' }}
          />
          <Bar dataKey="value" radius={[4, 4, 0, 0]}>
            {pipelineData.map((_, index) => (
              <Cell key={index} fill={COLORS[index]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}