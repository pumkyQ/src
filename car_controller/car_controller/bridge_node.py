import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import serial
import time

class ArduinoBridge(Node):
    def __init__(self):
        super().__init__('arduino_bridge')
        
        # 1. 시리얼 설정 (아두이노 포트 확인 필수: /dev/ttyACM0 또는 /dev/ttyUSB0)
        self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0.1)
        
        # 2. 구독자 설정 (cmd_vel 토픽을 받음)
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.cmd_vel_callback,
            10)
        
        self.get_logger().info('Arduino Bridge Node has been started')

    def cmd_vel_callback(self, msg):
        # 선속도(x)를 Throttle(TH)로 변환 (현재 아두이노는 -1.0 ~ 1.0 권장)
        throttle = msg.linear.x
        
        # 각속도(z)를 조향각(SA)으로 변환 (예: -20 ~ 20도)
        # 실제 차량의 회전 반경에 맞춰 계수를 조정해야 합니다.
        steer_angle = msg.angular.z * 15.0  # 임의의 계수 15를 곱함
        
        # 아두이노 규격에 맞게 문자열 생성
        th_cmd = f"TH {throttle:.2f}\n"
        sa_cmd = f"SA {steer_angle:.1f}\n"
        
        # 시리얼 전송
        try:
            self.ser.write(th_cmd.encode())
            self.ser.write(sa_cmd.encode())
            self.get_logger().info(f'Sent: {th_cmd.strip()}, {sa_cmd.strip()}')
        except Exception as e:
            self.get_logger().error(f'Serial error: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = ArduinoBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.ser.close()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()