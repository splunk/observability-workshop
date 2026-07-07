import { useEffect, useState } from 'react';
import { startPurchaseWorkflow } from './workflows';

const apiBase = import.meta.env.VITE_API_BASE || '';

export default function App() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState(null);
  const [email, setEmail] = useState('observer@cosmic.shop');
  const [status, setStatus] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetch(`${apiBase}/api/catalog`)
      .then((res) => res.json())
      .then((data) => {
        setProducts(data.products ?? []);
        setLoading(false);
      })
      .catch(() => {
        setStatus({ type: 'error', message: 'Unable to load catalog. Is the stack running?' });
        setLoading(false);
      });
  }, []);

  async function completePurchase(product) {
    setSubmitting(true);
    setStatus(null);

    const workflowSpan = startPurchaseWorkflow(product);

    try {
      const response = await fetch(`${apiBase}/api/purchases`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          productId: product.id,
          quantity: 1,
          customerEmail: email,
        }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Purchase failed');
      }

      workflowSpan.setAttribute('purchase.order_id', data.order?.orderId ?? '');
      workflowSpan.setAttribute('purchase.payment_id', data.payment?.paymentId ?? '');

      setStatus({
        type: 'success',
        message: `Purchase complete! Order ${data.order.orderId} |payment ${data.payment.paymentId} | Your order ships in 3 days`,
        order: data.order,
        payment: data.payment,
      });
      setSelected(null);
    } catch (error) {
      if (typeof workflowSpan.recordException === 'function') {
        workflowSpan.recordException(error);
      }
      setStatus({ type: 'error', message: error.message });
    } finally {
      workflowSpan.end();
      setSubmitting(false);
    }
  }

  return (
    <div className="page">
      <header className="hero">
        <div className="hero__glow" />
        <p className="eyebrow">Splunk OTel Workshop</p>
        <h1>Cosmic Observatory Shop</h1>
        <p className="subtitle">
          Browse our deluctable selection of telescopes, eyepieces, and astrophotography gear. We have the best telescopes to see the world closer.
        </p>
      </header>

      <section className="panel">
        <h2>Your observer details</h2>
        <label>
          Email for order confirmation
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@example.com"
          />
        </label>
      </section>

      {status && (
        <div className={`alert alert--${status.type}`}>
          <strong>{status.type === 'success' ? 'Purchase complete' : 'Something went wrong'}</strong>
          <p>{status.message}</p>
          {status.order && (
            <pre>{JSON.stringify({ order: status.order, payment: status.payment }, null, 2)}</pre>
          )}
        </div>
      )}

      <section className="catalog">
        <div className="catalog__header">
          <h2>Featured equipment</h2>
          <span>{products.length} items</span>
        </div>

        {loading ? (
          <p className="loading">Aligning the catalog…</p>
        ) : (
          <div className="grid">
            {products.map((product) => (
              <article key={product.id} className="card">
                <div className="card__icon">{product.image}</div>
                <p className="card__category">{product.category}</p>
                <h3>{product.name}</h3>
                <p>{product.description}</p>
                <div className="card__footer">
                  <strong>${product.price.toFixed(2)}</strong>
                  <button type="button" onClick={() => setSelected(product)}>
                    Purchase
                  </button>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>

      {selected && (
        <div className="modal-backdrop" role="presentation" onClick={() => setSelected(null)}>
          <div className="modal" role="dialog" aria-modal="true" onClick={(e) => e.stopPropagation()}>
            <h3>Confirm purchase</h3>
            <p>
              You are ordering <strong>{selected.name}</strong> for{' '}
              <strong>${selected.price.toFixed(2)}</strong>.
            </p>
            <p className="hint">
              Clicking <strong>Purchase</strong> only opens this dialog.
              <strong> Place order</strong> to complete the transaction.
            </p>
            <div className="modal__actions">
              <button type="button" className="secondary" onClick={() => setSelected(null)}>
                Cancel
              </button>
              <button type="button" disabled={submitting} onClick={() => completePurchase(selected)}>
                {submitting ? 'Processing…' : 'Place order'}
              </button>
            </div>
          </div>
        </div>
      )}

      <footer>
        <p>
          Workshop demo - This website is hosted for demo purpose only. It is not an actual shop.
        </p>
      </footer>
    </div>
  );
}
