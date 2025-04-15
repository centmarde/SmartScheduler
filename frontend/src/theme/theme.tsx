import React, { createContext, useContext, ReactNode } from 'react';

// Color palette
const colors = {
  darkGray: '#4C585B',
  mediumBlue: '#7E99A3',
  lightBlue: '#A5BFCC',
  cream: '#F4EDD3',
};

// Custom style interfaces with hover states
interface StyleWithHover {
  base: React.CSSProperties;
  hover?: React.CSSProperties;
}

interface TextStyles {
  heading: React.CSSProperties;
  body: React.CSSProperties;
  small: React.CSSProperties;
}

// Theme interface
interface ThemeType {
  colors: typeof colors;
  components: {
    button: {
      primary: StyleWithHover;
      secondary: StyleWithHover;
      text: StyleWithHover;
    };
    card: React.CSSProperties;
    input: StyleWithHover;
    text: TextStyles;
  };
}

// Define the theme
const theme: ThemeType = {
  colors,
  components: {
    button: {
      primary: {
        base: {
          backgroundColor: colors.darkGray,
          color: colors.cream,
          borderRadius: '6px',
          padding: '10px 20px',
          border: 'none',
          fontWeight: 'bold',
          cursor: 'pointer',
          transition: 'background-color 0.3s ease',
        },
        hover: {
          backgroundColor: colors.mediumBlue,
        },
      },
      secondary: {
        base: {
          backgroundColor: colors.mediumBlue,
          color: colors.cream,
          borderRadius: '6px',
          padding: '10px 20px',
          border: 'none',
          fontWeight: 'bold',
          cursor: 'pointer',
          transition: 'background-color 0.3s ease',
        },
        hover: {
          backgroundColor: colors.lightBlue,
        },
      },
      text: {
        base: {
          backgroundColor: 'transparent',
          color: colors.darkGray,
          padding: '10px 20px',
          border: 'none',
          cursor: 'pointer',
          transition: 'color 0.3s ease',
        },
        hover: {
          color: colors.mediumBlue,
        },
      },
    },
    card: {
      backgroundColor: colors.cream,
      borderRadius: '8px',
      padding: '20px',
      boxShadow: `0 4px 8px rgba(76, 88, 91, 0.1)`,
      border: `1px solid ${colors.lightBlue}`,
    },
    input: {
      base: {
        backgroundColor: colors.cream,
        border: `1px solid ${colors.lightBlue}`,
        borderRadius: '4px',
        padding: '10px 12px',
        color: colors.darkGray,
        transition: 'border-color 0.3s ease',
      },
      hover: {
        outline: 'none',
        borderColor: colors.mediumBlue,
      },
    },
    text: {
      heading: {
        color: colors.darkGray,
        fontWeight: 'bold',
        marginBottom: '16px',
      },
      body: {
        color: colors.darkGray,
        fontSize: '16px',
        lineHeight: 1.5,
      },
      small: {
        color: colors.mediumBlue,
        fontSize: '14px',
      },
    },
  },
};

// Create context
const ThemeContext = createContext<ThemeType>(theme);

// Custom hook for using the theme
export const useTheme = () => useContext(ThemeContext);

// Theme provider component
interface ThemeProviderProps {
  children: ReactNode;
}

export const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  return (
    <ThemeContext.Provider value={theme}>
      {children}
    </ThemeContext.Provider>
  );
};

// Export the theme
export default theme;
