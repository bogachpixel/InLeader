const FloatingBackground = () => {
  return (
    <>
      <div className="app-background" />
      <div className="floating-orb orb-1" />
      <div className="floating-orb orb-2" />
      <div className="floating-orb orb-3" />
      <div className="floating-orb orb-4" />
      <div className="floating-orb orb-5" />

      {/* Sparkle particles */}
      {Array.from({ length: 8 }).map((_, i) => (
        <div
          key={i}
          className="sparkle"
          style={{
            left: `${10 + Math.random() * 80}%`,
            top: `${10 + Math.random() * 80}%`,
            animationDelay: `${i * 0.7}s`,
            animationDuration: `${3 + Math.random() * 3}s`,
          }}
        />
      ))}
    </>
  );
};

export default FloatingBackground;
