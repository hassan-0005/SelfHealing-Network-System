import psutil
import time
import random
import threading

class NetworkEngine:
    def __init__(self):
        self.prev_io = psutil.net_io_counters()
        self.health_score = 100
        self.logs = []

    def get_stats(self):
        curr_io = psutil.net_io_counters()
        
        # Calculate real speeds
        upload_speed = (curr_io.bytes_sent - self.prev_io.bytes_sent) / 1024 / 1024
        download_speed = (curr_io.bytes_recv - self.prev_io.bytes_recv) / 1024 / 1024
        self.prev_io = curr_io

        # Simulate packet loss and AI detection
        packet_loss = round(random.uniform(0, 0.5), 2)
        if random.random() > 0.9: packet_loss = round(random.uniform(2, 5), 2)

        ai_action = self.ai_self_heal(packet_loss, download_speed)

        return {
            "upload": round(upload_speed, 2),
            "download": round(download_speed, 2),
            "packet_loss": packet_loss,
            "cpu": psutil.cpu_percent(),
            "ram": psutil.virtual_memory().percent,
            "health": self.health_score,
            "ai_msg": ai_action
        }

    def ai_self_heal(self, packet_loss, download):
        if packet_loss > 2.0:
            self.health_score -= 5
            return "⚠️ High Packet Loss! AI Re-routing traffic to Node-B..."
        if download > 80: # Simulated threshold
            return "🚀 Congestion Detected! AI Throttling heavy users..."
        
        if self.health_score < 100: self.health_score += 1
        return "✅ System Optimal - Monitoring Traffic"
