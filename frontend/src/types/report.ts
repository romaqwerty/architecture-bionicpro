export interface Report {
  username: string;
  email: string;
  date_of_birth: string;
  timestamp: string;
  sensor_value: number;
}

export interface ReportsResponse {
  reports: Report[];
}

export interface UserSummary {
  username: string;
  dateOfBirth: string;
}
