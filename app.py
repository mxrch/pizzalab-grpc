import asyncio
import random
from concurrent import futures

from pizzalab.grpc import pizzarpc
from pizzalab.logging import LOG

from grpclib.server import Server
from grpclib.reflection.service import ServerReflection
from uuid import uuid4


mock_words = ["Super", "Chilli", "Pizza", "Vegan", "Italian", "French", "Saucy", "Extra", "Original", "Classic"]
mock_pizzas = [
    pizzarpc.Pizza(
        name=(pizza_name := " ".join(random.choices(mock_words, k=3))),
        description=f'You should buy this super {pizza_name} !',
        price=float(random.randint(5, 20)),
        toppings=random.choices(list(pizzarpc.Topping), k=3),
        base_sauce=random.choice(list(pizzarpc.BaseSauce)),
    ) for _ in range(10)
]

class PizzaService(pizzarpc.PizzaServiceBase):
    async def get_menu(self, request: pizzarpc.MenuRequest) -> pizzarpc.MenuResponse:
        LOG.info("GetMenu request received")
        return pizzarpc.MenuResponse(pizzas=mock_pizzas)

    async def order_pizza(self, request: pizzarpc.OrderRequest) -> pizzarpc.OrderResponse:
        LOG.info("OrderPizza request received")
        
        pizzas = [pizza for pizza in mock_pizzas if pizza.name == request.pizza_name]
        if not pizzas:
            return pizzarpc.OrderResponse(success=False, error=f"Pizza {request.pizza_name} not found :( be sure to get the menu first !")

        pizza = pizzas[0]
        LOG.info(f"Ordering pizza {pizza.name}")

        # Adding toppings without duplicates
        pizza.toppings.extend([topping for topping in request.toppings if topping not in pizza.toppings])

        return pizzarpc.OrderResponse(
            success=True,
            pizza=pizza,
            message=f"Dear {request.customer_name}, your pizza {pizza.name} is on its way !",
            order_id=str(uuid4()),
            quantity=request.quantity,
            total_price=pizza.price * request.quantity
        )

async def main():
    services = [PizzaService()]
    services = ServerReflection.extend(services)

    server = Server(services)
    await server.start("0.0.0.0", 50051)
    await server.wait_closed()

if __name__ == "__main__":
    LOG.info("Starting PizzaLab server")
    asyncio.run(main())