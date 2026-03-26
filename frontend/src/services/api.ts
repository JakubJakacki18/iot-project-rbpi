import { BACKEND_URL } from "@/constants/url";
import axios from "axios";

export const AxiosApi = axios.create({
  baseURL: `${BACKEND_URL}/api`,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 5000,
});
