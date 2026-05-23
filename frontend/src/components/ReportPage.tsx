import { useMemo, useState } from "react";
import { useKeycloak } from "@react-keycloak/web";
import { fetchReports } from "../api/reports";
import { Report, UserSummary } from "../types/report";

type ReportState = {
  data: Report[] | null;
  loading: boolean;
  error: string | null;
};

const initialReportState: ReportState = {
  data: null,
  loading: false,
  error: null,
};

function getUserSummary(reports: Report[]): UserSummary | null {
  const firstReport = reports[0];

  if (!firstReport) {
    return null;
  }

  return {
    username: firstReport.username,
    dateOfBirth: firstReport.date_of_birth,
  };
}

function LoadingScreen() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-100 px-4 text-slate-700">
      Loading...
    </main>
  );
}

function LoginScreen({ onLogin }: { onLogin: () => void }) {
  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-100 px-4">
      <button
        onClick={onLogin}
        className="rounded bg-blue-600 px-4 py-2 font-medium text-white hover:bg-blue-700"
      >
        Login
      </button>
    </main>
  );
}

function ReportHeader({ onLogout }: { onLogout: () => void }) {
  return (
    <header className="mb-6 flex items-center justify-between gap-4">
      <h1 className="text-2xl font-bold text-slate-900">Usage Reports</h1>
      <button
        onClick={onLogout}
        className="rounded bg-red-600 px-4 py-2 font-medium text-white hover:bg-red-700"
      >
        Logout
      </button>
    </header>
  );
}

function UserInfo({ user }: { user: UserSummary }) {
  return (
    <section className="mt-6 rounded border border-slate-200 bg-slate-50 p-4">
      <dl className="grid gap-2 sm:grid-cols-2">
        <div>
          <dt className="text-sm font-medium text-slate-500">Username</dt>
          <dd className="text-slate-900">{user.username}</dd>
        </div>
        <div>
          <dt className="text-sm font-medium text-slate-500">Date of Birth</dt>
          <dd className="text-slate-900">{user.dateOfBirth}</dd>
        </div>
      </dl>
    </section>
  );
}

function ReportTable({ reports }: { reports: Report[] }) {
  return (
    <div className="mt-6 overflow-x-auto">
      <table className="min-w-full border border-slate-200 text-left">
        <thead className="bg-slate-100">
          <tr>
            <th className="border border-slate-200 px-4 py-2 font-semibold text-slate-700">
              Timestamp
            </th>
            <th className="border border-slate-200 px-4 py-2 font-semibold text-slate-700">
              Sensor Value
            </th>
          </tr>
        </thead>
        <tbody>
          {reports.map((report) => (
            <tr
              key={`${report.username}-${report.timestamp}`}
              className="even:bg-slate-50"
            >
              <td className="border border-slate-200 px-4 py-2 text-slate-700">
                {report.timestamp}
              </td>
              <td className="border border-slate-200 px-4 py-2 text-slate-700">
                {report.sensor_value}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function EmptyState() {
  return <div className="mt-4 text-slate-600">No reports available.</div>;
}

function ErrorMessage({ message }: { message: string }) {
  return (
    <div className="mt-4 rounded border border-red-200 bg-red-50 p-4 text-red-700">
      {message}
    </div>
  );
}

export default function ReportPage() {
  const { keycloak, initialized } = useKeycloak();
  const [reportState, setReportState] = useState<ReportState>(initialReportState);

  const userInfo = useMemo(
    () => (reportState.data ? getUserSummary(reportState.data) : null),
    [reportState.data],
  );

  async function loadReport() {
    if (!keycloak.token) {
      setReportState({ data: null, loading: false, error: "Not authenticated" });
      return;
    }

    setReportState((current) => ({ ...current, loading: true, error: null }));

    try {
      const data = await fetchReports(keycloak.token);
      setReportState({ data: data.reports, loading: false, error: null });
    } catch (error) {
      setReportState({
        data: null,
        loading: false,
        error: error instanceof Error ? error.message : "An error occurred",
      });
    }
  }

  function logout() {
    keycloak.logout({ redirectUri: window.location.origin });
  }

  if (!initialized) {
    return <LoadingScreen />;
  }

  if (!keycloak.authenticated) {
    return <LoginScreen onLogin={() => keycloak.login()} />;
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-100 p-4">
      <section className="w-full max-w-3xl rounded-lg bg-white p-8 shadow-md">
        <ReportHeader onLogout={logout} />

        <button
          onClick={loadReport}
          disabled={reportState.loading}
          className="rounded bg-blue-600 px-4 py-2 font-medium text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {reportState.loading ? "Loading Report..." : "Load Report"}
        </button>

        {reportState.error && <ErrorMessage message={reportState.error} />}
        {userInfo && <UserInfo user={userInfo} />}
        {reportState.data && reportState.data.length > 0 && (
          <ReportTable reports={reportState.data} />
        )}
        {reportState.data && reportState.data.length === 0 && <EmptyState />}
      </section>
    </main>
  );
}
