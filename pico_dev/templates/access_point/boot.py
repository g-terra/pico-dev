import network
import time
import secrets

ap = network.WLAN(network.AP_IF)
ap.config(essid=secrets.SSID, password=secrets.PASSWORD)  # Minimum 8 characters
ap.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.4.1', '0.0.0.0'))
ap.active(True)

for _ in range(10):
    if ap.active():
        print("Access Point active")
        print("IP address:", ap.ifconfig()[0])
        break
    time.sleep(0.5)
else:
    print("Failed to activate Access Point")
