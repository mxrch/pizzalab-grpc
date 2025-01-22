import asyncio

from pizzalab.grpc import pizzarpc

from grpclib.client import Channel
from rich import print


async def main():
    channel = Channel(host="127.0.0.1", port=50051)
    service = pizzarpc.PizzaServiceStub(channel)
    response = await service.get_menu(pizzarpc.MenuRequest())
    print("[bold]Menu:[/bold]")
    for pizza in response.pizzas:
        print(f"- [bold]{pizza.name}[/bold]: {pizza.description} - {pizza.price}€")
        print(f"  Toppings: {', '.join(topping.name for topping in pizza.toppings)}")
        print(f"  Base sauce: {pizza.base_sauce.name}")

    response = await service.order_pizza(pizzarpc.OrderRequest(
        customer_name="Alice",
        pizza_name=response.pizzas[0].name,
        quantity=2,
        toppings=[pizzarpc.Topping.OLIVE_OIL, pizzarpc.Topping.MUSHROOM, pizzarpc.Topping.MAYO]
    ))
    print(f"\n[bold]Order response:[/bold] {response.message}")
    print(f"Order ID: {response.order_id}")
    print(f"Total price: {response.total_price}€")
    print(f"Ordered pizza: {response.pizza.name}")
    print(f"Toppings: {', '.join(topping.name for topping in response.pizza.toppings)}")
    print(f"Quantity: {response.quantity}")

    # don't forget to close the channel when done!
    channel.close()


if __name__ == "__main__":
    asyncio.run(main())