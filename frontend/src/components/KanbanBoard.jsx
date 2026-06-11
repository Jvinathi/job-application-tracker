import { useState, useEffect } from 'react';
import { DndContext, DragOverlay, closestCenter, PointerSensor, useSensor, useSensors } from '@dnd-kit/core';
import axiosClient from '../api/axiosClient';
import KanbanColumn from './KanbanColumn';
import ApplicationCard from './ApplicationCard';
import AddApplicationModal from './AddApplicationModal';
import toast from 'react-hot-toast';

const STATUSES = ['applied', 'shortlisted', 'interview', 'offer', 'rejected'];

export default function KanbanBoard({ onStatsChange }) {
  const [applications, setApplications] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [editData, setEditData] = useState(null);
  const [activeApp, setActiveApp] = useState(null);

  const sensors = useSensors(useSensor(PointerSensor, { activationConstraint: { distance: 5 } }));

  const fetchApplications = async () => {
    try {
      const res = await axiosClient.get('/applications/');
      setApplications(res.data);
      onStatsChange(); // refresh stats
    } catch (err) {
      toast.error('Failed to load applications');
    }
  };

  useEffect(() => { fetchApplications(); }, []);

  const getByStatus = (status) => applications.filter(a => a.status === status);

  const handleDragStart = (event) => {
    const app = applications.find(a => a.id.toString() === event.active.id);
    setActiveApp(app);
  };

  const handleDragEnd = async (event) => {
    const { active, over } = event;
    setActiveApp(null);
    if (!over) return;

    const appId = parseInt(active.id);
    const newStatus = over.id;

    if (!STATUSES.includes(newStatus)) return;

    const app = applications.find(a => a.id === appId);
    if (!app || app.status === newStatus) return;

    // Optimistic update
    setApplications(prev => prev.map(a => a.id === appId ? { ...a, status: newStatus } : a));

    try {
      await axiosClient.patch(`/applications/${appId}/status`, { status: newStatus });
      onStatsChange();
    } catch (err) {
      toast.error('Failed to update status');
      fetchApplications(); // revert
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this application?')) return;
    try {
      await axiosClient.delete(`/applications/${id}`);
      setApplications(prev => prev.filter(a => a.id !== id));
      toast.success('Deleted');
      onStatsChange();
    } catch {
      toast.error('Delete failed');
    }
  };

  const handleEdit = (app) => {
    setEditData(app);
    setShowModal(true);
  };

  const handleSave = (savedApp) => {
    setApplications(prev => {
      const exists = prev.find(a => a.id === savedApp.id);
      if (exists) return prev.map(a => a.id === savedApp.id ? savedApp : a);
      return [...prev, savedApp];
    });
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-white">My Applications</h2>
        <button
          onClick={() => { setEditData(null); setShowModal(true); }}
          className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2.5 rounded-xl font-medium transition"
        >
          + Add Application
        </button>
      </div>
      <DndContext sensors={sensors} collisionDetection={closestCenter} onDragStart={handleDragStart} onDragEnd={handleDragEnd}>
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
          {STATUSES.map(status => (
            <KanbanColumn
              key={status}
              status={status}
              applications={getByStatus(status)}
              onDelete={handleDelete}
              onEdit={handleEdit}
            />
          ))}
        </div>
        <DragOverlay>
          {activeApp ? <ApplicationCard application={activeApp} onDelete={() => {}} onEdit={() => {}} /> : null}
        </DragOverlay>
      </DndContext>
      {showModal && (
        <AddApplicationModal
          onClose={() => { setShowModal(false); setEditData(null); }}
          onSave={handleSave}
          editData={editData}
        />
      )}
    </div>
  );
}