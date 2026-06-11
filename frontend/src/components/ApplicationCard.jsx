import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { format } from 'date-fns';

export default function ApplicationCard({ application, onDelete, onEdit }) {
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } = useSortable({
    id: application.id.toString(),
  });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  };

  const PLATFORM_COLORS = {
    linkedin: 'bg-blue-900 text-blue-300',
    naukri: 'bg-orange-900 text-orange-300',
    internshala: 'bg-green-900 text-green-300',
    indeed: 'bg-blue-900 text-blue-300',
    company: 'bg-slate-700 text-slate-300',
  };

  const platformColor = PLATFORM_COLORS[application.platform?.toLowerCase()] || 'bg-slate-700 text-slate-300';

  return (
    <div
      ref={setNodeRef}
      style={style}
      className="bg-slate-700 rounded-xl p-4 cursor-grab active:cursor-grabbing shadow-md hover:shadow-lg transition-shadow"
    >
      <div {...attributes} {...listeners}>
        <div className="flex items-start justify-between mb-2">
          <div>
            <p className="font-semibold text-white text-sm">{application.company_name}</p>
            <p className="text-slate-400 text-xs mt-0.5">{application.role_title}</p>
          </div>
          {application.platform && (
            <span className={`text-xs px-2 py-0.5 rounded-full ${platformColor}`}>
              {application.platform}
            </span>
          )}
        </div>
        <p className="text-slate-500 text-xs">
          Applied {format(new Date(application.applied_on), 'MMM d, yyyy')}
        </p>
      </div>
      <div className="flex gap-2 mt-3">
        <button
          onClick={() => onEdit(application)}
          className="text-xs text-blue-400 hover:text-blue-300 transition"
        >
          Edit
        </button>
        <button
          onClick={() => onDelete(application.id)}
          className="text-xs text-red-400 hover:text-red-300 transition"
        >
          Delete
        </button>
        {application.jd_url && (
          <a
            href={application.jd_url}
            target="_blank"
            rel="noreferrer"
            className="text-xs text-green-400 hover:text-green-300 transition ml-auto"
          >
            JD ↗
          </a>
        )}
      </div>
    </div>
  );
}