# config_tool.py
import sys
from e22_usb import E22USB

def print_usage():
    print("Usage: python config_tool.py <PORT> [command] [value]")
    print("Examples:")
    print("  python config_tool.py /dev/ttyUSB0 read")
    print("  python config_tool.py /dev/ttyUSB0 channel 25")
    print("  python config_tool.py /dev/ttyUSB0 power 17")
    sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print_usage()

    port = sys.argv[1]
    action = sys.argv[2] if len(sys.argv) > 2 else "read"

    # Open module directly in configuration mode
    lora = E22USB(port, baud=9600)
    lora.open(cfg_mode=True)

    try:
        if action == "read":
            cfg = lora.get_config()
            print("\n📊 Module Parameters:")
            print(f"  Address   : 0x{cfg['addr']:04X}")
            print(f"  Channel   : {cfg['ch']}  →  {cfg['freq']:.3f} MHz")
            print(f"  UART Baud : {cfg['uart']}")
            print(f"  Air Rate  : {cfg['air']} bps\n")

        elif action == "channel":
            if len(sys.argv) != 4:
                print("❌ Error: Missing channel value.")
                print_usage()
            new_ch = int(sys.argv[3])
            if not (0 <= new_ch <= 80):
                print("❌ Error: Channel must be between 0 and 80.")
                sys.exit(1)
            lora.write_reg(0x05, bytes([new_ch]))
            print(f"✅ Channel updated to {new_ch} ({850.125 + new_ch:.3f} MHz)")

        elif action == "power":
            if len(sys.argv) != 4:
                print("❌ Error: Missing power value.")
                print_usage()
            new_dbm = int(sys.argv[3])
            power_map = {22: 0, 17: 1, 13: 2, 10: 3}
            if new_dbm not in power_map:
                print("❌ Error: Valid power values are 22, 17, 13, or 10 dBm.")
                sys.exit(1)
            # Read current options register, modify power bits (6-7), write back
            opts = lora.read_reg(0x04, 2)
            opts[1] = (opts[1] & 0x3F) | (power_map[new_dbm] << 6)
            lora.write_reg(0x04, opts)
            print(f"✅ Transmit power updated to {new_dbm} dBm")

        else:
            print(f"❌ Unknown action: {action}")
            print_usage()

    except Exception as e:
        print(f"⚠️ Error: {e}")
    finally:
        lora.close()

if __name__ == "__main__":
    main()