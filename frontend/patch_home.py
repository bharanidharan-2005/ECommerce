# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\HomePage.jsx'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

target1 = '''const categories = [
  {
    name: "Fashion",
    image: "https://images.unsplash.com/photo-1441984904996-e0b6ba687e04?q=80&w=2070&auto=format&fit=crop",
    link: "/products?category=Fashion",
    count: "240+ Items"
  },
  {
    name: "Electronics",
    image: "https://images.unsplash.com/photo-1498049794561-7780e7231661?q=80&w=2070&auto=format&fit=crop",
    link: "/products?category=Electronics",
    count: "120+ Items"
  },
  {
    name: "Home",
    image: "https://images.unsplash.com/photo-1616046229478-9901c5536a45?q=80&w=2070&auto=format&fit=crop",
    link: "/products?category=Home",
    count: "180+ Items"
  },
  {
    name: "Gaming",
    image: "https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=2070&auto=format&fit=crop",
    link: "/products?category=Gaming",
    count: "90+ Items"
  }
];'''

new1 = '''const categories = [
  {
    name: "Electronics",
    image: "https://images.unsplash.com/photo-1498049794561-7780e7231661?q=80&w=2070&auto=format&fit=crop",
    link: "/products?category=electronics",
    count: "120+ Items"
  },
  {
    name: "Gaming",
    image: "https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=2070&auto=format&fit=crop",
    link: "/products?category=gaming",
    count: "90+ Items"
  },
  {
    name: "Audio",
    image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?q=80&w=2070&auto=format&fit=crop",
    link: "/products?category=audio",
    count: "45+ Items"
  },
  {
    name: "Smart Devices",
    image: "https://images.unsplash.com/photo-1558089687-f282ffcbc126?q=80&w=2070&auto=format&fit=crop",
    link: "/products?category=smart-devices",
    count: "60+ Items"
  }
];'''

target2 = '''<span className="mb-4 inline-block rounded-full bg-indigo-500/10 px-4 py-1.5 text-xs font-bold tracking-wider text-indigo-400 border border-indigo-500/20">
              NEW SEASON • NEW DROPS
            </span>
            <h1 className="mb-6 text-5xl font-black tracking-tight text-white sm:text-7xl lg:text-8xl">
              Everyday essentials,<br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">elevated.</span>
            </h1>
            <p className="mx-auto mb-10 max-w-2xl text-lg text-slate-400 sm:text-xl">
              Discover our curated collection of premium products designed for modern living.
              Uncompromising quality meets exceptional design.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/products"
                className="inline-flex items-center justify-center gap-2 rounded-full bg-indigo-600 px-8 py-4 text-sm font-bold text-white transition-all hover:bg-indigo-500 hover:shadow-lg hover:shadow-indigo-500/25"
              >
                Shop Collection <FiArrowRight />
              </Link>
              <Link
                to="/products?category=all"
                className="inline-flex items-center justify-center gap-2 rounded-full bg-slate-800 px-8 py-4 text-sm font-bold text-white transition-all hover:bg-slate-700 border border-slate-700"
              >
                Explore Categories
              </Link>
            </div>'''

new2 = '''<span className="mb-4 inline-block rounded-full bg-indigo-500/10 px-4 py-1.5 text-xs font-bold tracking-wider text-indigo-400 border border-indigo-500/20">
              PREMIUM TECHNOLOGY
            </span>
            <h1 className="mb-6 text-5xl font-black tracking-tight text-white sm:text-7xl lg:text-8xl">
              Upgrade Your<br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">Setup.</span>
            </h1>
            <p className="mx-auto mb-10 max-w-2xl text-lg text-slate-400 sm:text-xl">
              Discover gaming gear, electronics and smart technology built for everyday performance.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/products?category=electronics"
                className="inline-flex items-center justify-center gap-2 rounded-full bg-indigo-600 px-8 py-4 text-sm font-bold text-white transition-all hover:bg-indigo-500 hover:shadow-lg hover:shadow-indigo-500/25"
              >
                Shop Electronics <FiArrowRight />
              </Link>
              <Link
                to="/products?category=gaming"
                className="inline-flex items-center justify-center gap-2 rounded-full bg-slate-800 px-8 py-4 text-sm font-bold text-white transition-all hover:bg-slate-700 border border-slate-700"
              >
                Explore Gaming
              </Link>
            </div>'''

target3 = 'desc: "On all orders over "'
new3 = 'desc: "On qualifying orders"'

content = content.replace(target1, new1)
content = content.replace(target2, new2)
content = content.replace(target3, new3)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('Patched HomePage successfully.')
