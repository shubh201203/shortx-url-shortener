import '../styles/globals.css'

export const metadata = {
  title: 'ShortX - Premium URL Shortener',
  description: 'Lightning fast, analytics driven URL shortener.',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
