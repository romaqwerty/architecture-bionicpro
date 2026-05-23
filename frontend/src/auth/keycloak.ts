import Keycloak, { KeycloakConfig, KeycloakInitOptions } from "keycloak-js";

const keycloakConfig: KeycloakConfig = {
  url: process.env.REACT_APP_KEYCLOAK_URL,
  realm: process.env.REACT_APP_KEYCLOAK_REALM || "",
  clientId: process.env.REACT_APP_KEYCLOAK_CLIENT_ID || "",
};

export const keycloak = new Keycloak(keycloakConfig);

export const keycloakInitOptions: KeycloakInitOptions = {
  onLoad: "login-required",
  pkceMethod: "S256",
  checkLoginIframe: false,
};
