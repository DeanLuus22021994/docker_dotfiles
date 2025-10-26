#!/usr/bin/env bash
# Cleanup unused Docker volumes (Linux/macOS)
# Version: 1.0
# Last Modified: 2025-10-26

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Configuration
FORCE=false
DRY_RUN=false
EXCLUDE_PATTERN=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --force)
            FORCE=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --exclude)
            EXCLUDE_PATTERN="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --force         Skip confirmation"
            echo "  --dry-run       Preview deletions only"
            echo "  --exclude PATTERN  Exclude volumes matching pattern"
            echo "  --help          Show this help"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

echo -e "${CYAN}"
echo "========================================"
echo "  Docker Volume Cleanup Utility"
echo "========================================"
echo -e "${NC}"

# Get all volumes
mapfile -t ALL_VOLUMES < <(docker volume ls -q)
echo -e "${CYAN}Total volumes: ${#ALL_VOLUMES[@]}${NC}"

# Get volumes in use
mapfile -t VOLUMES_IN_USE < <(docker ps -a --format '{{.Mounts}}' | tr ',' '\n' | sort -u)
echo -e "${CYAN}Volumes in use: ${#VOLUMES_IN_USE[@]}${NC}"

# Find unused volumes
UNUSED_VOLUMES=()
TOTAL_SIZE=0

for volume in "${ALL_VOLUMES[@]}"; do
    # Skip if in use
    if printf '%s\n' "${VOLUMES_IN_USE[@]}" | grep -q "^$volume$"; then
        continue
    fi
    
    # Skip if matches exclude pattern
    if [[ -n "$EXCLUDE_PATTERN" ]] && [[ "$volume" =~ $EXCLUDE_PATTERN ]]; then
        continue
    fi
    
    # Get volume info
    VOLUME_INFO=$(docker volume inspect "$volume" 2>/dev/null || echo "[]")
    
    # Skip if has production/backup labels
    if echo "$VOLUME_INFO" | jq -e '.[0].Labels.production or .[0].Labels.backup' &>/dev/null; then
        continue
    fi
    
    UNUSED_VOLUMES+=("$volume")
    
    # Calculate size (if possible)
    MOUNTPOINT=$(echo "$VOLUME_INFO" | jq -r '.[0].Mountpoint' 2>/dev/null || echo "")
    if [[ -n "$MOUNTPOINT" ]] && [[ -d "$MOUNTPOINT" ]]; then
        SIZE=$(du -sb "$MOUNTPOINT" 2>/dev/null | cut -f1 || echo "0")
        TOTAL_SIZE=$((TOTAL_SIZE + SIZE))
    fi
done

echo -e "${YELLOW}Unused volumes: ${#UNUSED_VOLUMES[@]}${NC}"
echo -e "${YELLOW}Space to reclaim: $(numfmt --to=iec-i --suffix=B $TOTAL_SIZE)${NC}\n"

if [[ ${#UNUSED_VOLUMES[@]} -eq 0 ]]; then
    echo -e "${GREEN}No unused volumes to delete!${NC}"
    exit 0
fi

# Display volumes to delete
echo -e "${YELLOW}Volumes scheduled for deletion:${NC}"
printf '%s\n' "${UNUSED_VOLUMES[@]}"
echo ""

# Dry run - exit here
if [[ "$DRY_RUN" == "true" ]]; then
    echo -e "${CYAN}Dry run mode: No volumes were deleted${NC}"
    exit 0
fi

# Confirmation
if [[ "$FORCE" != "true" ]]; then
    echo -e "${YELLOW}This will permanently delete ${#UNUSED_VOLUMES[@]} volumes.${NC}"
    read -rp "Continue? (y/N): " confirmation
    if [[ "$confirmation" != "y" ]] && [[ "$confirmation" != "Y" ]]; then
        echo -e "${CYAN}Operation cancelled${NC}"
        exit 0
    fi
fi

# Delete volumes
echo -e "\n${CYAN}Deleting volumes...${NC}\n"

DELETED_COUNT=0
FAILED_COUNT=0

for volume in "${UNUSED_VOLUMES[@]}"; do
    echo -n "Deleting: $volume..."
    if docker volume rm "$volume" &>/dev/null; then
        echo -e " ${GREEN}✓${NC}"
        ((DELETED_COUNT++))
    else
        echo -e " ${RED}✗${NC}"
        ((FAILED_COUNT++))
    fi
done

echo -e "\n${CYAN}========================================"
echo "  Cleanup Complete"
echo "========================================${NC}\n"

echo -e "${GREEN}Successfully deleted: $DELETED_COUNT volumes${NC}"
[[ $FAILED_COUNT -gt 0 ]] && echo -e "${YELLOW}Failed to delete: $FAILED_COUNT volumes${NC}"
echo -e "${GREEN}Space reclaimed: $(numfmt --to=iec-i --suffix=B $TOTAL_SIZE)${NC}\n"
