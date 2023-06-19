import datetime
import turtle

class Node:
    def __init__(self, company_id):
        self.company_id = company_id
        self.products = []

    def add_product(self, product):
        self.products.append(product)

class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.user_products = {}

    def add_node(self, company_id):
        if company_id not in self.nodes:
            self.nodes[company_id] = Node(company_id)
            self.edges[company_id] = []

    def add_edge(self, node1, node2):
        if node1 in self.nodes and node2 in self.nodes:
            self.edges[node1].append(node2)
            self.edges[node2].append(node1)

    def get_connections(self, p):
        if p in self.nodes:
            return self.edges[p]
        return self.edges

    def add_product_to_node(self, company_id, product):
        if company_id in self.nodes:
            node = self.nodes[company_id]
            node.add_product(product)
        
    def get_products_by_node(self, company_id):
        if company_id in self.nodes:
            node = self.nodes[company_id]
            return node.products
        return []

    def get_all_nodes(self):
        return list(self.nodes.keys())

    def add_user_product(self, user_id, product):
        if user_id in self.user_products:
            self.user_products[user_id].append(product)
        else:
            self.user_products[user_id] = [product]

    def get_user_products(self, user_id):
        if user_id in self.user_products:
            return self.user_products[user_id]
        return []
        
    def get_companies_by_user(self, user_id):
        companies = []
        for company_id in self.nodes:
            products = self.get_products_by_node(company_id)
            for product in products:
                if product['user_id'] == user_id:
                    companies.append(company_id)
        return companies

class PriorityQueue:
    def __init__(self):
        self.queue = []

    def push(self, priority, item):
        self.queue.append((priority, item))

    def pop(self):
        if not self.is_empty():
            min_index = 0
            for i in range(1, len(self.queue)):
                if self.queue[i][0] < self.queue[min_index][0]:
                    min_index = i
            return self.queue.pop(min_index)[1]

    def is_empty(self):
        return len(self.queue) == 0

def validate_date(date_str):
    try:
        order_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        current_date = datetime.datetime.now().date()
        if order_date.date() <= current_date:
            return True
        else:
            print("Order date should be in the past.")
            return False
    except ValueError:
        return False

def add_product(user):
    r = {}
    print("   ")
    print("=== Add Product Details ===")
    name = input("Enter the product name: ")
    date = input("Enter the date of order (YYYY-MM-DD): ")
    priority_queue = PriorityQueue()
    priority_queue.push(0, date)  # Push the date into the priority queue
    while not priority_queue.is_empty():
        date = priority_queue.pop()
        if validate_date(date):
            break
        else:
            print("Invalid date format. Please enter a valid date in YYYY-MM-DD format.")
            date = input("Enter the date of order (YYYY-MM-DD): ")
            priority_queue.push(0, date)  # Push the new date into the priority queue
    try:
        company_id = int(input("Enter the company ID: "))
        product = {'name': name, 'date': date, 'user_id': user} #add user id to the product
        r[user]=product
        graph.add_node(company_id)
        graph.add_product_to_node(company_id, product)
        graph.add_user_product(user, product)  # Store the product for the user
        print("Product details added successfully.")
    except ValueError:
        print("Invalid company ID. Please enter a valid integer.")

def check_delivery_status():
    print("=== Delivery Status ===")
    priority_queue = PriorityQueue()
    for company_id in graph.get_all_nodes():
        products = graph.get_products_by_node(company_id)
        if products:
            order_date = datetime.datetime.strptime(products[0]['date'], "%Y-%m-%d").date()
            current_date = datetime.datetime.now().date()
            days_difference = (current_date - order_date).days
            delivery_status = ''

            if days_difference < 3:
                delivery_status = 'In-transit'
            elif 3 <= days_difference <= 5:
                delivery_status = 'Out of delivery'
            else:
                delivery_status = 'Delivered'

            print(f"Delivery status for Company {company_id}:")
            print(f"Number of products: {len(products)}")
            for product in products:
                print(f"Delivery status {product['name']} from Company {company_id} ordered on {product['date']} - {delivery_status}")
        else:
            print(f"No products found for Company {company_id}")
    else:
        print("No deliveries beyond this!")

def get_products_by_company():
    print("=== Get Products by Company ===")
    company_id = int(input("Enter the company ID: "))
    products = graph.get_products_by_node(company_id)
    if products:
        print(f"Products for Company {company_id}:")
        print(f"Number of products: {len(products)}")
        for product in products:
            print(f"Product Name: {product['name']}, Order Date: {product['date']}")
    else:
        print(f"No products found for Company {company_id}")

def calculate_average_delivery_time():
    print("=== Calculate Average Delivery Time ===")
    total_delivery_time = 0
    count = 0
    for company_id in graph.get_all_nodes():
        products = graph.get_products_by_node(company_id)
        if products:
            for product in products:
                order_date = datetime.datetime.strptime(product['date'], "%Y-%m-%d").date()
                current_date = datetime.datetime.now().date()
                days_difference = (current_date - order_date).days
                total_delivery_time += days_difference
                count += 1
    if count > 0:
        average_delivery_time = total_delivery_time / count
        print(f"The average delivery time for {count} products is: {average_delivery_time:.2f} days")
    else:
        print("No products found.")

