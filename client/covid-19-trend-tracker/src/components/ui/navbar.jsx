import ToggleBar from "./togglebar"
import "../../styles/navBar.css";

export function NavBar ({ isDark, setIsDark }) {
    return (
        <nav>
            <p className="logo">COVID-19 TREND TRACKER</p>
            <section aria-labelledby="Main Navigation">
                <ul>
                    <li> <a href="/">Home</a></li>
                    <li>Time Series</li>
                    <li>Compare</li>
                    <li>Filter</li>
                    <li>Map View</li>
                </ul>
            </section>
            <section aria-label="interactive-control">
                {/* Temmporary section */}
               <div className="others">
                <p>Date Range Selector</p>
                <p>Country</p>
                <div className="togglebar"><ToggleBar isDark={isDark} setIsDark={setIsDark} /></div>
            </div>
            </section>
            <section aria-label="utility-icons">

            </section>
        </nav>
    )
}