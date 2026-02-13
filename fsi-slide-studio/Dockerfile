FROM python:3.11-slim

# Install Node.js (for marp-cli) and Chromium (for PDF rendering)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    chromium \
    fonts-ipafont-gothic \
    fonts-ipafont-mincho \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g @marp-team/marp-cli@4.2.0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set Chromium path for marp-cli
ENV CHROME_PATH=/usr/bin/chromium
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

WORKDIR /app

# Install Python dependencies
COPY fsi-slide-studio/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY fsi-slide-studio/ .

# Copy skills library (read at runtime for domain knowledge)
COPY skills/ /app/skills-library/

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "app.py", \
    "--server.port=8501", \
    "--server.address=0.0.0.0", \
    "--server.headless=true", \
    "--browser.gatherUsageStats=false"]
