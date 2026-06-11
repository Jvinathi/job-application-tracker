import { useDroppable } from '@dnd-kit/core';
import { SortableContext, verticalListSortingStrategy } from '@dnd-kit/sortable';
import ApplicationCard from './ApplicationCard';

const COLUMN_COLORS = {
  applied: 'border-blue-500',
  shortlisted: 'border-yellow-500',
  interview: 'border-purple-500',
  offer: 'border-green-500',
  rejected: 'border-red-500',
};

const COLUMN_LABELS = {
  applied: '📤 Applied',
  shortlisted: '⭐ Shortlisted',
  interview: '🗣️ Interview',
  offer: '🎉 Offer',
  rejected: '❌ Rejected',
};

export default function KanbanColumn({ status, applications, onDelete, onEdit }) {
  const { setNodeRef } = useDroppable({ id: status });

  return (
    <div
      ref={setNodeRef}
      className={`bg-slate-800 rounded-xl p-4 flex flex-col min-h-[400px] border-t-2 ${COLUMN_COLORS[status]}`}
    >
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-white text-sm">{COLUMN_LABELS[status]}</h3>
        <span className="bg-slate-700 text-slate-300 text-xs px-2 py-1 rounded-full">
          {applications.length}
        </span>
      </div>
      <SortableContext items={applications.map(a => a.id.toString())} strategy={verticalListSortingStrategy}>
        <div className="flex flex-col gap-3 flex-1">
          {applications.map((app) => (
            <ApplicationCard
              key={app.id}
              application={app}
              onDelete={onDelete}
              onEdit={onEdit}
            />
          ))}
        </div>
      </SortableContext>
    </div>
  );
}