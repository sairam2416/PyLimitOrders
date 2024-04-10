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
        self.limit_order_agent.on_price_tick('IBM', 102.0)
        self.assertTrue(self.limit_order_agent.orders)
        print("test_execute_sell_order Passed Successfully")

    def test_retry_held_orders(self):
        self.limit_order_agent.add_order('buy', 'IBM', 1000, 100.5)
        self.limit_order_agent.on_price_tick('IBM', 101.0)
        self.assertTrue(self.limit_order_agent.orders)
        self.limit_order_agent.on_price_tick('IBM', 99.0)
        self.assertFalse(self.limit_order_agent.orders)
        print("test_retry_held_orders Passed Successfully")

    def test_add_order_different_product(self):
        self.limit_order_agent.add_order('buy', 'GOOG', 2000, 1200.0)
        self.assertEqual(len(self.limit_order_agent.orders), 1)
        print("test_add_order_different_product Passed Successfully")

    def test_execute_buy_order_different_product(self):
        self.limit_order_agent.add_order('buy', 'GOOG', 2000, 1100.0)
        self.limit_order_agent.on_price_tick('GOOG', 1050.0)
        self.assertTrue(self.limit_order_agent.orders)
        print("test_execute_buy_order_different_product Passed Successfully")

    def test_execute_sell_order_different_product(self):
        self.limit_order_agent.add_order('sell', 'GOOG', 2000, 950.0)
        self.limit_order_agent.on_price_tick('GOOG', 900.0)
        self.assertFalse(self.limit_order_agent.orders)
        print("test_execute_sell_order_different_product Passed Successfully")

    def test_execute_wrong_order_different_product(self):
        self.limit_order_agent.add_order('wrong', 'GOOG', 2000, 1000.0)
        self.limit_order_agent.on_price_tick('GOOG', 1050.0)
        self.assertTrue(self.limit_order_agent.orders)
        print("test_execute_wrong_order_different_product Passed Successfully")

    def test_retry_held_orders_different_product(self):
        self.limit_order_agent.add_order('buy', 'GOOG', 2000, 1100.0)
        self.limit_order_agent.on_price_tick('GOOG', 1150.0)
        self.assertTrue(self.limit_order_agent.orders)
        self.limit_order_agent.on_price_tick('GOOG', 1050.0)
        self.assertFalse(self.limit_order_agent.orders)
        print("test_retry_held_orders_different_product Passed Successfully")

    def test_add_order_different_amount(self):
        self.limit_order_agent.add_order('buy', 'MSFT', 500, 50.0)
        self.assertEqual(len(self.limit_order_agent.orders), 1)
        print("test_add_order_different_amount Passed Successfully")

    def test_execute_buy_order_different_amount(self):
        self.limit_order_agent.add_order('buy', 'MSFT', 500, 55.0)
        self.limit_order_agent.on_price_tick('MSFT', 52.0)
        self.assertTrue(self.limit_order_agent.orders)
        print("test_execute_buy_order_different_amount Passed Successfully")

    def test_execute_sell_order_different_amount(self):
        self.limit_order_agent.add_order('sell', 'MSFT', 500, 45.0)
        self.limit_order_agent.on_price_tick('MSFT', 40.0)
        self.assertFalse(self.limit_order_agent.orders)
        print("test_execute_sell_order_different_amount Passed Successfully")

    def test_execute_wrong_order_different_amount(self):
        self.limit_order_agent.add_order('wrong', 'MSFT', 500, 47.0)
        self.limit_order_agent.on_price_tick('MSFT', 52.0)
        self.assertTrue(self.limit_order_agent.orders)
        print("test_execute_wrong_order_different_amount Passed Successfully")

    def test_retry_held_orders_different_amount(self):
        self.limit_order_agent.add_order('buy', 'MSFT', 500, 55.0)
        self.limit_order_agent.on_price_tick('MSFT', 60.0)
        self.assertTrue(self.limit_order_agent.orders)
        self.limit_order_agent.on_price_tick('MSFT', 50.0)
        self.assertFalse(self.limit_order_agent.orders)
        print("test_retry_held_orders_different_amount Passed Successfully")

    def test_add_order_different_price_limit(self):
        self.limit_order_agent.add_order('buy', 'AAPL', 1000, 150.0)
        self.assertEqual(len(self.limit_order_agent.orders), 1)
        print("test_add_order_different_price_limit Passed Successfully")

    def test_execute_buy_order_different_price_limit(self):
        self.limit_order_agent.add_order('buy', 'AAPL', 1000, 140.0)
        self.limit_order_agent.on_price_tick('AAPL', 130.0)
        self.assertTrue(self.limit_order_agent.orders)
        print("test_execute_buy_order_different_price_limit Passed Successfully")

    def test_execute_sell_order_different_price_limit(self):
        self.limit_order_agent.add_order('sell', 'AAPL', 1000, 160.0)
        self.limit_order_agent.on_price_tick('AAPL', 170.0)
        self.assertFalse(self.limit_order_agent.orders)
        print("test_execute_sell_order_different_price_limit Passed Successfully")

    def test_execute_wrong_order_different_price_limit(self):
        self.limit_order_agent.add_order('wrong', 'AAPL', 1000, 155.0)
        self.limit_order_agent.on_price_tick('AAPL', 130.0)
        self.assertTrue(self.limit_order_agent.orders)
        print("test_execute_wrong_order_different_price_limit Passed Successfully")

    def test_retry_held_orders_different_price_limit(self):
        self.limit_order_agent.add_order('buy', 'AAPL', 1000, 140.0)
        self.limit_order_agent.on_price_tick('AAPL', 145.0)
        self.assertTrue(self.limit_order_agent.orders)
        self.limit_order_agent.on_price_tick('AAPL', 135.0)
        self.assertFalse(self.limit_order_agent.orders)
        print("test_retry_held_orders_different_price_limit Passed Successfully")


if __name__ == '__main__':
    unittest.main()
