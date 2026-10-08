import re

file_path = 'frontend/src/pages/HomePage.jsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add state for promotion
if 'const [promotion, setPromotion] = useState(null);' not in content:
    content = content.replace(
        'const [newArrivals, setNewArrivals] = useState([]);',
        'const [newArrivals, setNewArrivals] = useState([]);\n  const [promotion, setPromotion] = useState(null);'
    )

# Add fetch for promotion
fetch_block = '''
    const fetchHomeData = async () => {
      try {
        setLoading(true);
        // Fetch trending
        const trendingRes = await api.get('/products/?ordering=-rating,-num_reviews&limit=4');
        setTrendingProducts(trendingRes.data.results || trendingRes.data);
        
        // Fetch new arrivals
        const newRes = await api.get('/products/?ordering=-created_at&limit=4');
        setNewArrivals(newRes.data.results || newRes.data);

        // Fetch active promotion
        try {
          const promoRes = await api.get('/products/promotions/active/');
          setPromotion(promoRes.data);
        } catch (promoErr) {
          console.log('No active promotion found');
          setPromotion(null);
        }
      } catch (err) {
        console.error('Error fetching home data:', err);
      } finally {
        setLoading(false);
      }
    };
'''

content = re.sub(
    r'const fetchHomeData = async \(\) => \{.*?finally \{\s*setLoading\(false\);\s*\}\s*\};',
    fetch_block.strip(),
    content,
    flags=re.DOTALL
)

# Update Banner
old_banner_regex = r'\{/\*\s*Promo Banner\s*\*/\}.*?</section>'
new_banner = '''{/* Promo Banner */}
      <section className="mx-auto max-w-7xl px-4 py-24 sm:px-6 lg:px-8">
        <div className="relative overflow-hidden rounded-[2.5rem] bg-indigo-600">
          <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1618220179428-22790b46a0eb?q=80&w=2070&auto=format&fit=crop')] bg-cover bg-center mix-blend-overlay opacity-20"></div>
          <div className="relative z-10 p-12 sm:p-20 flex flex-col items-center text-center lg:items-start lg:text-left">
            <span className="mb-4 inline-block rounded-full bg-white/20 px-4 py-1.5 text-xs font-bold tracking-wider text-white backdrop-blur-md">
              {promotion ? promotion.badge : "FEATURED"}
            </span>
            <h2 className="mb-4 text-4xl font-black text-white sm:text-5xl lg:text-6xl">
              {promotion ? promotion.title : "ShopVerse Picks"}
            </h2>
            <p className="mb-8 max-w-xl text-lg text-indigo-100">
              {promotion ? promotion.description : "Discover our curated selection of top-rated tech and gaming gear."}
            </p>
            <Link
              to={promotion ? (promotion.category_slug ? \/products?category=\\ : "/products") : "/products"}
              className="inline-flex items-center justify-center rounded-full bg-white px-8 py-4 text-sm font-bold text-indigo-600 transition hover:bg-indigo-50"
            >
              {promotion ? promotion.button_text : "Explore Collection"}
            </Link>
          </div>
        </div>
      </section>'''

content = re.sub(old_banner_regex, new_banner, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated HomePage.jsx')
