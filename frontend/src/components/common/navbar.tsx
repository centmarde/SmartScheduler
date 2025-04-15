import { useTheme } from "@/theme/theme";
import { useState } from "react";

interface NavbarProps {
  // Add any props you might need in the future
}

export const Navbar: React.FC<NavbarProps> = () => {
  const theme = useTheme();
  const [activeLink, setActiveLink] = useState<string | null>(null);
  
  return (
    <header className="container mx-auto px-4 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M4 5C4 4.44772 4.44772 4 5 4H19C19.5523 4 20 4.44772 20 5V7C20 7.55228 19.5523 8 19 8H5C4.44772 8 4 7.55228 4 7V5Z" fill={theme.colors.darkGray} />
            <path d="M4 11C4 10.4477 4.44772 10 5 10H19C19.5523 10 20 10.4477 20 11V13C20 13.5523 19.5523 14 19 14H5C4.44772 14 4 13.5523 4 13V11Z" fill={theme.colors.mediumBlue} />
            <path d="M5 16C4.44772 16 4 16.4477 4 17V19C4 19.5523 4.44772 20 5 20H19C19.5523 20 20 19.5523 20 19V17C20 16.4477 19.5523 16 19 16H5Z" fill={theme.colors.lightBlue} />
          </svg>
          <span className="text-xl font-bold" style={{ color: theme.colors.darkGray }}>
            TeacherSchedule
          </span>
        </div>
        <nav className="hidden space-x-8 md:flex">
          {['features', 'testimonials', 'pricing', 'about us'].map((item) => (
            <a 
              key={item}
              href={`#${item}`} 
              className="text-sm font-medium relative py-2 group"
              onMouseEnter={() => setActiveLink(item)}
              onMouseLeave={() => setActiveLink(null)}
              style={{ color: theme.colors.darkGray }}
            >
              <span className="capitalize">{item}</span>
              <span 
                className="absolute bottom-0 left-0 w-full h-0.5 transform scale-x-0 transition-transform duration-300 ease-in-out group-hover:scale-x-100"
                style={{ 
                  backgroundColor: theme.colors.mediumBlue,
                  transformOrigin: 'left',
                  transform: activeLink === item ? 'scaleX(1)' : 'scaleX(0)'
                }}
              />
            </a>
          ))}
        </nav>
        <div className="hidden md:flex items-center space-x-4">
          <button 
            className="relative overflow-hidden transition-all duration-300 ease-out"
            style={{ ...theme.components.button.secondary.base, marginRight: '8px', position: 'relative' }}
            onMouseOver={(e) => {
              if (theme.components.button.secondary.hover) {
                Object.assign(e.currentTarget.style, theme.components.button.secondary.hover);
              }
            }}
            onMouseOut={(e) => {
              Object.assign(e.currentTarget.style, theme.components.button.secondary.base);
            }}
          >
            Learn More
          </button>
          <button 
            className="relative overflow-hidden transform transition-all duration-300 hover:scale-105"
            style={theme.components.button.primary.base}
            onMouseOver={(e) => {
              if (theme.components.button.primary.hover) {
                Object.assign(e.currentTarget.style, theme.components.button.primary.hover);
              }
            }}
            onMouseOut={(e) => {
              Object.assign(e.currentTarget.style, theme.components.button.primary.base);
            }}
          >
            Get Started
          </button>
        </div>
      </div>
    </header>
  );
};

export default Navbar;
