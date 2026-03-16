# Restaurant Ordering System Report

## Project Overview
This project implements a command-line restaurant ordering system using object-oriented programming principles.

The system supports:
- Menu management
- Combo items
- Order lifecycle management
- Inventory control
- Pricing with tax, discounts, and tips
- Receipt generation

## Class Design

MenuItem
├── FoodItem
├── DrinkItem
└── Combo

Discount
├── PercentageDiscount
└── FixedAmountDiscount

Order
└── OrderItem

Inventory

## Pricing Logic

Subtotal = sum(item price × quantity)

Discounts are applied sequentially.

Tax is calculated per category.

Tip = percentage of (subtotal − discounts + tax)

Final Total = subtotal − discounts + tax + tip

## Test Plan

Tested the following:

- Menu creation
- Combo pricing
- Adding/removing items
- Inventory validation
- Order lifecycle transitions
- Receipt accuracy

## Example CLI Run

Create Order
Add Burger ×2
Add Combo ×1
Apply discounts
Confirm order
Change status to Paid
Print receipt

## Limitations

- Only one order handled at a time
- Data not persisted between runs
- Menu editing not supported in CLI

## Possible Improvements

- Persistent database storage
- GUI interface
- Multiple concurrent orders