from flask import Flask, render_template_string
import os

app = Flask(__name__)

# Sample product data
PRODUCTS = [
    {
        'id': 1,
        'name': 'Wireless AirPods Pro',
        'price': 249.99,
        'original_price': 299.99,
        'image': 'https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?w=500&h=500&fit=crop',
        'category': 'Electronics',
        'rating': 4.8,
        'reviews': 1250,
        'description': 'Premium wireless earbuds with active noise cancellation and spatial audio.',
        'features': ['Active Noise Cancellation', 'Spatial Audio', '6 Hour Battery', 'Water Resistant']
    },
    {
        'id': 2,
        'name': 'Smart Watch Series X',
        'price': 399.99,
        'original_price': 449.99,
        'image': 'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=500&h=500&fit=crop',
        'category': 'Wearables',
        'rating': 4.9,
        'reviews': 2100,
        'description': 'Advanced smartwatch with health monitoring and GPS tracking.',
        'features': ['Health Monitoring', 'GPS Tracking', '7 Day Battery', 'Water Proof']
    },
    {
        'id': 3,
        'name': 'Premium Coffee Maker',
        'price': 189.99,
        'original_price': 229.99,
        'image': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=500&h=500&fit=crop',
        'category': 'Home & Kitchen',
        'rating': 4.7,
        'reviews': 850,
        'description': 'Professional-grade coffee maker with built-in grinder and programmable settings.',
        'features': ['Built-in Grinder', 'Programmable', 'Thermal Carafe', '12 Cup Capacity']
    },
    {
        'id': 4,
        'name': 'Gaming Mechanical Keyboard',
        'price': 159.99,
        'original_price': 199.99,
        'image': 'https://images.unsplash.com/photo-1541140532154-b024d705b90a?w=500&h=500&fit=crop',
        'category': 'Gaming',
        'rating': 4.6,
        'reviews': 1500,
        'description': 'RGB backlit mechanical keyboard with customizable keys and macro support.',
        'features': ['RGB Backlit', 'Mechanical Switches', 'Macro Support', 'Wired/Wireless']
    },
    {
        'id': 5,
        'name': 'Wireless Charging Pad',
        'price': 49.99,
        'original_price': 69.99,
        'image': 'https://images.unsplash.com/photo-1593642702909-dec73df255d7?w=500&h=500&fit=crop',
        'category': 'Accessories',
        'rating': 4.5,
        'reviews': 650,
        'description': 'Fast wireless charging pad compatible with all Qi-enabled devices.',
        'features': ['Fast Charging', 'Qi Compatible', 'LED Indicator', 'Non-slip Surface']
    },
    {
        'id': 6,
        'name': 'Bluetooth Speaker',
        'price': 79.99,
        'original_price': 99.99,
        'image': 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=500&h=500&fit=crop',
        'category': 'Audio',
        'rating': 4.4,
        'reviews': 900,
        'description': 'Portable Bluetooth speaker with 360-degree sound and long battery life.',
        'features': ['360° Sound', '20 Hour Battery', 'Water Resistant', 'Voice Assistant']
    }
]

CATEGORIES = ['All', 'Electronics', 'Wearables', 'Home & Kitchen', 'Gaming', 'Accessories', 'Audio']

# Base template
BASE_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}ModernShop - Premium E-commerce{% endblock %}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        primary: '#6366f1',
                        secondary: '#f59e0b',
                    }
                }
            }
        }
    </script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        body { font-family: 'Inter', sans-serif; }
        .glass { backdrop-filter: blur(10px); background: rgba(255, 255, 255, 0.1); }
        .gradient-bg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .card-hover { transition: all 0.3s ease; }
        .card-hover:hover { transform: translateY(-8px); box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); }
        .animate-float { animation: float 3s ease-in-out infinite; }
        @keyframes float { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-10px); } }
    </style>
