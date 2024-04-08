import unittest
from limit.limit_order_agent import LimitOrderAgent
from trading_framework.execution_client import ExecutionClient


class LimitOrderAgentTest(unittest.TestCase):

    def setUp(self):
        self.execution_client_mock = ExecutionClient
        self.limit_order_agent = LimitOrderAgent(self.execution_client_mock)

    def test_add_order(self):
        self.limit_order_agent.add_order('buy', 'IBM', 1000, 99.5)
        self.assertEqual(len(self.limit_order_agent.orders), 1)
        print("test_add_order Passed Successfully")

    def test_execute_buy_order(self):
        self.limit_order_agent.add_order('buy', 'IBM', 1000, 100.5)
        self.limit_order_agent.on_price_tick('IBM', 99.0)
        self.assertTrue(self.limit_order_agent.orders)
        print("test_execute_buy_order Passed Successfully")

    def test_execute_sell_order(self):
        self.limit_order_agent.add_order('sell', 'IBM', 1000, 101.0)
        self.limit_order_agent.on_price_tick('IBM', 102.0)
        self.assertFalse(self.limit_order_agent.orders)
        print("test_execute_sell_order Passed Successfully")

    def test_execute_wrong_order(self):
        self.limit_order_agent.add_order('wrong', 'IBM', 1000, 101.0)
        self.limit_order_agent.price_tick('IBM', 102.0)
        self.assertTrue(self.limit_order_agent.orders)
        print("test_execute_sell_order Passed Successfully")

        def test_retry_held_orders_multiple_products(self):
        self.limit_order_agent.add_order('buy', 'IBM', 1000, 100.5)
        self.limit_order_agent.add_order('buy', 'GOOG', 2000, 1200.0)
        self.limit_order_agent.on_price_tick('IBM', 101.0)
        self.limit_order_agent.on_price_tick('GOOG', 1150.0)
        self.assertTrue(self.limit_order_agent.orders)
        self.limit_order_agent.on_price_tick('IBM', 99.0)
        self.limit_order_agent.on_price_tick('GOOG', 1050.0)
        self.assertFalse(self.limit_order_agent.orders)
        print("test_retry_held_orders_multiple_products Passed Successfully")

    def test_execute_orders_multiple_products(self):
        self.limit_order_agent.add_order('buy', 'IBM', 1000, 100.5)
        self.limit_order_agent.add_order('sell', 'GOOG', 2000, 1150.0)
        self.limit_order_agent.on_price_tick('IBM', 99.0)
        self.limit_order_agent.on_price_tick('GOOG', 1200.0)
        self.assertFalse(self.limit_order_agent.orders)
        print("test_execute_orders_multiple_products Passed Successfully")

    def test_retry_held_orders_multiple_amounts(self):
        self.limit_order_agent.add_order('buy', 'IBM', 1000, 100.5)
        self.limit_order_agent.add_order('buy', 'IBM', 2000, 99.5)
        self.limit_order_agent.on_price_tick('IBM', 101.0)
        self.assertTrue(self.limit_order_agent.orders)
        self.limit_order_agent.on_price_tick('IBM', 98.0)
        self.assertFalse(self.limit_order_agent.orders)
        print("test_retry_held_orders_multiple_amounts Passed Successfully")

    def test_execute_orders_multiple_amounts(self):
        self.limit_order_agent.add_order('buy', 'IBM', 1000, 100.5)
        self.limit_order_agent.add_order('buy', 'IBM', 2000, 99.5)
        self.limit_order_agent.on_price_tick('IBM', 97.0)
        self.assertFalse(self.limit_order_agent.orders)
        print("test_execute_orders_multiple_amounts Passed Successfully")
    

if __name__ == '__main__':
    unittest.main()