def search_product_by_name():
    print("=== Search Product by Name ===")
    product_name = input("Enter the product name to search: ")
    found = False
    for company_id in graph.get_all_nodes():
        products = graph.get_products_by_node(company_id)
        for product in products:
            if product['name'] == product_name:
                print(f"Product found in Company {company_id}:")
                print(f"Product Name: {product['name']}, Order Date: {product['date']}")
                found = True
    if not found:
        print(f"No products found with the name '{product_name}'.")

def get_companies_by_user():
    print("=== Get Companies by User ===")
    user_id = input("Enter the user name : ")
    companies = graph.get_companies_by_user(user_id)
    if companies:
        print(f"Companies with User {user_id}:")
        for company_id in companies:
            print(f"Company ID: {company_id}")
    else:
        print(f"No companies found for User {user_id}")

def main():
    n = int(input("No. of Users: "))
    names = []
    for i in range(n):
        names.append(input(f"Username {i+1} : " ))
        
    while True:
        print("   ")
        print("============     * Product Management Menu *    ============")
        print("1. Add Product Details")
        print("2. Check Delivery Status")
        print("3. Get Products by Company")
        print("4. Calculate Average Delivery Time")
        print("5. Get product names by user")
        print("6. Search Product by Name")
        print("7. Get Companies by users")
        print("8. Show Company IDs")
        print("9. Show the Companies using edges connected with users")
        print("10. Exit")
        choice = input("Enter your choice (1-10): ")
        if choice == '1':
            for user in names:
                add_product(user)
        elif choice == '2':
            check_delivery_status()
        elif choice == '3':
            get_products_by_company()
        elif choice == '4':
            calculate_average_delivery_time()
        elif choice == '5':
            for i in names:
                user = i
                products = graph.get_user_products(user)
                print(f"Products for user {user}:")
                print(f"Number of products: {len(products)}")
                for product in products:
                    print(f"Product Name: {product['name']}, Order Date: {product['date']}")
        elif choice == '6':
            search_product_by_name()
        elif choice == '7':
            get_companies_by_user()
        elif choice == '8':
            x = graph.get_all_nodes()
            print(x)
        elif choice == '9':
            x = graph.get_all_nodes()
            for i in range(n):
                for j in x:
                    graph.add_edge(i, j)
                connections = graph.get_connections(i)
                # Print the connected companies
                print(f"User {names[i]} is connected to the following companies:")
                print(connections)
                # for k in connections:
                #     print(k)
        elif choice == '10':
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    graph = Graph()
    main()


# Set up the turtle screen
screen = turtle.Screen()
screen.setup(1200, 600)

# Create the turtle objects
t1 = turtle.Turtle()
t2 = turtle.Turtle()
t1.speed(20)
t2.speed(20)

# Define colors for the circles
circle_colors = ['orange', 'gray']

# Draw the central circle for the first output
radius = 50
t1.penup()
t1.goto(-300, -radius)
t1.pendown()
t1.color(circle_colors[0])
t1.begin_fill()
t1.circle(radius)
t1.end_fill()

# Draw the outer circles and connecting lines for the first output
num_shapes = 8
angle = 360 / num_shapes

for i in range(num_shapes):
    t1.penup()
    t1.goto(-320, 0)
    t1.pendown()
    t1.setheading(i * angle)
    t1.forward(radius * 2)

    # Draw the square for the first output
    t1.color(circle_colors[1])
    t1.begin_fill()
    for _ in range(4):
        t1.forward(radius)
        t1.right(90)
    t1.end_fill()

# Draw the central circle for the second output
t2.penup()
t2.goto(200, 0)
t2.pendown()
t2.color(circle_colors[0])
t2.begin_fill()
t2.circle(radius)
t2.end_fill()

# Connect the second output circle with adjacent two blue squares in the first output
for i in range(2):
    # Connect each side of the second output circle with the corresponding blue square
    t2.penup()
    t2.goto(175, 0)
    t2.pendown()
    t2.setheading((i+0.25) * angle)
    t2.color('orange')
    t2.pensize(5)
    t2.forward(radius)
    t2.goto(-259 + radius, 0 + (radius * 2 * i))

# Hide the turtle cursors
t1.hideturtle()
t2.hideturtle()

#legend
t = turtle.Turtle()

legend_items = {
    "Companies": "gray",
    "Users": "orange",
}

x = -150
y = 150
t.penup()
t.goto(x, y)
t.pendown()

for item, color in legend_items.items():
    t.color(color)
    t.begin_fill()
    for _ in range(4):
        t.forward(20)
        t.right(90)
    t.end_fill()
    t.penup()
    t.forward(30)
    t.pendown()
    t.write(item, align="left", font=("Arial", 12, "normal"))
    t.penup()
    t.forward(80)
    t.pendown()

t.hideturtle()
turtle.exitonclick()

# Close the turtle graphics window
turtle.done()
