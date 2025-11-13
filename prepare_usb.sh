#!/bin/bash
# Prepare USB Drive for CDJ-2000
# This script helps format and prepare your USB for Rekordbox export

set -e

echo "=========================================="
echo "CDJ-2000 USB PREPARATION TOOL"
echo "=========================================="
echo ""

# Check if USB is connected
echo "Step 1: Detecting USB drives..."
echo ""

if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "Connected drives:"
    diskutil list | grep -E "^/dev/disk[0-9]+" | while read disk rest; do
        info=$(diskutil info "$disk" 2>/dev/null | grep "Device / Media Name" || echo "")
        if [[ -n "$info" ]]; then
            size=$(diskutil info "$disk" 2>/dev/null | grep "Disk Size" | awk '{print $3, $4}' || echo "")
            echo "  $disk - $size"
        fi
    done
    echo ""
    echo "Your main system disk is usually /dev/disk0 - DO NOT format this!"
    echo ""
    read -p "Enter the disk to format (e.g., disk2): " DISK_NUM
    DISK="/dev/${DISK_NUM}"

    # Safety check
    if [[ "$DISK_NUM" == "disk0" ]] || [[ "$DISK_NUM" == "disk1" ]]; then
        echo "❌ Error: Cannot format system disk! Please select your USB drive."
        exit 1
    fi

    echo ""
    echo "⚠️  WARNING: This will ERASE ALL DATA on $DISK"
    diskutil info "$DISK" 2>/dev/null | grep -E "(Device / Media Name|Disk Size)" || true
    echo ""
    read -p "Are you sure you want to format $DISK? (type 'YES' to confirm): " CONFIRM

    if [[ "$CONFIRM" != "YES" ]]; then
        echo "Cancelled."
        exit 0
    fi

    echo ""
    echo "Step 2: Formatting USB drive as exFAT..."
    echo "This may take a few minutes..."

    # Unmount first
    diskutil unmountDisk "$DISK" 2>/dev/null || true

    # Format as exFAT (supports files >4GB, works with CDJ-2000)
    sudo diskutil eraseDisk exFAT "REKORDBOX" "$DISK"

    echo ""
    echo "✓ USB formatted successfully!"
    echo ""
    echo "USB is now ready at: /Volumes/REKORDBOX"
    USB_PATH="/Volumes/REKORDBOX"

elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    echo "Connected drives:"
    lsblk -o NAME,SIZE,TYPE,MOUNTPOINT | grep -v "loop"
    echo ""
    read -p "Enter the device to format (e.g., sdb): " DEVICE
    DISK="/dev/${DEVICE}"

    echo ""
    echo "⚠️  WARNING: This will ERASE ALL DATA on $DISK"
    echo ""
    read -p "Are you sure? (type 'YES' to confirm): " CONFIRM

    if [[ "$CONFIRM" != "YES" ]]; then
        echo "Cancelled."
        exit 0
    fi

    echo ""
    echo "Step 2: Formatting USB drive as exFAT..."

    # Unmount if mounted
    sudo umount "${DISK}"* 2>/dev/null || true

    # Create new partition table and format
    sudo parted "$DISK" --script mklabel msdos
    sudo parted "$DISK" --script mkpart primary exfat 0% 100%
    sudo mkfs.exfat -n REKORDBOX "${DISK}1"

    # Mount
    sudo mkdir -p /mnt/rekordbox
    sudo mount "${DISK}1" /mnt/rekordbox

    echo ""
    echo "✓ USB formatted successfully!"
    echo ""
    echo "USB is now ready at: /mnt/rekordbox"
    USB_PATH="/mnt/rekordbox"
else
    echo "❌ Unsupported operating system"
    exit 1
fi

echo ""
echo "=========================================="
echo "USB PREPARATION COMPLETE!"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Create a shopping list from your recognized tracks:"
echo "   cd ~/dj-set-song-recognizer"
echo "   python3 rekordbox_helper.py --shopping-list ~/Downloads/dj_set_shazam_results.json -o shopping.txt"
echo ""
echo "2. Download tracks from Beatport/Traxsource:"
echo "   - Open shopping.txt"
echo "   - Search and download each track (WAV or AIFF format recommended)"
echo "   - Save to ~/Music/DJ Music/ or your preferred folder"
echo ""
echo "3. Import to Rekordbox:"
echo "   - Open Rekordbox"
echo "   - File → Import → Select your download folder"
echo "   - Wait for analysis to complete"
echo ""
echo "4. Create playlist and export to USB:"
echo "   - Create new playlist in Rekordbox"
echo "   - Add all imported tracks"
echo "   - Drag playlist to USB device in Rekordbox sidebar"
echo "   - Wait for export to complete"
echo ""
echo "5. Test on CDJ-2000:"
echo "   - Safely eject USB from Rekordbox"
echo "   - Insert into CDJ-2000"
echo "   - Your playlist will appear in the CDJ browser"
echo ""
echo "USB Path: $USB_PATH"
echo ""
