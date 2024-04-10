from trading_framework.execution_client import ExecutionClient, ExecutionException
from trading_framework.price_listener import PriceListener


class LimitOrderAgent(PriceListener):
    def __init__(self, execution_client: ExecutionClient):
        """
        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self.execution_client = execution_client
        self.orders = []

    def on_price_tick(self, product_id: str, price: float):
        # Fetching the current market price of the product
        print(f"Price tick for {product_id}: {price}")
        self.retry_held_orders(product_id, price)

    def retry_held_orders(self, product_id: str, price: float):
        held_orders = [order for order in self.orders if order[0] in ['buy', 'sell'] and order[1] == product_id]
        for order in held_orders:
            flag, order_product_id, amount, limit = order
            if (flag == 'buy' and price <= limit) or (flag == 'sell' and price >= limit):
                self.execute_order(product_id, price, order)

    def get_current_price(self, product_id: str) -> float:
        # Implement a method to fetch the current market price of the product
        return self.execution_client.get_current_price(product_id)

    def execute_order(self, product_id: str, price: float, order=None):
        if order is None:
            for order in self.orders:
                if product_id == order[1]:
                    break
        flag, order_product_id, amount, limit = order
        if product_id == order_product_id:
            print("exec", order_product_id, amount)
            try:
                if flag == 'buy' and price <= limit:
                    self._execute_buy_order(order_product_id, amount)
                elif flag == 'sell' and price >= limit:
                    self._execute_sell_order(order_product_id, amount)
                    # Removing the sold order
                    self.orders.remove(order)
                else:
                    raise ExecutionException
            except ExecutionException:
                print(f"Failed to place an order due to invalid operation")

    def add_order(self, flag: str, product_id: str, amount: int, limit: float):
        # Adding the bought order
        self.orders.append((flag, product_id, amount, limit))

