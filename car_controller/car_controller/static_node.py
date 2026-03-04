import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math
import time

class StaticControlNode(Node):
    def __init__(self):
        super().__init__('static_control_node')
        
        # /cmd_vel 토픽 발행자
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        
        # 0.1초 주기로 발행 (통신 부하를 고려하여 10Hz로 설정)
        self.timer = self.create_timer(0.1, self.timer_callback)
        
        self.start_time = time.time()
        self.get_logger().info('Steering Swing Node (-20 to 20 deg) started.')

    def timer_callback(self):
        elapsed_time = time.time() - self.start_time
        msg = Twist()

        # 1. 속도(Linear): 테스트를 위해 0.3 정도로 고정 (필요시 수정)
        msg.linear.x = 0.3
        
        # 2. 조향(Angular): -20도 ~ 20도 사이를 약 4초 주기로 왕복
        # math.sin은 -1.0 ~ 1.0을 반환하므로 20.0을 곱함
        msg.angular.z = 20.0 * math.sin(elapsed_time * 1.5)
        
        # 데이터 타입 강제 변환 (float64)
        msg.linear.x = float(msg.linear.x)
        msg.angular.z = float(msg.angular.z)

        self.publisher_.publish(msg)
        # self.get_logger().info(f'Target Angle: {msg.angular.z:.1f} deg')

def main(args=None):
    rclpy.init(args=args)
    node = StaticControlNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        stop_msg = Twist()
        node.publisher_.publish(stop_msg)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()