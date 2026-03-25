import type { SensorType } from "@/types/sensors";

export const sensorConfigs: Record<
  SensorType,
  { label: string; unit: string; color: string }
> = {
  temperature: {
    label: "Temperatura",
    unit: "°C",
    color: "#3b82f6",
  },
  humidity: {
    label: "Wilgotność",
    unit: "%",
    color: "#10b981",
  },
  pressure: {
    label: "Ciśnienie",
    unit: "hPa",
    color: "#3b82f6",
  },
  tilt: {
    label: "Pochylenie",
    unit: "°",
    color: "#3b82f6",
  },
  light: {
    label: "Natężenie światła",
    unit: "",
    color: "#3b82f6",
  },
};
