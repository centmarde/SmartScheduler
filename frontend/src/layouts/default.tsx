import React from "react";
import InsideNavbar from "@/components/common/inside_nav";
import Footer from "@/components/common/footer";
import { useTheme } from "@/theme/theme";

interface DefaultLayoutProps {
  children: React.ReactNode;
}

const DefaultLayout: React.FC<DefaultLayoutProps> = ({ children }) => {
  const theme = useTheme();

  return (
    <div className="flex flex-col min-h-screen" style={{ backgroundColor: theme.colors.cream }}>
      <InsideNavbar />
      <main className="flex-grow container mx-auto px-4 py-6">
        {children}
      </main>
      <Footer />
    </div>
  );
};

export default DefaultLayout;
