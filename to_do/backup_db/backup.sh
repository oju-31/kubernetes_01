#!/usr/bin/env bash
set -euo pipefail

# ----------------------------
# PostgreSQL Backup Script
# ----------------------------

# Config (from environment variables)
DB_HOST="${DATABASE_HOST:-localhost}"
DB_PORT="${DATABASE_PORT:-5432}"
DB_NAME="${DATABASE_NAME:-mydb}"
DB_USER="${DATABASE_USER:-postgres}"
DB_PASSWORD="${DATABASE_PASSWORD:-}"
BACKUP_DIR="${FILES:-/tmp/pg_backups}"
GCS_BUCKET="${GCS_BUCKET:-}"        # Optional: e.g. "gs://my-backup-bucket"
RETENTION_DAYS="${RETENTION_DAYS:-30}"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Timestamp for backup filename
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/backup_${DB_NAME}_${TIMESTAMP}.sql.gz"

echo "[INFO] Starting backup of database '$DB_NAME'..."
export PGPASSWORD="$DB_PASSWORD"

# Streamed backup + compression
pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" \
    --format=plain --no-owner --no-acl \
    | gzip > "$BACKUP_FILE"

# Show backup info
SIZE_MB=$(du -m "$BACKUP_FILE" | cut -f1)
echo "[INFO] Backup completed: $BACKUP_FILE (${SIZE_MB} MB)"

# ----------------------------
# Upload to Google Cloud Storage
# ----------------------------
if [[ -n "$GCS_BUCKET" ]]; then
    echo "[INFO] Uploading to GCS bucket: $GCS_BUCKET"
    
    if ! command -v gsutil &>/dev/null; then
        echo "[ERROR] gsutil not found. Install Google Cloud SDK in the image."
        exit 1
    fi

    gsutil cp "$BACKUP_FILE" "$GCS_BUCKET"/

    echo "[INFO] Upload completed: $GCS_BUCKET/$(basename "$BACKUP_FILE")"
else
    echo "[WARN] GCS_BUCKET not set. Skipping upload."
fi

# ----------------------------
# Cleanup (optional)
# ----------------------------
find "$BACKUP_DIR" -type f -name "backup_${DB_NAME}_*.sql.gz" -mtime +"$RETENTION_DAYS" -exec rm {} \; || true
echo "[INFO] Local cleanup done. Old backups older than $RETENTION_DAYS days removed."
