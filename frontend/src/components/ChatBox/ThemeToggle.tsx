import React, { useEffect, useState } from 'react';
import '../../App.css';

const ThemeToggle: React.FC = () => {
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    const root = window.document.documentElement;
    if (isDark) {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
  }, [isDark]);

  return (
    <button
      className="p-2"
      onClick={() => setIsDark(!isDark)}
    >
      {isDark ? '🌙' : '☀️'}
    </button>
  );
};

export default ThemeToggle;
