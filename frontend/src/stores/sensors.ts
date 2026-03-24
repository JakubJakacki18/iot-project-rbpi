import { defineStore } from "pinia";
export const SENSOR_KEYS: SensorType[] = [
  "temperature",
  "humidity",
  "pressure",
  "tilt",
  "light",
] as const;

export type TimeValue = [time: string, value: number];
export type SensorDataDict = Record<string, TimeValue[]>;
type SensorMap = {
  temperature: SensorDataDict;
  humidity: SensorDataDict;
  pressure: SensorDataDict;
  tilt: SensorDataDict;
  light: SensorDataDict;
};
export type SensorType = keyof SensorMap;
export const useSensorStore = defineStore("sensor", {
  state: () => ({
    data: {} as SensorMap,
    MAX: 20,
  }),
  actions: {
    setSensorValue(id: string, type: SensorType, value: TimeValue) {
      if (!this.data[type]) {
        this.data[type] = {};
      }
      if (!this.data[type][id]) {
        this.data[type][id] = [];
      }
      this.data[type][id].push(value);

      if (this.data[type][id].length > this.MAX) {
        this.data[type][id].shift();
      }
    },
  },
  getters: {
    getSensorValues: (state) => (id: string, type: SensorType) =>
      state.data[type][id] ?? [],
    getLastSensorValue: (state) => (id: string, type: SensorType) => {
      const sensorValue = state.data[type]?.[id];
      return sensorValue?.at(-1) ?? null;
    },
    getAllLastSensorValue: (state) => (id: string) => {
      const data = {} as Record<SensorType, TimeValue | null>;
      for (const key of SENSOR_KEYS) {
        const sensorValue = state.data[key]?.[id];
        data[key] = sensorValue?.at(-1) ?? null;
      }
      return data;
    },
  },
});
