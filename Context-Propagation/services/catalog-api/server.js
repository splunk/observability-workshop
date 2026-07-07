import express from 'express';
import { trace } from '@opentelemetry/api';

const app = express();
const port = Number(process.env.PORT || 3002);
const tracer = trace.getTracer('catalog-api');

const products = [
  {
    id: 'telescope-orion-8',
    name: 'Orion 8" Dobsonian Telescope',
    price: 449.99,
    category: 'Telescopes',
    description: 'Classic light-bucket for deep-sky observing.',
    image: '🔭',
  },
  {
    id: 'eyepiece-plossl-set',
    name: 'Plossl Eyepiece Set (4-piece)',
    price: 129.99,
    category: 'Eyepieces',
    description: 'Multi-coated 52° eyepieces from 6mm to 25mm.',
    image: '👁️',
  },
  {
    id: 'filter-nebula-uhc',
    name: 'UHC Nebula Filter 1.25"',
    price: 89.99,
    category: 'Filters',
    description: 'Enhance emission nebulae from light-polluted skies.',
    image: '🌌',
  },
  {
    id: 'mount-eq6-pro',
    name: 'SkyWatcher EQ6-R Pro Mount',
    price: 1899.0,
    category: 'Mounts',
    description: 'Heavy-duty equatorial mount for astrophotography.',
    image: '⚙️',
  },
  {
    id: 'book-cosmic-cliffs',
    name: 'Cosmic Cliffs Observing Atlas',
    price: 34.99,
    category: 'Books',
    description: 'Season-by-season guide to the best deep-sky targets.',
    image: '📖',
  },
  {
    id: 'camera-asi533',
    name: 'ZWO ASI533MC Pro Camera',
    price: 999.0,
    category: 'Cameras',
    description: 'Cooled one-shot color camera for nebula imaging.',
    image: '📷',
  },
];

app.get('/health', (_req, res) => {
  res.json({ status: 'ok', service: 'catalog-api' });
});

app.get('/products', (req, res) => {
  const span = trace.getActiveSpan();
  span?.setAttribute('catalog.product_count', products.length);

  tracer.startActiveSpan('catalog.list_products', (listSpan) => {
    try {
      const category = req.query.category;
      const results = category
        ? products.filter((p) => p.category.toLowerCase() === String(category).toLowerCase())
        : products;

      listSpan.setAttribute('catalog.filtered_count', results.length);
      res.json({ products: results });
    } finally {
      listSpan.end();
    }
  });
});

app.get('/products/:id', (req, res) => {
  tracer.startActiveSpan('catalog.get_product', (span) => {
    try {
      const product = products.find((p) => p.id === req.params.id);
      span.setAttribute('catalog.product_id', req.params.id);

      if (!product) {
        span.setAttribute('http.status_code', 404);
        res.status(404).json({ error: 'Product not found' });
        return;
      }

      res.json({ product });
    } finally {
      span.end();
    }
  });
});

app.listen(port, () => {
  console.log(`catalog-api listening on port ${port}`);
});
