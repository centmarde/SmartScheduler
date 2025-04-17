import { useState, useEffect, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Loader2, Server, CheckCircle, AlertCircle, X } from "lucide-react";
import axios from "axios";
import { useTheme } from "@/theme/theme";
import { Card, CardContent } from "@/components/ui/card";

type AlertStatus = {
  show: boolean;
  type: 'success' | 'error';
  message: string;
};

export default function ApiTester() {
  const [apiTestLoading, setApiTestLoading] = useState(false);
  const [alert, setAlert] = useState<AlertStatus>({
    show: false,
    type: 'success',
    message: ''
  });
  const theme = useTheme();
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  // Auto-close alert after 3 seconds
  useEffect(() => {
    if (alert.show) {
      // Clear any existing timer
      if (timerRef.current) {
        clearTimeout(timerRef.current);
      }
      
      // Set new timer to close alert after 3 seconds
      timerRef.current = setTimeout(() => {
        closeAlert();
      }, 3000);
    }
    
    // Cleanup function
    return () => {
      if (timerRef.current) {
        clearTimeout(timerRef.current);
      }
    };
  }, [alert.show, alert.message]);

  const handleApiTest = async () => {
    setApiTestLoading(true);
    setAlert({ show: false, type: 'success', message: '' });
    
    try {
      const response = await axios.get('http://127.0.0.1:8080/teachers', {
        headers: {
          'Content-Type': 'application/json',
        },
        withCredentials: true
      });
      
      // Show custom alert component instead of using window.alert
      if (response.data) {
        setAlert({
          show: true,
          type: 'success',
          message: "API connection successful! The backend is ready to use."
        });
      }
    } catch (error) {
      console.error("API test failed:", error);
      // Axios error handling
      if (axios.isAxiosError(error)) {
        setAlert({
          show: true,
          type: 'error',
          message: `API Error: ${error.response?.status || 'Unknown'} - ${error.message}`
        });
      } else {
        setAlert({
          show: true,
          type: 'error',
          message: error instanceof Error ? error.message : 'Unknown error occurred'
        });
      }
    } finally {
      setApiTestLoading(false);
    }
  };

  const closeAlert = () => {
    setAlert({ ...alert, show: false });
    if (timerRef.current) {
      clearTimeout(timerRef.current);
      timerRef.current = null;
    }
  };

  return (
    <div className="relative">
      <Button
        onClick={handleApiTest}
        className="flex items-center gap-2"
        disabled={apiTestLoading}
        style={{
          ...theme.components.button.secondary?.base || theme.components.button.primary.base,
          ...(apiTestLoading ? { opacity: 0.6, cursor: 'not-allowed' } : {})
        }}
      >
        {apiTestLoading ? (
          <>
            <Loader2 className="h-4 w-4 animate-spin" /> 
            Testing Connection
          </>
        ) : (
          <>
            <Server className="h-4 w-4" />  Test Connection...
          </>
        )}
      </Button>

      {alert.show && (
        <div className="fixed top-5 right-5 z-50 animate-in slide-in-from-top-5 duration-300">
          <Card
            className="min-w-80 shadow-lg"
            style={{
              ...theme.components.card,
              borderColor: alert.type === 'success' ?   '#4CAF50' :  '#F44336',
              borderWidth: '1px'
            }}
          >
            <CardContent className="pt-4 pb-3 px-4">
              <div className="flex items-start gap-3">
                {alert.type === 'success' ? (
                  <CheckCircle className="h-5 w-5 text-green-500 flex-shrink-0 mt-0.5" />
                ) : (
                  <AlertCircle className="h-5 w-5 text-red-500 flex-shrink-0 mt-0.5" />
                )}
                <div className="flex-1">
                  <h4 className="font-medium text-sm" style={{ color: theme.colors.darkGray }}>
                    {alert.type === 'success' ? 'Success' : 'Error'}
                  </h4>
                  <p className="text-sm mt-1" style={{ color: theme.colors.mediumBlue }}>
                    {alert.message}
                  </p>
                </div>
                <button 
                  onClick={closeAlert}
                  className="text-gray-500 hover:text-gray-700 transition-colors"
                >
                  <X className="h-4 w-4" />
                </button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
