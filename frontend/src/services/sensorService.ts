import type { SensorHistoryAvgResponse, SensorType } from "@/types/sensors";
import { AxiosApi } from "./api";

export const SensorService = {
  async getSensorLastWeekAvgValues(
    sensorType: SensorType,
  ): Promise<SensorHistoryAvgResponse> {
    const response = await AxiosApi.get<SensorHistoryAvgResponse>(
      `/sensor/week/${sensorType}`,
    );
    return response.data;
  },
};
