import { ReactKeycloakProvider } from "@react-keycloak/web";
import ReportPage from "./components/ReportPage";
import { keycloak, keycloakInitOptions } from "./auth/keycloak";

function App() {
  return (
    <ReactKeycloakProvider
      authClient={keycloak}
      initOptions={keycloakInitOptions}
    >
      <ReportPage />
    </ReactKeycloakProvider>
  );
}

export default App;
