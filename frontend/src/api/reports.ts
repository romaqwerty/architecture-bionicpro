import { ReportsResponse } from "../types/report";

const API_URL = process.env.REACT_APP_API_URL;

export async function fetchReports(token: string): Promise<ReportsResponse> {
  const response = await fetch(`${API_URL}/reports`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(`Error ${response.status}: ${message}`);
  }

  return response.json();
}
