# TLS Certificate Expiration Plugin

# Returns the number of days remaining for the certificate on the give domain(s)

# Example configuration:

# - type: python-monitor
#   scriptFilePath: "/usr/local/scripts/tls.py"
#   domains: ["signalfx.com", "github.com", "google.com"]

import datetime
import socket
import ssl
import logging

logger = logging.getLogger(__name__)

def ssl_expiry_datetime(hostname):
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'

    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=hostname,
    )

    # 3 second timeout
    conn.settimeout(3.0)

    conn.connect((hostname, 443))
    ssl_info = conn.getpeercert()
    # Parse the string from the certificate into a Python datetime object
    return datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)

def ssl_valid_time_remaining(hostname):
    # Get the number of seconds left in a cert's lifetime
    try:
        expires = ssl_expiry_datetime(hostname)
    except ssl.SSLError:
        return datetime.timedelta(0)
    return expires - datetime.datetime.utcnow()

def run(config, output):
    domains = config.get("domains")
    for domain in domains:
        t = ssl_valid_time_remaining(domain)
        t = t.total_seconds()
        t = int(t) / 86400
        output.send_gauge("days.remaining", t, {"domain": domain, "source": "tls_cert_expiration"})