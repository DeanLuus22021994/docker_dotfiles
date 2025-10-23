FROM nvidia/cuda:12.2.0-base-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

# Install tzdata first to avoid prompts
RUN apt-get update && apt-get install -y tzdata && apt-get clean

# Python layer - install Python 3.13 and UV
RUN apt-get update && apt-get install -y \
  curl \
  gnupg \
  software-properties-common \
  && add-apt-repository ppa:deadsnakes/ppa \
  && apt-get update \
  && apt-get install -y python3.13 python3.13-venv python3.13-dev \
  && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.13 1 \
  && update-alternatives --install /usr/bin/python python /usr/bin/python3.13 1 \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && rm -rf /var/cache/apt/*

# Install UV (fast Python package manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
  && mv /root/.local/bin/uv /usr/local/bin/uv \
  && chmod +x /usr/local/bin/uv

# Node.js layer - install Node.js 22
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
  && apt-get install -y nodejs \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && rm -rf /var/cache/apt/*

# MariaDB layer - install MariaDB
RUN apt-get update && apt-get install -y \
  mariadb-server \
  mariadb-client \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && rm -rf /var/cache/apt/*

# Initialize MariaDB if data directory is empty
RUN if [ ! -d /var/lib/mysql/mysql ]; then \
  mysql_install_db --user=mysql --datadir=/var/lib/mysql; \
  fi

# Copy MariaDB configuration
COPY my.cnf /etc/mysql/my.cnf
COPY init.sql /docker-entrypoint-initdb.d/

# Create a non-root user with sudo access
RUN mkdir -p /etc/sudoers.d \
  && useradd -m -s /bin/bash vscode \
  && echo 'vscode ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers.d/vscode \
  && chmod 0440 /etc/sudoers.d/vscode \
  && mkdir -p /workspaces \
  && chown vscode:vscode /workspaces \
  && mkdir -p /home/vscode/.cache/pip \
  && mkdir -p /home/vscode/.npm \
  && chown -R vscode:vscode /home/vscode

# Set the default shell to bash
SHELL ["/bin/bash", "-c"]

# Switch to the vscode user
USER vscode

# Ensure the user has access to the workspace directory
RUN mkdir -p /workspaces

# Switch back to root for running services
USER root

# Expose MariaDB port
EXPOSE 3306

# Set the default command to keep container running
CMD ["sleep", "infinity"]
