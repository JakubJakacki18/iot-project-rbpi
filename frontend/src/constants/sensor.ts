import type { SensorType } from "@/types/sensors";

export const sensorConfigs: Record<
  SensorType,
  { label: string; unit: string }
> = {
  temperature: {
    label: "Temperatura",
    unit: "°C",
  },
  humidity: {
    label: "Wilgotność",
    unit: "%",
  },
  pressure: {
    label: "Ciśnienie",
    unit: "hPa",
  },
  tilt: {
    label: "Pochylenie",
    unit: "°",
  },
  light: {
    label: "Natężenie światła",
    unit: "",
  },
};
