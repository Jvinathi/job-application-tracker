import { useState, useEffect } from 'react';
import axiosClient from '../api/axiosClient';
import toast from 'react-hot-toast';

const STATUSES = ['applied', 'shortlisted', 'interview', 'offer', 'rejected'];
const PLATFORMS = ['LinkedIn', 'Naukri', 'Internshala', 'Indeed', 'Company', 'Other'];

export default function AddApplicationModal({ onClose, onSave, editData }) {
  const [form, setForm] = useState({
    company_name: '',
    role_title: '',
    platform: '',
    jd_url: '',
    notes: '',
    status: 'applied',
  });

  useEffect(() => {
    if (editData) setForm(editData);
  }, [editData]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      let res;
      if (editData) {
        res = await axiosClient.put(`/applications/${editData.id}`, form);
        toast.success('Application updated!');
      } else {
        res = await axiosClient.post('/applications/', form);
        toast.success('Application added!');
      }
      onSave(res.data);
      onClose();
    } catch (err) {
      toast.error('Something went wrong');
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4">
      <div className="bg-slate-800 rounded-2xl p-6 w-full max-w-lg shadow-2xl">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-bold text-white">
            {editData ? 'Edit Application' : 'Add Application'}
          </h2>
          <button onClick={onClose} className="text-slate-400 hover:text-white text-2xl">×</button>
        </div>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm text-slate-300 mb-1">Company *</label>
              <input
                value={form.company_name}
                onChange={(e) => setForm({ ...form, company_name: e.target.value })}
                className="w-full bg-slate-700 text-white rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Google"
                required
              />
            </div>
            <div>
              <label className="block text-sm text-slate-300 mb-1">Role *</label>
              <input
                value={form.role_title}
                onChange={(e) => setForm({ ...form, role_title: e.target.value })}
                className="w-full bg-slate-700 text-white rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Frontend Developer"
                required
              />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm text-slate-300 mb-1">Platform</label>
              <select
                value={form.platform}
                onChange={(e) => setForm({ ...form, platform: e.target.value })}
                className="w-full bg-slate-700 text-white rounded-lg px-4 py-2.5 text-sm focus:outline-none"
              >
                <option value="">Select platform</option>
                {PLATFORMS.map(p => <option key={p} value={p.toLowerCase()}>{p}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-sm text-slate-300 mb-1">Status</label>
              <select
                value={form.status}
                onChange={(e) => setForm({ ...form, status: e.target.value })}
                className="w-full bg-slate-700 text-white rounded-lg px-4 py-2.5 text-sm focus:outline-none"
              >
                {STATUSES.map(s => <option key={s} value={s}>{s.charAt(0).toUpperCase() + s.slice(1)}</option>)}
              </select>
            </div>
          </div>
          <div>
            <label className="block text-sm text-slate-300 mb-1">JD URL</label>
            <input
              value={form.jd_url}
              onChange={(e) => setForm({ ...form, jd_url: e.target.value })}
              className="w-full bg-slate-700 text-white rounded-lg px-4 py-2.5 text-sm focus:outline-none"
              placeholder="https://..."
            />
          </div>
          <div>
            <label className="block text-sm text-slate-300 mb-1">Notes</label>
            <textarea
              value={form.notes}
              onChange={(e) => setForm({ ...form, notes: e.target.value })}
              className="w-full bg-slate-700 text-white rounded-lg px-4 py-2.5 text-sm focus:outline-none resize-none"
              rows={3}
              placeholder="Any notes about this application..."
            />
          </div>
          <div className="flex gap-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 bg-slate-700 hover:bg-slate-600 text-white py-2.5 rounded-lg transition text-sm"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2.5 rounded-lg transition text-sm"
            >
              {editData ? 'Save Changes' : 'Add Application'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}