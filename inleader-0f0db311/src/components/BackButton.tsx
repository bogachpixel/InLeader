import { ArrowLeft, Home } from "lucide-react";

interface BackButtonProps {
  onClick: () => void;
  label?: string;
}

const BackButton = ({ onClick, label = "В меню" }: BackButtonProps) => {
  return (
    <button
      onClick={onClick}
      className="neu-button px-4 py-3.5 text-sm text-[#333] flex items-center gap-2 w-full justify-center group mt-1"
    >
      <Home className="w-4 h-4 shrink-0 text-[var(--gold-primary)] group-hover:-translate-x-1 transition-transform duration-300" />
      <span className="font-semibold">{label}</span>
    </button>
  );
};

export default BackButton;
