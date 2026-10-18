'use client'

import { useState } from 'react';
import { Copy, Check, ExternalLink, Activity } from 'lucide-react';
import Link from 'next/link';
import styles from './page.module.css';

export default function Home() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [copied, setCopied] = useState(false);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  const handleCopy = () => {
    if (!result) return;
    navigator.clipboard.writeText(`${API_URL}/r/${result.short_code}`);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleShorten = async (e) => {
    e.preventDefault();
    if (!url) return;
    
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const res = await fetch(`${API_URL}/api/shorten`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      });
      
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Failed to shorten URL');
      
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className={styles.container}>
      <div className={styles.hero}>
        <h1 className={styles.title}>ShortX</h1>
        <p className={styles.subtitle}>
          The lightning-fast, secure, and analytics-driven URL shortener.
        </p>
        <Link href="/dashboard" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.5rem', color: 'var(--primary)', marginTop: '1.5rem', textDecoration: 'none', fontWeight: 500, padding: '0.5rem 1rem', background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 'var(--radius)', transition: 'all 0.2s' }}>
          <Activity size={18} />
          View Global Analytics
        </Link>
      </div>

      <div className={`glass-panel ${styles.formContainer}`}>
        <form onSubmit={handleShorten}>
          <div className={styles.inputGroup}>
            <input
              type="url"
              className={styles.input}
              placeholder="Paste your long URL here..."
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              required
            />
            <button type="submit" className={styles.button} disabled={loading}>
              {loading ? 'Shortening...' : 'Shorten'}
            </button>
          </div>
        </form>
        
        {error && <p style={{ color: 'var(--danger)', marginTop: '1rem' }}>{error}</p>}

        {result && (
          <div className={styles.resultCard}>
            <div className={styles.resultHeader}>
              <a 
                href={`${API_URL}/r/${result.short_code}`} 
                target="_blank" 
                rel="noopener noreferrer" 
                className={styles.shortLink}
              >
                shrt.x/{result.short_code}
              </a>
              <span className={`${styles.statusBadge} ${result.status === 'safe' ? styles.statusSafe : styles.statusSuspicious}`}>
                {result.status}
              </span>
            </div>
            <p className={styles.originalLink}>{result.original_url}</p>
            <div className={styles.actionRow}>
              <button type="button" className={styles.actionBtn} onClick={handleCopy}>
                {copied ? <Check size={18} color="var(--success)"/> : <Copy size={18} />}
                <span>{copied ? 'Copied' : 'Copy'}</span>
              </button>
              <a href={`${API_URL}/r/${result.short_code}`} target="_blank" rel="noopener noreferrer" className={styles.actionBtnText}>
                <ExternalLink size={18} />
                <span>Open</span>
              </a>
            </div>
          </div>
        )}
      </div>

      <footer style={{ marginTop: 'auto', padding: '2rem', textAlign: 'center', color: 'var(--text-muted)' }}>
        <p>Engineered with ⚡️ by <strong>SHUBH</strong></p>
      </footer>
    </main>
  );
}