</head>
<body class="bg-gray-50 min-h-screen">
    <!-- Navigation -->
    <nav class="bg-white/80 backdrop-blur-md shadow-lg sticky top-0 z-50 border-b border-gray-100">
        <div class="container mx-auto px-4">
            <div class="flex justify-between items-center py-4">
                <div class="flex items-center space-x-8">
                    <a href="/" class="text-2xl font-bold bg-gradient-to-r from-primary to-purple-600 bg-clip-text text-transparent">
                        <i class="fas fa-store mr-2"></i>ModernShop
                    </a>
                    <div class="hidden md:flex space-x-6">
                        <a href="/" class="text-gray-700 hover:text-primary transition-colors font-medium">Home</a>
                        <a href="/products" class="text-gray-700 hover:text-primary transition-colors font-medium">Products</a>
                        <a href="/categories" class="text-gray-700 hover:text-primary transition-colors font-medium">Categories</a>
                        <a href="/about" class="text-gray-700 hover:text-primary transition-colors font-medium">About</a>
                        <a href="/contact" class="text-gray-700 hover:text-primary transition-colors font-medium">Contact</a>
                    </div>
                </div>
                <div class="flex items-center space-x-4">
                    <div class="relative hidden md:block">
                        <input type="text" placeholder="Search products..." 
                               class="pl-10 pr-4 py-2 bg-gray-100 rounded-full focus:outline-none focus:ring-2 focus:ring-primary focus:bg-white transition-all">
                        <i class="fas fa-search absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
                    </div>
                    <a href="/cart" class="relative p-2 text-gray-700 hover:text-primary transition-colors">
                        <i class="fas fa-shopping-cart text-xl"></i>
                        <span class="absolute -top-1 -right-1 bg-primary text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">3</span>
                    </a>
                    <a href="/account" class="p-2 text-gray-700 hover:text-primary transition-colors">
                        <i class="fas fa-user text-xl"></i>
                    </a>
                    <button class="md:hidden p-2 text-gray-700">
                        <i class="fas fa-bars text-xl"></i>
                    </button>
                </div>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main>
        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    <footer class="bg-gray-900 text-white py-12 mt-16">
        <div class="container mx-auto px-4">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
                <div>
                    <h3 class="text-xl font-bold mb-4 bg-gradient-to-r from-primary to-purple-400 bg-clip-text text-transparent">ModernShop</h3>
                    <p class="text-gray-400 mb-4">Premium e-commerce experience with the latest products and exceptional customer service.</p>
                    <div class="flex space-x-4">
                        <a href="#" class="text-gray-400 hover:text-primary transition-colors"><i class="fab fa-facebook-f"></i></a>
                        <a href="#" class="text-gray-400 hover:text-primary transition-colors"><i class="fab fa-twitter"></i></a>
                        <a href="#" class="text-gray-400 hover:text-primary transition-colors"><i class="fab fa-instagram"></i></a>
                        <a href="#" class="text-gray-400 hover:text-primary transition-colors"><i class="fab fa-linkedin-in"></i></a>
                    </div>
                </div>
                <div>
                    <h4 class="font-semibold mb-4">Quick Links</h4>
                    <ul class="space-y-2">
                        <li><a href="/" class="text-gray-400 hover:text-white transition-colors">Home</a></li>
                        <li><a href="/products" class="text-gray-400 hover:text-white transition-colors">Products</a></li>
                        <li><a href="/categories" class="text-gray-400 hover:text-white transition-colors">Categories</a></li>
                        <li><a href="/about" class="text-gray-400 hover:text-white transition-colors">About Us</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="font-semibold mb-4">Customer Service</h4>
                    <ul class="space-y-2">
                        <li><a href="/contact" class="text-gray-400 hover:text-white transition-colors">Contact Us</a></li>
                        <li><a href="#" class="text-gray-400 hover:text-white transition-colors">Shipping Info</a></li>
                        <li><a href="#" class="text-gray-400 hover:text-white transition-colors">Returns</a></li>
                        <li><a href="#" class="text-gray-400 hover:text-white transition-colors">Size Guide</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="font-semibold mb-4">Newsletter</h4>
                    <p class="text-gray-400 mb-4">Subscribe for updates and exclusive offers</p>
                    <div class="flex">
                        <input type="email" placeholder="Your email" 
                               class="flex-1 px-4 py-2 bg-gray-800 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-primary">
                        <button class="bg-primary px-6 py-2 rounded-r-lg hover:bg-primary/90 transition-colors">
                            <i class="fas fa-paper-plane"></i>
                        </button>
                    </div>
                </div>
            </div>
            <div class="border-t border-gray-800 mt-8 pt-8 text-center">
                <p class="text-gray-400">&copy; 2024 ModernShop. All rights reserved. | Privacy Policy | Terms of Service</p>
            </div>
        </div>
    </footer>

    <script>
        // Simple cart functionality
        let cart = [];
        
        function addToCart(productId, productName, price) {
            cart.push({id: productId, name: productName, price: price});
            updateCartCount();
            showNotification('Added to cart!');
        }
        
        function updateCartCount() {
            const cartCount = document.querySelector('.fa-shopping-cart + span');
            if (cartCount) cartCount.textContent = cart.length;
        }
        
        function showNotification(message) {
            const notification = document.createElement('div');
            notification.className = 'fixed top-20 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50 transform translate-x-full transition-transform';
            notification.textContent = message;
            document.body.appendChild(notification);
            
            setTimeout(() => notification.classList.remove('translate-x-full'), 100);
            setTimeout(() => {
                notification.classList.add('translate-x-full');
                setTimeout(() => notification.remove(), 300);
            }, 2000);
        }
        
        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });
    </script>
