from app.product_loader import product_loader

# Fetch product details for productId 1
product_1 = product_loader.get_product(1)
print("Product 1:", product_1)

# Fetch product details for productId 5
product_5 = product_loader.get_product(5)
print("Product 5:", product_5)

# Fetch product details for productId 10
product_10 = product_loader.get_product(10)
print("Product 10:", product_10)
