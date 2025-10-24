FROM nvidia/cuda:12.2.0-base-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

# Install tzdata first to avoid prompts
RUN apt-get update && apt-get install -y tzdata && apt-get clean

# Install devcontainer features: common-utils, github-cli, shellcheck
RUN apt-get update && apt-get install -y \
  apt-utils \
  curl \
  wget \
  unzip \
  lsb-release \
  tree \
  vim \
  && curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
  && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
  && apt-get update \
  && apt-get install -y gh \
  && apt-get install -y shellcheck \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && rm -rf /var/cache/apt/*

# Python layer - install Python 3.14 and UV
RUN apt-get update && apt-get install -y \
  curl \
  gnupg \
  software-properties-common \
  && add-apt-repository ppa:deadsnakes/ppa \
  && apt-get update \
  && apt-get install -y python3.14 python3.14-venv python3.14-dev \
  && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.14 1 \
  && update-alternatives --install /usr/bin/python python /usr/bin/python3.14 1 \
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

# GitHub Actions Runner layer - install GitHub Actions runner
RUN apt-get update && apt-get install -y \
  jq \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && rm -rf /var/cache/apt/*

# Create vscode home directory
RUN mkdir -p /home/vscode

# Install GitHub Actions runner
RUN cd /home/vscode && mkdir actions-runner && cd actions-runner \
  && curl -O -L https://github.com/actions/runner/releases/download/v2.303.0/actions-runner-linux-x64-2.303.0.tar.gz \
  && tar xzf actions-runner-linux-x64-2.303.0.tar.gz \
  && /home/vscode/actions-runner/bin/installdependencies.sh \
  && rm actions-runner-linux-x64-2.303.0.tar.gz

# Copy GitHub Actions runner startup script
COPY scripts/start.sh /home/vscode/actions-runner/start.sh
RUN chmod +x /home/vscode/actions-runner/start.sh

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
