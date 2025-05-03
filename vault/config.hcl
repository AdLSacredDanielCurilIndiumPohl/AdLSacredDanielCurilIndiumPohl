ui = true

storage "file" {
  path = "/vault/data"
}

listener "tcp" {
  address = "0.0.0.0:8200"
  tls_disable = true
}

auth_enable "userpass" {
  path = "/sys/auth/userpass"
  type = "userpass"
}

api_addr = "http://0.0.0.0:8200"

# Cross-Layer-Policies
path "auth/token/create" {
  capabilities = ["create", "read", "update"]
}

path "secret/data/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

# Tool-spezifische Policies
path "secret/data/tools/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

# API-Zugriffstoken
path "auth/token/lookup" {
  capabilities = ["create", "read", "update"]
}

path "auth/token/renew" {
  capabilities = ["create", "read", "update"]
}

path "auth/token/revoke" {
  capabilities = ["create", "read", "update"]
}