import { useState, useEffect } from "react";
import { X, AlertCircle, CheckCircle, Info, AlertTriangle } from "lucide-react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const alertVariants = cva(
  "flex items-center p-4 mb-4 border rounded-lg shadow-sm transition-opacity duration-300",
  {
    variants: {
      variant: {
        default: "bg-gray-100 border-gray-300 text-gray-800",
        success: "bg-green-50 border-green-200 text-green-800",
        error: "bg-red-50 border-red-200 text-red-800",
        warning: "bg-yellow-50 border-yellow-200 text-yellow-800",
        info: "bg-blue-50 border-blue-200 text-blue-800",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
);

export interface AlertProps extends VariantProps<typeof alertVariants> {
  title?: string;
  message: string;
  dismissible?: boolean;
  duration?: number;
  className?: string;
  onClose?: () => void;
  icon?: boolean;
}

export function Alert({
  title,
  message,
  variant = "default",
  dismissible = true,
  duration,
  className,
  onClose,
  icon = true,
}: AlertProps) {
  const [visible, setVisible] = useState(true);

  // Auto-dismiss after specified duration
  useEffect(() => {
    if (duration && duration > 0) {
      const timer = setTimeout(() => {
        setVisible(false);
        if (onClose) onClose();
      }, duration);

      return () => clearTimeout(timer);
    }
  }, [duration, onClose]);

  // Handle manual dismiss
  const handleDismiss = () => {
    setVisible(false);
    if (onClose) onClose();
  };

  if (!visible) return null;

  // Icon mapping for each variant
  const IconComponent = () => {
    if (!icon) return null;
    
    switch (variant) {
      case "success":
        return <CheckCircle className="w-5 h-5 mr-3 text-green-700" aria-hidden="true" />;
      case "error":
        return <AlertCircle className="w-5 h-5 mr-3 text-red-700" aria-hidden="true" />;
      case "warning":
        return <AlertTriangle className="w-5 h-5 mr-3 text-yellow-700" aria-hidden="true" />;
      case "info":
        return <Info className="w-5 h-5 mr-3 text-blue-700" aria-hidden="true" />;
      default:
        return <Info className="w-5 h-5 mr-3 text-gray-700" aria-hidden="true" />;
    }
  };

  return (
    <div
      className={cn(alertVariants({ variant }), className)}
      role="alert"
      aria-live="assertive"
    >
      <div className="flex items-center">
        <IconComponent />
        <div>
          {title && <h3 className="font-medium">{title}</h3>}
          <div className={title ? "text-sm mt-0.5" : ""}>{message}</div>
        </div>
      </div>
      
      {dismissible && (
        <button
          type="button"
          className="ml-auto -mx-1.5 -my-1.5 rounded-lg p-1.5 inline-flex items-center justify-center h-8 w-8 focus:outline-none focus:ring-2 focus:ring-offset-2"
          onClick={handleDismiss}
          aria-label="Close"
        >
          <span className="sr-only">Close</span>
          <X className="w-4 h-4" />
        </button>
      )}
    </div>
  );
}

// Global Alert Container Component
export interface AlertItem extends AlertProps {
  id: string;
}

interface AlertContainerProps {
  position?: "top-right" | "top-left" | "bottom-right" | "bottom-left" | "top-center" | "bottom-center";
  alerts: AlertItem[];
  onDismiss: (id: string) => void;
}

export function AlertContainer({ 
  position = "top-right", 
  alerts, 
  onDismiss 
}: AlertContainerProps) {
  // Position styling classes
  const positionClasses = {
    "top-right": "fixed top-4 right-4 z-50",
    "top-left": "fixed top-4 left-4 z-50",
    "bottom-right": "fixed bottom-4 right-4 z-50",
    "bottom-left": "fixed bottom-4 left-4 z-50",
    "top-center": "fixed top-4 left-1/2 transform -translate-x-1/2 z-50",
    "bottom-center": "fixed bottom-4 left-1/2 transform -translate-x-1/2 z-50",
  };

  if (!alerts.length) return null;

  return (
    <div className={positionClasses[position]}>
      <div className="flex flex-col space-y-2 max-w-sm">
        {alerts.map((alert) => (
          <Alert
            key={alert.id}
            title={alert.title}
            message={alert.message}
            variant={alert.variant}
            dismissible={alert.dismissible}
            duration={alert.duration}
            className="w-full"
            onClose={() => onDismiss(alert.id)}
            icon={alert.icon}
          />
        ))}
      </div>
    </div>
  );
}

// Hook for managing alerts
export function useAlerts() {
  const [alerts, setAlerts] = useState<AlertItem[]>([]);

  const addAlert = (alert: Omit<AlertItem, "id">) => {
    const id = Math.random().toString(36).substring(2, 9);
    setAlerts((prev) => [...prev, { ...alert, id }]);
    
    // Auto-remove after duration
    if (alert.duration) {
      setTimeout(() => {
        removeAlert(id);
      }, alert.duration);
    }
    
    return id;
  };

  const removeAlert = (id: string) => {
    setAlerts((prev) => prev.filter((alert) => alert.id !== id));
  };

  return {
    alerts,
    addAlert,
    removeAlert,
    success: (message: string, options?: Omit<AlertProps, "message" | "variant">) => 
      addAlert({ message, variant: "success", ...options }),
    error: (message: string, options?: Omit<AlertProps, "message" | "variant">) => 
      addAlert({ message, variant: "error", ...options }),
    warning: (message: string, options?: Omit<AlertProps, "message" | "variant">) => 
      addAlert({ message, variant: "warning", ...options }),
    info: (message: string, options?: Omit<AlertProps, "message" | "variant">) => 
      addAlert({ message, variant: "info", ...options }),
  };
}
