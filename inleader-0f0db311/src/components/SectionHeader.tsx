interface SectionHeaderProps {
  emoji: string;
  title: string;
  description?: string;
}

const SectionHeader = ({ emoji, title, description }: SectionHeaderProps) => {
  return (
    <div className="glass-header rounded-2xl px-5 py-4 mb-4 text-[#333] animate-fade-in">
      <h2 className="text-lg font-display font-bold flex items-center gap-2">
        <span className="text-2xl w-8 shrink-0 text-center">{emoji}</span> {title}
      </h2>
      {description && (
        <p className="text-sm mt-2 opacity-85 leading-relaxed">{description}</p>
      )}
    </div>
  );
};

export default SectionHeader;
