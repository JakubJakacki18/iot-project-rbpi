export const SENSOR_KEYS: SensorType[] = [
  "temperature",
  "humidity",
  "pressure",
  "tilt",
  "light",
] as const;

export type TimeValue = { time: string; value: number };
export type SensorDataDict = Record<string, TimeValue[]>;
export type SensorMap = {
  temperature: SensorDataDict;
  humidity: SensorDataDict;
  pressure: SensorDataDict;
  tilt: SensorDataDict;
  light: SensorDataDict;
};
export type SensorType = keyof SensorMap;
