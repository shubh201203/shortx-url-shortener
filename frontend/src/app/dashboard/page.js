'use client'

import { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import { Activity, Link as LinkIcon, ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import styles from './dashboard.module.css';

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await fetch(`${API_URL}/api/analytics/summary`);
        if (!res.ok) throw new Error('Failed to fetch analytics');
        const json = await res.json();
        setData(json);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  if (loading) return <div className={styles.container}>Loading dashboard...</div>;
  if (error) return <div className={styles.container}>Error: {error}</div>;

  return (
    <main className={styles.container}>
      <div style={{ marginBottom: '2rem' }}>
        <Link href="/" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-muted)', textDecoration: 'none', fontWeight: 500 }}>
          <ArrowLeft size={18} />
          Back to Home
        </Link>
      </div>
      <header className={styles.header}>
        <h1 className={styles.title}>Analytics Overview</h1>
        <p className={styles.subtitle}>Track your shortened link performance globally.</p>
      </header>

      <section className={styles.metricsGrid}>
        <div className={`glass-panel ${styles.metricCard}`}>
          <span className={styles.metricTitle}>Total Clicks</span>
          <span className={styles.metricValue}>
            {data?.global_clicks || 0}
          </span>
        </div>
        <div className={`glass-panel ${styles.metricCard}`}>
          <span className={styles.metricTitle}>Total Links</span>
          <span className={styles.metricValue}>
            {data?.total_links || 0}
          </span>
        </div>
        <div className={`glass-panel ${styles.metricCard}`}>
          <span className={styles.metricTitle}>Active Users</span>
          <span className={styles.metricValue} style={{color: 'var(--secondary)'}}>
            N/A
          </span>
        </div>
      </section>

      <section className={`glass-panel ${styles.chartSection}`}>
        <h2 className={styles.sectionTitle}>
          <Activity size={24} style={{ display: 'inline', marginRight: '8px', verticalAlign: 'middle' }} />
          Click Activity (7 Days)
        </h2>
        <div style={{ width: '100%', height: 300 }}>
          <ResponsiveContainer>
            <LineChart data={data?.chart_data || []}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis dataKey="name" stroke="var(--text-muted)" />
              <YAxis stroke="var(--text-muted)" />
              <Tooltip 
                contentStyle={{ backgroundColor: 'var(--background)', border: '1px solid var(--border)' }}
                itemStyle={{ color: 'var(--primary)' }}
              />
              <Line type="monotone" dataKey="clicks" stroke="var(--primary)" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 8 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </section>

      <section className={`glass-panel ${styles.tableSection}`}>
        <h2 className={styles.sectionTitle}>
          <LinkIcon size={24} style={{ display: 'inline', marginRight: '8px', verticalAlign: 'middle' }} />
          Top Performing Links
        </h2>
        <table className={styles.table}>
          <thead>
            <tr>
              <th>Short Code</th>
              <th>Original URL</th>
              <th>Total Clicks</th>
            </tr>
          </thead>
          <tbody>
            {(data?.top_links || []).map((link) => (
              <tr key={link.short_code}>
                <td>
                  <a href={`${API_URL}/r/${link.short_code}`} target="_blank" rel="noopener noreferrer" className={styles.shortCode}>
                    shrt.x/{link.short_code}
                  </a>
                </td>
                <td>
                  <span className={styles.linkUrl}>{link.original_url}</span>
                </td>
                <td>{link.clicks}</td>
              </tr>
            ))}
            {(!data?.top_links || data.top_links.length === 0) && (
              <tr>
                <td colSpan="3" style={{ textAlign: 'center', color: 'var(--text-muted)' }}>
                  No links created yet.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </section>
    </main>
  );
}
