import grpc
import train_service_pb2
import train_service_pb2_grpc
from rich import print

def run():
    try:
        channel = grpc.insecure_channel('localhost:50051')
        stub = train_service_pb2_grpc.TrainServiceStub(channel)

        while True:
            print("\n[bold cyan]1. Purchase Ticket[/bold cyan]")
            print("[bold cyan]2. Get Receipt[/bold cyan]")
            print("[bold cyan]3. View Users By Section[/bold cyan]")
            print("[bold cyan]4. Remove User[/bold cyan]")
            print("[bold cyan]5. Modify User Seat[/bold cyan]")
            print("[bold cyan]6. Exit[/bold cyan]")

            choice = input("Enter your choice: ")

            if choice == '1':
                first_name = input("Enter first name: ")
                last_name = input("Enter last name: ")
                email = input("Enter email: ")
                user = train_service_pb2.User(first_name=first_name, last_name=last_name, email=email)
                departure = "London"
                to = "France"
                response = stub.PurchaseTicket(train_service_pb2.PurchaseTicketRequest(departure=departure, to=to, user=user))
                print(f"[bold green]Receipt ID: {response.receipt_id}[/bold green]")

            elif choice == '2':
                try:
                    receipt_id = input("Enter receipt id: ")
                    response = stub.GetReceipt(train_service_pb2.GetReceiptRequest(receipt_id=receipt_id))
                    print(f"[bold green]Receipt: {response}[/bold green]")
                except grpc.RpcError as e:
                    print(f"[bold red]{e.details()}[/bold red]")
                except Exception as e:
                    print(f"[bold red]An unexpected error occurred: {str(e)}[/bold red]")

            elif choice == '3':
                section = input("Enter section (A/B): ")
                response = stub.ViewUsersBySection(train_service_pb2.ViewUsersBySectionRequest(section=section))
                for user in response.users:
                    print(f"[bold green]User: {user}[/bold green]")

            elif choice == '4':
                try:
                    receipt_id = input("Enter receipt id: ")
                    stub.RemoveUser(train_service_pb2.RemoveUserRequest(receipt_id=receipt_id))
                    print("[bold red]User removed[/bold red]")
                except grpc.RpcError as e:
                    print(f"[bold red]{e.details()}[/bold red]")
                except Exception as e:
                    print(f"[bold red]An unexpected error occurred: {str(e)}[/bold red]")

            elif choice == '5':
                try:
                    receipt_id = input("Enter receipt id: ")
                    new_seat = input("Enter new seat: ")
                    stub.ModifyUserSeat(train_service_pb2.ModifyUserSeatRequest(receipt_id=receipt_id, new_seat=new_seat))
                    print("[bold yellow]Seat modified[/bold yellow]")
                except grpc.RpcError as e:
                    print(f"[bold red]{e.details()}[/bold red]")
                except Exception as e:
                    print(f"[bold red]An unexpected error occurred: {str(e)}[/bold red]")

            elif choice == '6':
                break

            else:
                print("[bold red]Invalid choice. Please try again.[/bold red]")
    
    except grpc.RpcError as e:
        print(f"[bold red]A gRPC error occurred: {e.details()}[/bold red]")
    except Exception as e:
        print(f"[bold red]An unexpected error occurred: {str(e)}[/bold red]")

if __name__ == "__main__":
    run()