import { cn } from "@/lib/utils";

interface MenuButtonProps {
  emoji: string;
  label: string;
  onClick?: () => void;
  className?: string;
  index?: number;
  disabled?: boolean;
  showLowBalance?: boolean;
   note?: string;
}

const MenuButton = ({ emoji, label, onClick, className, index = 0, disabled, showLowBalance, note }: MenuButtonProps) => {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={cn(
        "neu-button px-4 py-3.5 text-sm text-[#333] flex flex-col items-start gap-1 w-full text-left group",
        className
      )}
      style={{ animationDelay: `${index * 50}ms` }}
    >
      <div className="flex items-center gap-3 w-full">
        <span className="w-8 h-8 flex items-center justify-center text-2xl shrink-0 group-hover:scale-125 transition-transform duration-300 group-hover:rotate-12 drop-shadow-md">
          {emoji}
        </span>
        <span className="leading-tight font-bold">{label}</span>
      </div>
      {showLowBalance && (
        <span className="text-[10px] text-red-500 font-medium">Нужно пополнить баланс</span>
      )}
      {note && !showLowBalance && (
        <span className="text-[10px] text-[#666] font-medium">{note}</span>
      )}
    </button>
  );
};

export default MenuButton;
