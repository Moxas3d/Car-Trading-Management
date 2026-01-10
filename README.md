# Car Trade Management

An Odoo module for managing a car trading business. This module helps you manage your car inventory, purchases, sales, and financial transactions.

## Features

- **Car Management:**
  - Maintain a detailed record of each car in your inventory.
  - Track car details like VIN, brand, model, year, and purchase price.
  - Manage the state of each car (Draft, Purchased, Available, Sold).

- **Purchase Order Management:**
  - Create and manage purchase orders for new cars.
  - Track the vendor, cars being purchased, and total purchase price.
  - Confirm orders, mark them as done, or cancel them.
  - Smart buttons to easily access related cars and vendors.
  - Chatter and state tracking for better collaboration.

- **Sales Order Management:**
  - Create and manage sales orders for selling cars.
  - Select a customer, car, and selling price.
  - Manage installment plans for customers.

- **Partner Management:**
  - Manage both customers and vendors.
  - Store contact information and other relevant details.

- **Installment Strategies:**
  - Define different installment strategies for car sales.
  - Set the number of months, down payment percentage, and bank.
  - Track important changes in the chatter.

- **Bank Management:**
  - Manage a list of financing banks.
  - Store bank details like name, interest rate, and max installment months.

- **Reporting:**
  - Generate XLSX reports for banks.

## Installation

1. Clone this repository or download the source code.
2. Copy the `car_trade_management` folder to your Odoo `addons` directory.
3. Restart the Odoo server.
4. Go to `Apps` in your Odoo instance.
5. Click on `Update Apps List`.
6. Search for "Car Trade Management" and click `Install`.

## Usage

After installation, you can access the Car Trade Management features from the main Odoo menu. You will find menu items for:

- Cars
- Purchase Orders
- Sales Orders
- Installment Strategies
- Banks
- Partners

## Contributing

Contributions are welcome! If you want to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes.
4. Create a pull request with a clear description of your changes.
