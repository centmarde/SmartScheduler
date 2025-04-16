import { ThemeProvider, useTheme } from "@/theme/theme";
import Navbar from "@/components/common/navbar";
import { useNavigate } from "react-router-dom";

function LandingContent() {
  const theme = useTheme();
  const navigate = useNavigate();

  const goToTable = () => {
    navigate("/algorithms");
  };
  
  return (
    <div className="h-screen flex flex-col overflow-hidden" style={{ backgroundColor: theme.colors.cream }}>
      <Navbar />

      <main className="container mx-auto px-4 py-6 flex-grow flex items-center overflow-hidden">
        <div className="grid items-center gap-8 md:grid-cols-2 w-full max-h-full">
          <div className="order-2 md:order-1 hidden md:block">
            <img
              src="images/schedule.png"
              alt="Teacher scheduling illustration"
              className=" object-cover max-h-[80vh] w-auto"
             
            />
          </div>
          <div className="order-1 md:order-2">
            <h1 className="mb-3 text-3xl font-extrabold tracking-tight sm:text-4xl md:text-5xl" 
                style={theme.components.text.heading}>
              Simplify Your Teaching Schedule
            </h1>
            <p className="mb-6 text-lg" style={theme.components.text.body}>
              Our intelligent schedule sorter helps teachers organize classes, plan lessons, and manage time
              effectively. Save hours each week and focus on what matters most - your students.
            </p>
            <div className="space-y-4 sm:flex sm:space-x-4 sm:space-y-0">
              <button 
                onClick={goToTable}
                style={{ ...theme.components.button.primary.base, padding: '12px 24px' }}
                onMouseOver={(e) => {
                  if (theme.components.button.primary.hover) {
                    Object.assign(e.currentTarget.style, theme.components.button.primary.hover);
                  }
                }}
                onMouseOut={(e) => {
                  Object.assign(e.currentTarget.style, theme.components.button.primary.base);
                }}
                className="w-full sm:w-auto">
                Get Started
              </button>
              <button 
                onClick={goToTable}
                style={{ ...theme.components.button.secondary.base, padding: '12px 24px' }}
                onMouseOver={(e) => {
                  if (theme.components.button.secondary.hover) {
                    Object.assign(e.currentTarget.style, theme.components.button.secondary.hover);
                  }
                }}
                onMouseOut={(e) => {
                  Object.assign(e.currentTarget.style, theme.components.button.secondary.base);
                }}
                className="w-full sm:w-auto">
                Learn More
              </button>
            </div>
            <div className="mt-6 flex items-center">
              <div className="flex -space-x-2">
                {[1, 2, 3, 4].map((i) => (
                  <img 
                    key={i} 
                    src={`persons/${i}.png`} 
                    alt={`User avatar ${i}`}
                    className="h-8 w-8 rounded-full border-2 border-white object-cover"
                  />
                ))}
              </div>
              <p className="ml-4 text-sm" style={theme.components.text.small}>
                <span style={{ fontWeight: 'bold', color: theme.colors.darkGray }}>2,000+</span> teachers already using our platform
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default function LandingPage() {
  return (
    <ThemeProvider>
      <LandingContent />
    </ThemeProvider>
  );
}
