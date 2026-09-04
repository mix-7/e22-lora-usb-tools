# e22_usb.py
import serial
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class E22USB:
    """Low-level driver for Ebyte E22-xxxT22U USB LoRa modules."""

    CMD_WRITE = 0xC0
    CMD_READ  = 0xC1
    CMD_MODE  = bytes([0xC0, 0xC1, 0xC2, 0xC3, 0x02])
    MODE_TX   = 0x00  # Transparent transmission mode
    MODE_CFG  = 0x01  # Configuration mode

    def __init__(self, port: str, baud: int = 9600):
        self.port = port
        self.baud = baud
        self.ser = None
        self.in_cfg = False

    def open(self, cfg_mode=False):
        """Open serial connection to the module."""
        baudrate = 9600 if cfg_mode else self.baud
        self.ser = serial.Serial(self.port, baudrate, timeout=0.5)
        self.in_cfg = cfg_mode
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        time.sleep(0.1)
        logging.info(f"Connected to {self.port} @ {baudrate} baud")

    def close(self):
        """Close serial connection."""
        if self.ser and self.ser.is_open:
            self.ser.close()
            logging.info("Connection closed")

    def _switch(self, mode: int) -> bool:
        """Internal method to switch module mode via software command."""
        self.ser.write(self.CMD_MODE + bytes([mode]))
        time.sleep(0.15)
        resp = self.ser.read(6)
        # Expect response: C1 06 01 <mode>
        ok = len(resp) >= 2 and resp[0:2] == bytes([0xC1, 0x06])
        if ok:
            self.in_cfg = (mode == self.MODE_CFG)
            self.ser.baudrate = 9600 if self.in_cfg else self.baud
        return ok

    def enter_cfg(self):
        """Switch to configuration mode."""
        if self.in_cfg:
            return True
        return self._switch(self.MODE_CFG)

    def exit_cfg(self):
        """Switch to transparent transmission mode."""
        if not self.in_cfg:
            return True
        return self._switch(self.MODE_TX)

    def send(self, data: bytes):
        """Send raw data in transparent mode."""
        if self.in_cfg:
            self.exit_cfg()
        self.ser.write(data)
        time.sleep(0.1)  # Allow time for LoRa packet transmission

    def read_reg(self, addr: int, length: int) -> bytes:
        """Read module register(s)."""
        if not self.in_cfg:
            self.enter_cfg()
        self.ser.write(bytes([self.CMD_READ, addr, length]))
        time.sleep(0.05)
        resp = self.ser.read(10)
        if len(resp) < 3 or resp[0] != self.CMD_READ:
            raise RuntimeError(f"Register read failed: {resp.hex()}")
        return resp[3:3+length]

    def write_reg(self, addr: int, data: bytes) -> bool:
        """Write to module register(s)."""
        if not self.in_cfg:
            self.enter_cfg()
        cmd = bytes([self.CMD_WRITE, addr, len(data)]) + data
        self.ser.write(cmd)
        time.sleep(0.05)
        resp = self.ser.read(10)
        # Success indicated by module echoing command with C1 header
        return resp[:len(cmd)+1] == bytes([self.CMD_READ]) + cmd[1:]

    def get_config(self) -> dict:
        """Read and parse key module parameters."""
        if not self.in_cfg:
            self.enter_cfg()
        cfg = {}
        cfg['addr'] = int.from_bytes(self.read_reg(0x00, 2), 'big')
        cfg['ch'] = self.read_reg(0x05, 1)[0]
        cfg['freq'] = 850.125 + cfg['ch']
        s = self.read_reg(0x03, 2)
        # UART speed: bits 7-5
        uart_idx = (s[0] >> 5) & 0x07
        cfg['uart'] = [1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200][uart_idx]
        # Air rate: bits 2-0
        air_idx = s[0] & 0x07
        cfg['air'] = [2400, 4800, 9600, 19200, 38400, 62500][air_idx - 2] if air_idx >= 2 else 2400
        return cfg

    def enable_sw_switch(self):
        """Enable software mode switching (one-time setup)."""
        if not self.in_cfg:
            self.enter_cfg()
        func_reg = self.read_reg(0x06, 1)[0]
        # Bit 2 controls software mode switch
        if not (func_reg & 0x04):
            self.write_reg(0x06, bytes([func_reg | 0x04]))
            logging.info("✅ Software Mode Switch enabled")