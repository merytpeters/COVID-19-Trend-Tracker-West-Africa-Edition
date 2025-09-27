import { useEffect } from "react";

function ToggleBar({ isDark, setIsDark }) {
  useEffect(() => {
    if (isDark) {
      document.body.classList.add("dark-mode");
      document.body.classList.remove("light-mode");
    } else {
      document.body.classList.add("light-mode");
      document.body.classList.remove("dark-mode");
    }
  }, [isDark]);

  return (
    <button
      onClick={() => setIsDark((prev) => !prev)}
      style={{
        padding: "8px 16px",
        borderRadius: 8,
        border: "none",
        color: isDark ? "#222" : "#eee",
        background: isDark ? "#fff" : "#222",
        cursor: "pointer",
        margin: 8,
      }}
      aria-label="Toggle light/dark mode"
    >
      {isDark ? "🌙 Dark Mode" : "☀️ Light Mode"}
    </button>
  );
}

export default ToggleBar;