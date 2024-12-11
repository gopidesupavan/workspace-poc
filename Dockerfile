# Base image
FROM python:3.9-slim AS base

# Set working directory
WORKDIR /app

# Copy and install dependencies first to leverage caching
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy application files
COPY . .
