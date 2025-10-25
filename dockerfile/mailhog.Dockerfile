# MailHog Dockerfile - Email testing tool
# Captures emails sent during development for testing

FROM mailhog/mailhog:latest

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:8025 || exit 1

USER mailhog

# Expose SMTP and Web UI ports
EXPOSE 1025 8025

# Start MailHog
CMD ["MailHog"]
