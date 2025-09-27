import { useState } from "react";
import { NavBar } from "../ui/navbar";
import "../../styles/pageLayout.css";

function PageLayout({ children }) {
  const [isDark, setIsDark] = useState(false);
  return (
    <div
      className={`page-layout ${isDark ? "dark-mode" : "light-mode"}`}
      style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}
    >
      <NavBar isDark={isDark} setIsDark={setIsDark} />
      <main style={{ flex: 1 }}>{children}</main>
      <footer></footer>
    </div>
  );
}

export default PageLayout;