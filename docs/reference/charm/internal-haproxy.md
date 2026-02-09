(reference-charm-internal-haproxy)=

# Internal HAProxy Service

Starting with the Landscape Server 26.04 beta version of the charm, each unit on the Landscape Server charm installs its own internal HAProxy service. This allows the charm to manage traffic to worker processes on all units without needing to integrate with the legacy HAProxy charm.

## HAProxy Config Template

The charm uses [`jinja2`](https://jinja.palletsprojects.com/en/stable/) and the following template to dynamically generate the HAProxy config file on each unit:

```jinja
global
    maxconn {{ global_max_connections }}
    user haproxy
    group haproxy

    log /dev/log local0

    # generated 2026-01-07, Mozilla Guideline v5.7, HAProxy 2.8, OpenSSL 1.1.1w (UNSUPPORTED; end-of-life), intermediate config, no HSTS
    # https://ssl-config.mozilla.org/#server=haproxy&version=2.8&config=intermediate&openssl=1.1.1w&hsts=false&guideline=5.7
    # intermediate configuration
    ssl-default-bind-curves X25519:prime256v1:secp384r1
    ssl-default-bind-ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:DHE-RSA-CHACHA20-POLY1305
    ssl-default-bind-ciphersuites TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
    ssl-default-bind-options prefer-client-ciphers ssl-min-ver TLSv1.2 no-tls-tickets

    ssl-default-server-ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:DHE-RSA-CHACHA20-POLY1305
    ssl-default-server-ciphersuites TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
    ssl-default-server-options ssl-min-ver TLSv1.2 no-tls-tickets

    tune.ssl.default-dh-param 2048

defaults
    log global
    mode http
    option httplog
    option dontlognull
    retries 3
    timeout queue 60000
    timeout connect 5000
    timeout client 120000
    timeout server 120000

    {% for status, filename in error_files.items() %}
    errorfile {{ status }} {{ error_files_directory }}/{{ filename }}
    {% endfor %}

frontend {{ http_service.frontend.frontend_name }}
    bind [::]:{{ http_service.frontend.frontend_port }} v4v6
    {% for option in http_service.frontend.frontend_options %}
    {{ option }}
    {% endfor %}

    {% if redirect_directive %}
    {{ redirect_directive }}
    {% endif %}

    default_backend {{ http_service.default_backend }}

frontend {{ https_service.frontend.frontend_name }}
    bind [::]:{{ https_service.frontend.frontend_port }} v4v6 ssl crt {{ ssl_cert_path }}
    {% for option in https_service.frontend.frontend_options %}
    {{ option }}
    {% endfor %}

    default_backend {{ https_service.default_backend }}

{% if hostagent_messenger_service %}
frontend {{ hostagent_messenger_service.frontend.frontend_name }}
    bind [::]:{{ hostagent_messenger_service.frontend.frontend_port }} v4v6 ssl crt {{ ssl_cert_path }} alpn h2,http/1.1
    {% for option in hostagent_messenger_service.frontend.frontend_options %}
    {{ option }}
    {% endfor %}

    default_backend {{ hostagent_messenger_service.default_backend }}
{% endif %}

{% if ubuntu_installer_attach_service %}
frontend {{ ubuntu_installer_attach_service.frontend.frontend_name }}
    bind [::]:{{ ubuntu_installer_attach_service.frontend.frontend_port }} v4v6 ssl crt {{ ssl_cert_path }} alpn h2,http/1.1
    {% for option in ubuntu_installer_attach_service.frontend.frontend_options %}
    {{ option }}
    {% endfor %}

    default_backend {{ ubuntu_installer_attach_service.default_backend }}
{% endif %}

{% for backend in http_service.backends %}
backend {{ backend.backend_name }}
    mode http
    timeout server {{ server_timeout }}
    {% for server in backend.servers %}
    server {{ server.name }} {{ server.ip }}:{{ server.port }} {{ server.options }}
    {% endfor %}

{% endfor %}

{% for backend in https_service.backends %}
backend {{ backend.backend_name }}
    mode http
    timeout server {{ server_timeout }}
    {% for server in backend.servers %}
    server {{ server.name }} {{ server.ip }}:{{ server.port }} {{ server.options }}
    {% endfor %}

{% endfor %}

{% if hostagent_messenger_service %}
{% for backend in hostagent_messenger_service.backends %}
backend {{ backend.backend_name }}
    mode http
    timeout server {{ server_timeout }}
    {% for server in backend.servers %}
    server {{ server.name }} {{ server.ip }}:{{ server.port }} {{ server.options }}
    {% endfor %}

{% endfor %}
{% endif %}

{% if ubuntu_installer_attach_service %}
{% for backend in ubuntu_installer_attach_service.backends %}
backend {{ backend.backend_name }}
    mode http
    timeout server {{ server_timeout }}
    {% for server in backend.servers %}
    server {{ server.name }} {{ server.ip }}:{{ server.port }} {{ server.options }}
    {% endfor %}

{% endfor %}
{% endif %}
```

### HAProxy Configuration Template Input Parameters

The HAProxy configuration is rendered using the following input parameters:

### `all_ips`

- Purpose: A list of IP addresses of all peer units
- Type: `list[IPvAnyAddress]`
- Default: *Required*

### `leader_ip`

- Purpose: The IP address of the leader unit
- Type: `IPvAnyAddress`
- Default: *Required*

### `worker_counts`

- Purpose: The number of worker processes configured
- Type: `int`
- Default: *Required*

### `redirect_https`

- Purpose: Settings to determine how to redirect HTTP to HTTPS
- Type: `RedirectHTTPS`
- Default: *Required*

### `enable_hostagent_messenger`

- Purpose: Whether to create a frontend/backend for the Hostagent Messenger service
- Type: `bool`
- Default: *Required*

### `enable_ubuntu_installer_attach`

- Purpose: Whether to create a frontend/backend for the Ubuntu Installer Attach service
- Type: `bool`
- Default: *Required*

### `max_connections`

- Purpose: Maximum concurrent connections for HAProxy
- Type: `int`
- Default: `4096`

### `ssl_cert_path`

- Purpose: The path of the SSL certificate to use for the HAProxy service
- Type: `str`
- Default: "/etc/haproxy/haproxy.pem"

### `rendered_config_path`

- Purpose: Path where the rendered config will be written
- Type: `str`
- Default: `/etc/haproxy/haproxy.cfg`

### `service_ports`

- Purpose: A mapping of services to their base ports
- Type: `ServicePorts`
- Default:

    ```python
    {
        "appserver": 8080,
        "pingserver": 8070,
        "message-server": 8090,
        "api": 9080,
        "package-upload": 9100,
        "hostagent-messenger": 50052,
        "ubuntu-installer-attach": 53354,
    }
    ```

### `error_files_directory`

- Purpose: Directory where the Landscape error files are located
- Type: `str`
- Default: `/etc/haproxy/errors`

### `error_files`

- Purpose: A mapping of status codes (string) to the name of the error file in `error_files_directory`
- Type: `dict[str, str]`
- Default:

    ```python
    {
        "403": "unauthorized-haproxy.html",
        "500": "exception-haproxy.html",
        "502": "unplanned-offline-haproxy.html",
        "503": "unplanned-offline-haproxy.html",
        "504": "timeout-haproxy.html",
    }
    ```

### `server_timeout`

- Purpose: Timeout for backend servers in milliseconds
- Type: `int`
- Default: `300000` (5 minutes)

### `server_options`

- Purpose: Options applied to all backend servers
- Type: `str`
- Default: `check inter 5000 rise 2 fall 5 maxconn 50`

### `template_path`

- Purpose: Path to the Jinja2 template file used to render the HAProxy config
- Type: `str`
- Default: `haproxy.cfg.j2`

## Template helpers

Key constants and classes used in template rendering:

- `CLIENT_TIMEOUT`: 300000ms (5 minutes)
- `SERVER_TIMEOUT`: 300000ms (5 minutes)
- `SERVER_OPTIONS`: `check inter 5000 rise 2 fall 5 maxconn 50`
- `GRPC_SERVER_OPTIONS`: `proto h2`

### Frontend ports

- HTTP: 80
- HTTPS: 443
- Hostagent Messenger: 6554
- Ubuntu Installer Attach: 50051

### Backend services

HTTP backends:

- `landscape-http-api`
- `landscape-http-message`
- `landscape-http-ping`
- `landscape-http-hashid-databases`
- `landscape-http-package-upload`

HTTPS backends:

- `landscape-https-api`
- `landscape-https-message`
- `landscape-https-ping`
- `landscape-https-hashid-databases`
- `landscape-https-package-upload`

gRPC backends:

- `landscape-hostagent-messenger`
- `landscape-ubuntu-installer-attach`

### ACL path mappings

- `/ping` → `landscape-http-ping` / `landscape-https-ping`
- `/message-system` → `landscape-http-message` / `landscape-https-message`
- `/attachment` → `landscape-http-message` / `landscape-https-message`
- `/api` → `landscape-http-api` / `landscape-https-api`
- `/hash-id-databases` → `landscape-http-hashid-databases` / `landscape-https-hashid-databases`
- `/upload` → `landscape-http-package-upload` / `landscape-https-package-upload`
