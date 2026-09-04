# lora_app.py
import sys
import time
import threading
from e22_usb import E22USB

# Set to True for the first run on a new module to enable software mode switching
FIRST_RUN = False

class LoRaApp:
    """Interactive LoRa chat application for E22 USB modules."""

    def __init__(self, port: str):
        self.lora = E22USB(port, baud=9600)
        self.running = True

    def first_setup(self):
        """Guided setup to enable software mode switching."""
        print("\n🔧 FIRST RUN: Enabling software mode switching...")
        print("1️⃣  Press and hold the button on the module for >1.5 seconds")
        print("2️⃣  Release it (the red LED should stay solid)")
        print("3️⃣  Press Enter to continue...")
        input()
        self.lora.open(cfg_mode=True)
        self.lora.enable_sw_switch()
        cfg = self.lora.get_config()
        print(f"✅ Setup complete. Channel: {cfg['ch']}, Frequency: {cfg['freq']} MHz")
        self.lora.close()

    def run(self):
        """Main application loop."""
        if FIRST_RUN:
            self.first_setup()
            print("\n🔁 Please set FIRST_RUN = False in the script and run again.")
            return

        self.lora.open()
        print(f"\n📡 LoRa Chat started on {self.lora.port}")
        print("Commands: send <message> | quit")
        print("-" * 30)

        # Start background receiver thread
        threading.Thread(target=self._rx_loop, daemon=True).start()

        try:
            while self.running:
                cmd = input("> ").strip()
                if cmd.startswith("send "):
                    self.lora.send(f"{cmd[5:]}\n".encode('utf-8'))
                    print("📤 Message sent")
                elif cmd == "quit":
                    self.running = False
                elif cmd:
                    print("❓ Unknown command. Use: send <message> | quit")
        except KeyboardInterrupt:
            self.running = False
        finally:
            self.lora.close()
            print("\n👋 Session ended")

    def _rx_loop(self):
        """Background thread to receive and display incoming messages."""
        while self.running:
            try:
                if self.lora.ser.in_waiting > 0:
                    raw = self.lora.ser.read(self.lora.ser.in_waiting)
                    # Filter out ACK or empty lines
                    decoded = raw.decode('utf-8', errors='ignore').strip()
                    if decoded and decoded != "ACK":
                        print(f"\n💬 Received: {decoded}")
                        print("> ", end='', flush=True)
            except Exception as e:
                logging.debug(f"RX error: {e}")
            time.sleep(0.05)

if __name__ == '__main__':
    port = sys.argv[1] if len(sys.argv) > 1 else '/dev/ttyUSB0'
    LoRaApp(port).run()