</body>
</html>
'''

# Home page template
HOME_TEMPLATE = BASE_TEMPLATE.replace(
    '{% block content %}{% endblock %}', 
    '''
    <!-- Hero Section -->
    <section class="relative gradient-bg text-white py-20 overflow-hidden">
        <div class="absolute inset-0 bg-black/20"></div>
        <div class="container mx-auto px-4 relative z-10">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
                <div class="space-y-6">
                    <h1 class="text-5xl lg:text-6xl font-bold leading-tight">
                        Discover <span class="text-secondary">Premium</span> Products
                    </h1>
                    <p class="text-xl text-white/90 leading-relaxed">
                        Explore our curated collection of cutting-edge technology and lifestyle products designed for the modern world.
                    </p>
                    <div class="flex flex-col sm:flex-row gap-4">
                        <a href="/products" class="bg-white text-gray-900 px-8 py-4 rounded-full font-semibold hover:bg-gray-100 transition-colors transform hover:scale-105">
                            Shop Now
                        </a>
                        <a href="#featured" class="border-2 border-white text-white px-8 py-4 rounded-full font-semibold hover:bg-white hover:text-gray-900 transition-colors">
                            View Collection
                        </a>
                    </div>
                </div>
                <div class="relative">
                    <div class="animate-float">
                        <img src="https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=600&h=400&fit=crop" 
                             alt="Premium Products" class="rounded-2xl shadow-2xl">
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Stats Section -->
    <section class="py-12 bg-white">
        <div class="container mx-auto px-4">
            <div class="grid grid-cols-2 lg:grid-cols-4 gap-8">
                <div class="text-center">
                    <div class="text-3xl font-bold text-primary mb-2">10K+</div>
                    <div class="text-gray-600">Happy Customers</div>
                </div>
                <div class="text-center">
                    <div class="text-3xl font-bold text-primary mb-2">500+</div>
                    <div class="text-gray-600">Premium Products</div>
                </div>
                <div class="text-center">
                    <div class="text-3xl font-bold text-primary mb-2">99%</div>
                    <div class="text-gray-600">Satisfaction Rate</div>
                </div>
                <div class="text-center">
                    <div class="text-3xl font-bold text-primary mb-2">24/7</div>
                    <div class="text-gray-600">Customer Support</div>
                </div>
            </div>
        </div>
    </section>

    <!-- Featured Products -->
    <section id="featured" class="py-16 bg-gray-50">
        <div class="container mx-auto px-4">
            <div class="text-center mb-12">
                <h2 class="text-4xl font-bold text-gray-800 mb-4">Featured Products</h2>
                <p class="text-xl text-gray-600">Handpicked items just for you</p>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {% for product in products[:3] %}
                <div class="bg-white rounded-2xl shadow-lg card-hover overflow-hidden">
                    <div class="relative">
                        <img src="{{ product.image }}" alt="{{ product.name }}" class="w-full h-64 object-cover">
                        {% if product.original_price > product.price %}
                        <span class="absolute top-4 left-4 bg-red-500 text-white px-3 py-1 rounded-full text-sm font-semibold">
                            Sale
                        </span>
                        {% endif %}
                        <button class="absolute top-4 right-4 p-2 bg-white/80 rounded-full hover:bg-white transition-colors">
                            <i class="fas fa-heart text-gray-600"></i>
                        </button>
                    </div>
                    <div class="p-6">
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-sm text-primary font-semibold">{{ product.category }}</span>
                            <div class="flex items-center">
                                <i class="fas fa-star text-yellow-400 mr-1"></i>
                                <span class="text-sm text-gray-600">{{ product.rating }} ({{ product.reviews }})</span>
                            </div>
                        </div>
                        <h3 class="text-xl font-bold text-gray-800 mb-2">{{ product.name }}</h3>
                        <p class="text-gray-600 mb-4 line-clamp-2">{{ product.description }}</p>
                        <div class="flex items-center justify-between">
                            <div class="flex items-center space-x-2">
                                <span class="text-2xl font-bold text-primary">${{ "%.2f"|format(product.price) }}</span>
                                {% if product.original_price > product.price %}
                                <span class="text-sm text-gray-500 line-through">${{ "%.2f"|format(product.original_price) }}</span>
                                {% endif %}
                            </div>
                            <button onclick="addToCart({{ product.id }}, '{{ product.name }}', {{ product.price }})" 
                                    class="bg-primary text-white px-6 py-2 rounded-full hover:bg-primary/90 transition-colors transform hover:scale-105">
                                Add to Cart
                            </button>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
            <div class="text-center mt-12">
                <a href="/products" class="bg-primary text-white px-8 py-4 rounded-full font-semibold hover:bg-primary/90 transition-colors transform hover:scale-105">
                    View All Products
                </a>
            </div>
        </div>
    </section>

    <!-- Features Section -->
    <section class="py-16 bg-white">
        <div class="container mx-auto px-4">
            <div class="text-center mb-12">
                <h2 class="text-4xl font-bold text-gray-800 mb-4">Why Choose ModernShop?</h2>
                <p class="text-xl text-gray-600">Experience the difference with our premium service</p>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div class="text-center p-6">
                    <div class="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                        <i class="fas fa-shipping-fast text-2xl text-primary"></i>
                    </div>
                    <h3 class="text-xl font-bold text-gray-800 mb-2">Fast Shipping</h3>
                    <p class="text-gray-600">Free express shipping on orders over $50. Get your products delivered in 1-2 business days.</p>
                </div>
                <div class="text-center p-6">
                    <div class="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                        <i class="fas fa-award text-2xl text-primary"></i>
                    </div>
                    <h3 class="text-xl font-bold text-gray-800 mb-2">Quality Guarantee</h3>
                    <p class="text-gray-600">All products come with our quality guarantee and comprehensive warranty coverage.</p>
                </div>
                <div class="text-center p-6">
                    <div class="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                        <i class="fas fa-headset text-2xl text-primary"></i>
                    </div>
                    <h3 class="text-xl font-bold text-gray-800 mb-2">24/7 Support</h3>
                    <p class="text-gray-600">Our dedicated customer support team is available around the clock to help you.</p>
                </div>
            </div>
        </div>
    </section>
    '''
)

# Products page template
PRODUCTS_TEMPLATE = BASE_TEMPLATE.replace(
    '{% block content %}{% endblock %}',
    '''
    <!-- Page Header -->
    <section class="bg-gradient-to-r from-primary to-purple-600 text-white py-16">
        <div class="container mx-auto px-4">
            <div class="text-center">
                <h1 class="text-4xl lg:text-5xl font-bold mb-4">Our Products</h1>
                <p class="text-xl text-white/90">Discover our complete collection of premium products</p>
            </div>
        </div>
    </section>

    <!-- Filters -->
    <section class="py-8 bg-white border-b">
        <div class="container mx-auto px-4">
            <div class="flex flex-wrap items-center justify-between gap-4">
                <div class="flex flex-wrap gap-2">
                    {% for category in categories %}
                    <button class="px-4 py-2 rounded-full border border-gray-300 hover:border-primary hover:text-primary transition-colors {{ 'bg-primary text-white border-primary' if category == 'All' else '' }}">
                        {{ category }}
                    </button>
                    {% endfor %}
                </div>
                <select class="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary">
                    <option>Sort by: Featured</option>
                    <option>Price: Low to High</option>
                    <option>Price: High to Low</option>
                    <option>Newest First</option>
                    <option>Best Rated</option>
                </select>
            </div>
        </div>
    </section>

    <!-- Products Grid -->
    <section class="py-12">
        <div class="container mx-auto px-4">
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
                {% for product in products %}
                <div class="bg-white rounded-2xl shadow-lg card-hover overflow-hidden">
                    <div class="relative">
                        <img src="{{ product.image }}" alt="{{ product.name }}" class="w-full h-64 object-cover">
                        {% if product.original_price > product.price %}
                        <span class="absolute top-4 left-4 bg-red-500 text-white px-3 py-1 rounded-full text-sm font-semibold">
                            Sale
                        </span>
                        {% endif %}
                        <button class="absolute top-4 right-4 p-2 bg-white/80 rounded-full hover:bg-white transition-colors">
                            <i class="fas fa-heart text-gray-600"></i>
                        </button>
                        <div class="absolute inset-0 bg-black/40 opacity-0 hover:opacity-100 transition-opacity flex items-center justify-center">
                            <a href="/product/{{ product.id }}" class="bg-white text-gray-900 px-6 py-2 rounded-full font-semibold hover:bg-gray-100 transition-colors">
                                Quick View
                            </a>
                        </div>
                    </div>
                    <div class="p-6">
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-sm text-primary font-semibold">{{ product.category }}</span>
                            <div class="flex items-center">
                                <i class="fas fa-star text-yellow-400 mr-1"></i>
                                <span class="text-sm text-gray-600">{{ product.rating }}</span>
                            </div>
                        </div>
                        <h3 class="text-xl font-bold text-gray-800 mb-2">{{ product.name }}</h3>
                        <p class="text-gray-600 mb-4 text-sm line-clamp-2">{{ product.description }}</p>
                        <div class="flex items-center justify-between">
                            <div class="flex items-center space-x-2">
                                <span class="text-xl font-bold text-primary">${{ "%.2f"|format(product.price) }}</span>
                                {% if product.original_price > product.price %}
                                <span class="text-sm text-gray-500 line-through">${{ "%.2f"|format(product.original_price) }}</span>
                                {% endif %}
                            </div>
                            <button onclick="addToCart({{ product.id }}, '{{ product.name }}', {{ product.price }})" 
                                    class="bg-primary text-white px-4 py-2 rounded-full hover:bg-primary/90 transition-colors transform hover:scale-105">
                                <i class="fas fa-cart-plus mr-1"></i> Add
                            </button>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </section>
    '''
)

# Product detail template
PRODUCT_DETAIL_TEMPLATE = BASE_TEMPLATE.replace(
    '{% block content %}{% endblock %}',
    '''
    <!-- Product Detail -->
    <section class="py-12">
        <div class="container mx-auto px-4">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
                <!-- Product Images -->
                <div class="space-y-4">
                    <div class="relative">
                        <img src="{{ product.image }}" alt="{{ product.name }}" 
                             class="w-full h-96 object-cover rounded-2xl shadow-lg">
                        {% if product.original_price > product.price %}
                        <span class="absolute top-4 left-4 bg-red-500 text-white px-4 py-2 rounded-full font-semibold">
                            {{ ((product.original_price - product.price) / product.original_price * 100)|round|int }}% OFF
                        </span>
                        {% endif %}
                    </div>
                    <div class="grid grid-cols-4 gap-4">
                        {% for i in range(4) %}
                        <img src="{{ product.image }}" alt="{{ product.name }}" 
                             class="w-full h-24 object-cover rounded-lg shadow-md cursor-pointer opacity-60 hover:opacity-100 transition-opacity">
                        {% endfor %}
                    </div>
                </div>

                <!-- Product Info -->
                <div class="space-y-6">
                    <div>
                        <span class="text-primary font-semibold text-sm uppercase tracking-wide">{{ product.category }}</span>
                        <h1 class="text-3xl lg:text-4xl font-bold text-gray-900 mt-2">{{ product.name }}</h1>
                        <div class="flex items-center mt-4 space-x-4">
                            <div class="flex items-center">
                                {% for i in range(5) %}
                                <i class="fas fa-star {{ 'text-yellow-400' if i < product.rating else 'text-gray-300' }}"></i>
                                {% endfor %}
                                <span class="ml-2 text-gray-600">{{ product.rating }} ({{ product.reviews }} reviews)</span>
                            </div>
                        </div>
                    </div>

                    <div class="flex items-center space-x-4">
                        <span class="text-4xl font-bold text-primary">${{ "%.2f"|format(product.price) }}</span>
                        {% if product.original_price > product.price %}
                        <span class="text-2xl text-gray-500 line-through">${{ "%.2f"|format(product.original_price) }}</span>
                        <span class="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-semibold">
                            Save ${{ "%.2f"|format(product.original_price - product.price) }}
                        </span>
                        {% endif %}
                    </div>

                    <div>
                        <h3 class="font-semibold text-gray-900 mb-3">Description</h3>
                        <p class="text-gray-600 leading-relaxed">{{ product.description }}</p>
                    </div>

                    <div>
                        <h3 class="font-semibold text-gray-900 mb-3">Key Features</h3>
                        <ul class="grid grid-cols-2 gap-2">
                            {% for feature in product.features %}
                            <li class="flex items-center text-gray-600">
                                <i class="fas fa-check text-green-500 mr-2"></i>
                                {{ feature }}
                            </li>
                            {% endfor %}
                        </ul>
                    </div>

                    <div class="space-y-4">
                        <div class="flex items-center space-x-4">
                            <label class="font-semibold text-gray-900">Quantity:</label>
                            <div class="flex items-center border border-gray-300 rounded-lg">
                                <button class="px-3 py-2 hover:bg-gray-100 transition-colors">-</button>
                                <input type="number" value="1" min="1" class="w-16 text-center border-none focus:outline-none">
                                <button class="px-3 py-2 hover:bg-gray-100 transition-colors">+</button>
                            </div>
                        </div>
                        
                        <div class="flex flex-col sm:flex-row gap-4">
                            <button onclick="addToCart({{ product.id }}, '{{ product.name }}', {{ product.price }})" 
                                    class="flex-1 bg-primary text-white py-4 rounded-full font-semibold hover:bg-primary/90 transition-colors transform hover:scale-105">
                                <i class="fas fa-cart-plus mr-2"></i>
                                Add to Cart
                            </button>
                            <button class="px-8 py-4 border-2 border-primary text-primary rounded-full font-semibold hover:bg-primary hover:text-white transition-colors">
                                <i class="fas fa-heart mr-2"></i>
                                Wishlist
                            </button>
                        </div>
                        
                        <button class="w-full bg-secondary text-white py-4 rounded-full font-semibold hover:bg-secondary/90 transition-colors">
                            <i class="fas fa-bolt mr-2"></i>
                            Buy Now
                        </button>
                    </div>

                    <div class="border-t pt-6 space-y-3">
                        <div class="flex items-center text-gray-600">
                            <i class="fas fa-truck mr-3 text-primary"></i>
                            <span>Free shipping on orders over $50</span>
                        </div>
                        <div class="flex items-center text-gray-600">
                            <i class="fas fa-undo mr-3 text-primary"></i>
                            <span>30-day return policy</span>
                        </div>
                        <div class="flex items-center text-gray-600">
                            <i class="fas fa-shield-alt mr-3 text-primary"></i>
                            <span>2-year warranty included</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Related Products -->
    <section class="py-16 bg-gray-50">
        <div class="container mx-auto px-4">
            <h2 class="text-3xl font-bold text-gray-900 mb-8 text-center">Related Products</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                {% for related_product in related_products %}
                <div class="bg-white rounded-2xl shadow-lg card-hover overflow-hidden">
                    <div class="relative">
                        <img src="{{ related_product.image }}" alt="{{ related_product.name }}" class="w-full h-48 object-cover">
                        <button class="absolute top-4 right-4 p-2 bg-white/80 rounded-full hover:bg-white transition-colors">
                            <i class="fas fa-heart text-gray-600"></i>
                        </button>
                    </div>
                    <div class="p-4">
                        <h3 class="font-bold text-gray-800 mb-2">{{ related_product.name }}</h3>
                        <div class="flex items-center justify-between">
                            <span class="text-lg font-bold text-primary">${{ "%.2f"|format(related_product.price) }}</span>
                            <button onclick="addToCart({{ related_product.id }}, '{{ related_product.name }}', {{ related_product.price }})" 
                                    class="bg-primary text-white px-4 py-2 rounded-full hover:bg-primary/90 transition-colors">
                                <i class="fas fa-plus"></i>
                            </button>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </section>
    '''
)

# Cart page template
CART_TEMPLATE = BASE_TEMPLATE.replace(
    '{% block content %}{% endblock %}',
    '''
    <!-- Cart Page -->
    <section class="py-12">
        <div class="container mx-auto px-4">
            <h1 class="text-3xl font-bold text-gray-900 mb-8">Shopping Cart</h1>
            
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <!-- Cart Items -->
                <div class="lg:col-span-2 space-y-4">
                    {% for i in range(3) %}
                    <div class="bg-white rounded-2xl shadow-lg p-6">
                        <div class="flex items-center space-x-4">
                            <img src="{{ products[i].image }}" alt="{{ products[i].name }}" 
                                 class="w-20 h-20 object-cover rounded-lg">
                            <div class="flex-1">
                                <h3 class="font-bold text-gray-900">{{ products[i].name }}</h3>
                                <p class="text-gray-600 text-sm">{{ products[i].category }}</p>
                                <div class="flex items-center mt-2">
                                    <span class="text-primary font-bold">${{ "%.2f"|format(products[i].price) }}</span>
                                </div>
                            </div>
                            <div class="flex items-center space-x-3">
                                <div class="flex items-center border border-gray-300 rounded-lg">
                                    <button class="px-3 py-1 hover:bg-gray-100 transition-colors">-</button>
                                    <input type="number" value="1" min="1" class="w-12 text-center border-none focus:outline-none">
                                    <button class="px-3 py-1 hover:bg-gray-100 transition-colors">+</button>
                                </div>
                                <button class="p-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors">
                                    <i class="fas fa-trash"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>

                <!-- Order Summary -->
                <div class="bg-white rounded-2xl shadow-lg p-6 h-fit">
                    <h2 class="text-xl font-bold text-gray-900 mb-6">Order Summary</h2>
                    <div class="space-y-4">
                        <div class="flex justify-between">
                            <span class="text-gray-600">Subtotal (3 items)</span>
                            <span class="font-semibold">$639.97</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600">Shipping</span>
                            <span class="text-green-600 font-semibold">Free</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600">Tax</span>
                            <span class="font-semibold">$51.20</span>
                        </div>
                        <hr class="my-4">
                        <div class="flex justify-between text-lg font-bold">
                            <span>Total</span>
                            <span class="text-primary">$691.17</span>
                        </div>
                    </div>
                    
                    <div class="mt-6 space-y-3">
                        <input type="text" placeholder="Promo code" 
                               class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary">
                        <button class="w-full bg-primary text-white py-4 rounded-full font-semibold hover:bg-primary/90 transition-colors">
                            Proceed to Checkout
                        </button>
                        <a href="/products" class="block w-full text-center text-primary font-semibold py-2 hover:underline">
                            Continue Shopping
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </section>
    '''
)

# Routes
@app.route('/')
def home():
    return render_template_string(HOME_TEMPLATE, products=PRODUCTS[:3])

@app.route('/products')
def products():
    return render_template_string(PRODUCTS_TEMPLATE, products=PRODUCTS, categories=CATEGORIES)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        return "Product not found", 404
    
    # Get related products (same category, excluding current product)
    related_products = [p for p in PRODUCTS if p['category'] == product['category'] and p['id'] != product_id][:4]
    
    return render_template_string(PRODUCT_DETAIL_TEMPLATE, product=product, related_products=related_products)

@app.route('/cart')
def cart():
    return render_template_string(CART_TEMPLATE, products=PRODUCTS)

@app.route('/categories')
def categories():
    return render_template_string('''
    {% extends "base.html" %}
    {% block content %}
    <section class="py-12">
        <div class="container mx-auto px-4">
            <h1 class="text-3xl font-bold text-gray-900 mb-8 text-center">Shop by Category</h1>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {% for category in categories[1:] %}
                <div class="bg-gradient-to-br from-primary to-purple-600 rounded-2xl shadow-lg overflow-hidden card-hover">
                    <div class="p-8 text-white text-center">
                        <i class="fas fa-laptop text-4xl mb-4"></i>
                        <h3 class="text-2xl font-bold mb-2">{{ category }}</h3>
                        <p class="text-white/80 mb-4">Discover premium {{ category.lower() }} products</p>
                        <a href="/products?category={{ category }}" 
                           class="inline-block bg-white text-primary px-6 py-3 rounded-full font-semibold hover:bg-gray-100 transition-colors">
                            Shop Now
                        </a>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </section>
    {% endblock %}
    ''', categories=CATEGORIES)

@app.route('/about')
def about():
    return render_template_string('''
    {% extends "base.html" %}
    {% block content %}
    <section class="py-16 bg-gradient-to-r from-primary to-purple-600 text-white">
        <div class="container mx-auto px-4 text-center">
            <h1 class="text-4xl lg:text-5xl font-bold mb-6">About ModernShop</h1>
            <p class="text-xl text-white/90 max-w-3xl mx-auto">
                We're passionate about bringing you the latest in technology and lifestyle products with exceptional quality and service.
            </p>
        </div>
    </section>
    
    <section class="py-16">
        <div class="container mx-auto px-4">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
                <div>
                    <h2 class="text-3xl font-bold text-gray-900 mb-6">Our Story</h2>
                    <p class="text-gray-600 mb-4">
                        Founded in 2020, ModernShop started with a simple mission: to make premium technology and lifestyle products accessible to everyone. We believe that quality shouldn't be compromised, and customer satisfaction should always come first.
                    </p>
                    <p class="text-gray-600 mb-6">
                        Today, we serve thousands of satisfied customers worldwide, offering a curated selection of products from the best brands in the industry.
                    </p>
                    <div class="grid grid-cols-2 gap-4">
                        <div class="text-center">
                            <div class="text-2xl font-bold text-primary">10K+</div>
                            <div class="text-gray-600">Happy Customers</div>
                        </div>
                        <div class="text-center">
                            <div class="text-2xl font-bold text-primary">500+</div>
                            <div class="text-gray-600">Products</div>
                        </div>
                    </div>
                </div>
                <div>
                    <img src="https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=600&h=400&fit=crop" 
                         alt="Our Team" class="rounded-2xl shadow-lg">
                </div>
            </div>
        </div>
    </section>
    {% endblock %}
    ''')

@app.route('/contact')
def contact():
    return render_template_string('''
    {% extends "base.html" %}
    {% block content %}
    <section class="py-16">
        <div class="container mx-auto px-4">
            <div class="max-w-4xl mx-auto">
                <div class="text-center mb-12">
                    <h1 class="text-4xl font-bold text-gray-900 mb-4">Contact Us</h1>
                    <p class="text-xl text-gray-600">We'd love to hear from you. Send us a message and we'll respond as soon as possible.</p>
                </div>
                
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
                    <div>
                        <h2 class="text-2xl font-bold text-gray-900 mb-6">Get in Touch</h2>
                        <div class="space-y-6">
                            <div class="flex items-center">
                                <div class="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mr-4">
                                    <i class="fas fa-map-marker-alt text-primary"></i>
                                </div>
                                <div>
                                    <h3 class="font-semibold text-gray-900">Address</h3>
                                    <p class="text-gray-600">123 Commerce Street, Tech City, TC 12345</p>
                                </div>
                            </div>
                            <div class="flex items-center">
                                <div class="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mr-4">
                                    <i class="fas fa-phone text-primary"></i>
                                </div>
                                <div>
                                    <h3 class="font-semibold text-gray-900">Phone</h3>
                                    <p class="text-gray-600">+1 (555) 123-4567</p>
                                </div>
                            </div>
                            <div class="flex items-center">
                                <div class="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mr-4">
                                    <i class="fas fa-envelope text-primary"></i>
                                </div>
                                <div>
                                    <h3 class="font-semibold text-gray-900">Email</h3>
                                    <p class="text-gray-600">support@modernshop.com</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="bg-white rounded-2xl shadow-lg p-8">
                        <form class="space-y-6">
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <input type="text" placeholder="First Name" 
                                       class="px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary">
                                <input type="text" placeholder="Last Name" 
                                       class="px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary">
                            </div>
                            <input type="email" placeholder="Email Address" 
                                   class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary">
                            <input type="text" placeholder="Subject" 
                                   class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary">
                            <textarea placeholder="Your Message" rows="4" 
                                      class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary resize-none"></textarea>
                            <button type="submit" 
                                    class="w-full bg-primary text-white py-3 rounded-lg font-semibold hover:bg-primary/90 transition-colors">
                                Send Message
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </section>
    {% endblock %}
    ''')

if __name__ == '__main__':
    app.run(debug=True)
