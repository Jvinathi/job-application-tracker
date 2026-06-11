import { Link, useNavigate } from 'react-router-dom';
import useAuthStore from '../store/authStore';
import toast from 'react-hot-toast';

export default function Navbar() {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    toast.success('Logged out');
    navigate('/login');
  };

  return (
    <nav className="bg-slate-800 border-b border-slate-700 px-6 py-4 flex items-center justify-between">
      <Link to="/dashboard" className="text-xl font-bold text-white">
        Job Tracker
      </Link>
      <div className="flex items-center gap-6">
        <Link to="/dashboard" className="text-slate-300 hover:text-white transition text-sm">
          Board
        </Link>
        <Link to="/reminders" className="text-slate-300 hover:text-white transition text-sm">
          Reminders
        </Link>
        <span className="text-slate-400 text-sm">{user?.full_name}</span>
        <button
          onClick={handleLogout}
          className="text-sm bg-slate-700 hover:bg-slate-600 text-white px-4 py-2 rounded-lg transition"
        >
          Logout
        </button>
      </div>
    </nav>
  );
}