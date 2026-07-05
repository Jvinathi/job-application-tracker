import { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import axiosClient from '../api/axiosClient';
import toast from 'react-hot-toast';
import { format } from 'date-fns';

const REMINDER_TYPES = ['follow_up', 'interview_prep', 'deadline'];

export default function Reminders() {
  const [reminders, setReminders] = useState([]);
  const [applications, setApplications] = useState([]);
  const [form, setForm] = useState({ application_id: '', reminder_type: 'follow_up', remind_at: '', note: '' });

  useEffect(() => {
    axiosClient.get('/reminders/').then(r => setReminders(r.data)).catch(() => {});
    axiosClient.get('/applications/').then(r => setApplications(r.data)).catch(() => {});
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      // Convert local datetime to UTC before sending to backend
      // e.g. 1:55 PM IST → 8:25 AM UTC
      const localDate = new Date(form.remind_at);
      const utcString = localDate.toISOString().slice(0, 16); // "2026-07-05T08:25"

      const res = await axiosClient.post('/reminders/', {
        ...form,
        application_id: parseInt(form.application_id),
        remind_at: utcString,   // ← send UTC to backend
      });
      setReminders(prev => [...prev, res.data]);
      toast.success('Reminder set!');
      setForm({ application_id: '', reminder_type: 'follow_up', remind_at: '', note: '' });
    } catch {
      toast.error('Failed to create reminder');
    }
  };

  const handleDelete = async (id) => {
    try {
      await axiosClient.delete(`/reminders/${id}`);
      setReminders(prev => prev.filter(r => r.id !== id));
      toast.success('Reminder deleted');
    } catch {
      toast.error('Delete failed');
    }
  };

  const getAppName = (id) => {
    const app = applications.find(a => a.id === id);
    return app ? `${app.company_name} — ${app.role_title}` : 'Unknown';
  };

  return (
    <div className="min-h-screen bg-slate-900">
      <Navbar />
      <div className="max-w-3xl mx-auto px-6 py-8">
        <h1 className="text-2xl font-bold text-white mb-6">Follow-up Reminders</h1>
        <div className="bg-slate-800 rounded-2xl p-6 mb-8">
          <h2 className="text-lg font-semibold text-white mb-4">Set New Reminder</h2>
          <form onSubmit={handleCreate} className="space-y-4">
            <div>
              <label className="block text-sm text-slate-300 mb-1">Application</label>
              <select
                value={form.application_id}
                onChange={(e) => setForm({ ...form, application_id: e.target.value })}
                className="w-full bg-slate-700 text-white rounded-lg px-4 py-2.5 text-sm focus:outline-none"
                required
              >
                <option value="">Select application...</option>
                {applications.map(app => (
                  <option key={app.id} value={app.id}>
                    {app.company_name} — {app.role_title}
                  </option>
                ))}
              </select>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm text-slate-300 mb-1">Type</label>
                <select
                  value={form.reminder_type}
                  onChange={(e) => setForm({ ...form, reminder_type: e.target.value })}
                  className="w-full bg-slate-700 text-white rounded-lg px-4 py-2.5 text-sm focus:outline-none"
                >
                  {REMINDER_TYPES.map(t => <option key={t} value={t}>{t.replace('_', ' ').replace(/\b\w/g, c => c.toUpperCase())}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm text-slate-300 mb-1">Remind at</label>
                <input
                  type="datetime-local"
                  value={form.remind_at}
                  onChange={(e) => setForm({ ...form, remind_at: e.target.value })}
                  className="w-full bg-slate-700 text-white rounded-lg px-4 py-2.5 text-sm focus:outline-none"
                  required
                />
              </div>
            </div>
            <div>
              <label className="block text-sm text-slate-300 mb-1">Note</label>
              <input
                value={form.note}
                onChange={(e) => setForm({ ...form, note: e.target.value })}
                className="w-full bg-slate-700 text-white rounded-lg px-4 py-2.5 text-sm focus:outline-none"
                placeholder="What do you want to be reminded about?"
              />
            </div>
            <button
              type="submit"
              className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2.5 rounded-lg transition text-sm font-medium"
            >
              Set Reminder
            </button>
          </form>
        </div>
        <div className="space-y-3">
          {reminders.length === 0 && (
            <p className="text-slate-400 text-center py-8">No reminders set yet.</p>
          )}
          {reminders.map(r => (
            <div key={r.id} className={`bg-slate-800 rounded-xl p-4 flex items-center justify-between ${r.is_sent ? 'opacity-50' : ''}`}>
              <div>
                <p className="text-white text-sm font-medium">{getAppName(r.application_id)}</p>
                <p className="text-slate-400 text-xs mt-0.5">
                  {r.reminder_type.replace('_', ' ')} · {format(new Date(r.remind_at + 'Z'), 'MMM d, yyyy h:mm a')}
                </p>
                {r.note && <p className="text-slate-500 text-xs mt-1">{r.note}</p>}
              </div>
              <div className="flex items-center gap-3">
                {r.is_sent && <span className="text-green-400 text-xs">Sent ✓</span>}
                <button onClick={() => handleDelete(r.id)} className="text-red-400 hover:text-red-300 text-xs">Delete</button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}