#!/usr/bin/env python3

"""
PostgreSQL Backup Script to Google Cloud Storage
Usage: python backup_postgres.py
"""

import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
import gzip
import shutil
from google.cloud import storage

# Configuration
DB_HOST = os.getenv("DATABASE_HOST", "localhost")
DB_PORT = os.getenv("DATABASE_PORT", "5432")
DB_NAME = os.getenv("DATABASE_NAME", "mydb")
DB_USER = os.getenv("DATABASE_USER", "postgres")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD", "")
GCS_BUCKET = os.getenv("GCS_BUCKET", "my-backup-bucket")
BACKUP_DIR = Path(os.getenv("FILES_DIR", "/tmp/pg_backups"))
RETENTION_DAYS = int(os.getenv("RETENTION_DAYS", "30"))

print('this is pass: ', DB_PASSWORD)
class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    NC = '\033[0m'


def log_info(msg):
    """Log info message"""
    print(f"{Colors.GREEN}[INFO]{Colors.NC} {msg}")


def log_error(msg):
    """Log error message"""
    print(f"{Colors.RED}[ERROR]{Colors.NC} {msg}", file=sys.stderr)


def log_warn(msg):
    """Log warning message"""
    print(f"{Colors.YELLOW}[WARN]{Colors.NC} {msg}")


def check_prerequisites():
    """Check if required tools are available"""
    log_info("Checking prerequisites...")
    
    # Check pg_dump
    if shutil.which("pg_dump") is None:
        log_error("pg_dump not found. Please install PostgreSQL client tools.")
        result = subprocess.run(['find', '/', '-name', 'pg_dump'], 
                          capture_output=True, text=True)
        log_error(f"Search results: {result.stdout}")
        sys.exit(1)
    
    log_info("All prerequisites met.")


def create_backup_dir():
    """Create backup directory if it doesn't exist"""
    if not BACKUP_DIR.exists():
        log_info(f"Creating backup directory: {BACKUP_DIR}")
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)


def backup_database():
    """Perform database backup using pg_dump"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"backup_{DB_NAME}_{timestamp}.sql.gz"
    
    log_info(f"Starting backup of database: {DB_NAME}")
    
    try:
        # Prepare pg_dump command
        cmd = [
            "pg_dump",
            "-h", DB_HOST,
            "-p", DB_PORT,
            "-U", DB_USER,
            "-d", DB_NAME,
            "--format=plain",
            "--no-owner",
            "--no-acl"
        ]
        
        # Set environment for password
        env = os.environ.copy()
        env["PGPASSWORD"] = DB_PASSWORD
        print('env pass: ', env["PGPASSWORD"])
        
        # Run pg_dump and compress output
        with gzip.open(backup_file, 'wb') as f:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env
            )
            
            # Stream output to gzip file
            for chunk in iter(lambda: process.stdout.read(8192), b''):
                f.write(chunk)
            
            process.wait()
            
            if process.returncode != 0:
                error_msg = process.stderr.read().decode()
                log_error(f"pg_dump failed: {error_msg}")
                sys.exit(1)
        
        # Get file size
        size_mb = backup_file.stat().st_size / (1024 * 1024)
        log_info(f"Backup created successfully: {backup_file.name} ({size_mb:.2f} MB)")
        
        return backup_file
        
    except Exception as e:
        log_error(f"Backup failed: {str(e)}")
        sys.exit(1)


def upload_to_gcs(backup_file):
    """Upload backup file to Google Cloud Storage"""
    log_info(f"Uploading backup to GCS: gs://{GCS_BUCKET}")
    
    try:
        # Initialize GCS client
        client = storage.Client()
        bucket = client.bucket(GCS_BUCKET)
        blob = bucket.blob(backup_file.name)
        
        # Upload file
        blob.upload_from_filename(str(backup_file))
        
        log_info(f"Upload completed successfully: gs://{GCS_BUCKET}/{backup_file.name}")
        
    except Exception as e:
        log_error(f"Upload failed: {str(e)}")
        sys.exit(1)


def cleanup_old_backups():
    """Clean up backups older than retention period from GCS"""
    log_info(f"Cleaning up backups older than {RETENTION_DAYS} days...")
    
    try:
        client = storage.Client()
        bucket = client.bucket(GCS_BUCKET)
        
        # Calculate cutoff date
        cutoff_date = datetime.now() - timedelta(days=RETENTION_DAYS)
        
        # List and delete old backups
        blobs = bucket.list_blobs(prefix=f"backup_{DB_NAME}_")
        deleted_count = 0
        
        for blob in blobs:
            # Extract timestamp from filename
            try:
                # Format: backup_dbname_YYYYMMDD_HHMMSS.sql.gz
                timestamp_str = blob.name.split('_')[-2] + '_' + blob.name.split('_')[-1].split('.')[0]
                file_date = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                
                if file_date < cutoff_date:
                    log_info(f"Deleting old backup: {blob.name}")
                    blob.delete()
                    deleted_count += 1
            except (ValueError, IndexError):
                log_warn(f"Could not parse date from filename: {blob.name}")
                continue
        
        if deleted_count > 0:
            log_info(f"Deleted {deleted_count} old backup(s)")
        else:
            log_info("No old backups to delete")
            
    except Exception as e:
        log_error(f"Cleanup failed: {str(e)}")
        # Don't exit on cleanup failure


def cleanup_local(backup_file):
    """Remove local backup file"""
    log_info("Cleaning up local backup file...")
    try:
        backup_file.unlink()
        log_info("Local cleanup completed.")
    except Exception as e:
        log_warn(f"Could not delete local backup: {str(e)}")


def main():
    """Main execution function"""
    log_info("PostgreSQL Backup Script Started")
    log_info(f"Database: {DB_NAME} | Bucket: {GCS_BUCKET}")
    
    check_prerequisites()
    create_backup_dir()
    backup_file = backup_database()
    upload_to_gcs(backup_file)
    cleanup_old_backups()
    cleanup_local(backup_file)
    
    log_info("Backup process completed successfully!")


if __name__ == "__main__":
    main()
