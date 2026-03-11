import { Wallet, X } from "lucide-react";

interface WalletModalProps {
  isOpen: boolean;
  onClose: () => void;
  walletTitle: string;
  inCoins: number | null;
  onPayment: () => void;
}

const WalletModal = ({ isOpen, onClose, walletTitle, inCoins, onPayment }: WalletModalProps) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50" onClick={onClose}>
      <div
        className="glass-card glow-border p-6 w-full max-w-sm animate-fade-in"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-bold text-[#333] flex items-center gap-2">
            <Wallet className="w-5 h-5 text-[var(--gold-primary)]" />
            {walletTitle}
          </h3>
          <button
            onClick={onClose}
            className="p-2 text-[#666] hover:text-[#333] transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
        <div className="flex flex-col gap-3">
          <div className="flex items-center gap-2 text-[var(--gold-primary)] font-bold">
            <span>{inCoins !== null ? `${inCoins} InCoins` : "..."}</span>
          </div>
          <button
            type="button"
            onClick={onPayment}
            className="glass-card glow-border px-4 py-3 text-sm font-semibold text-[var(--gold-primary)] rounded-xl transition-opacity hover:opacity-90 w-full"
          >
            Пополнить 10 InCoins (10 руб)
          </button>
        </div>
      </div>
    </div>
  );
};

export default WalletModal;
