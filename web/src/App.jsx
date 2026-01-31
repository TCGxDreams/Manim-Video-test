import { useState, useEffect } from 'react'
import './App.css'

const API_URL = 'http://localhost:5000/api'

function App() {
  const [topic, setTopic] = useState('')
  const [language, setLanguage] = useState('en')
  const [duration, setDuration] = useState(1)
  const [jobId, setJobId] = useState(null)
  const [status, setStatus] = useState(null)
  const [videos, setVideos] = useState([])
  const [isGenerating, setIsGenerating] = useState(false)

  // Fetch videos on mount
  useEffect(() => {
    fetchVideos()
  }, [])

  // Poll status when generating
  useEffect(() => {
    if (!jobId) return

    const interval = setInterval(async () => {
      try {
        const res = await fetch(`${API_URL}/status/${jobId}`)
        const data = await res.json()
        setStatus(data)

        if (data.status === 'completed' || data.status === 'error') {
          setIsGenerating(false)
          clearInterval(interval)
          fetchVideos()
        }
      } catch (err) {
        console.error(err)
      }
    }, 2000)

    return () => clearInterval(interval)
  }, [jobId])

  const fetchVideos = async () => {
    try {
      const res = await fetch(`${API_URL}/videos`)
      const data = await res.json()
      setVideos(data)
    } catch (err) {
      console.error(err)
    }
  }

  const handleGenerate = async () => {
    if (!topic.trim()) {
      alert('Please enter a topic / Vui long nhap chu de')
      return
    }

    setIsGenerating(true)
    setStatus(null)

    try {
      const res = await fetch(`${API_URL}/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic, language, duration })
      })
      const data = await res.json()
      setJobId(data.job_id)
    } catch (err) {
      alert('Failed to start generation / Khong the bat dau tao video')
      setIsGenerating(false)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>🎬 Manim AI Studio</h1>
        <p className="subtitle">AI-Powered Math Animation Generator</p>
      </header>

      <main className="main">
        <section className="generator-section">
          <h2>Create Video / Tao Video</h2>

          <div className="form-group">
            <label>Topic / Chu de:</label>
            <input
              type="text"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="e.g., Basic Derivatives - derivative of x^n, sin(x), e^x"
              disabled={isGenerating}
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Language / Ngon ngu:</label>
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                disabled={isGenerating}
              >
                <option value="en">English</option>
                <option value="vi">Tieng Viet</option>
              </select>
            </div>

            <div className="form-group">
              <label>Duration / Thoi luong:</label>
              <select
                value={duration}
                onChange={(e) => setDuration(Number(e.target.value))}
                disabled={isGenerating}
              >
                <option value={1}>1 minute / phut</option>
                <option value={3}>3 minutes / phut</option>
              </select>
            </div>
          </div>

          <button
            className="generate-btn"
            onClick={handleGenerate}
            disabled={isGenerating}
          >
            {isGenerating ? 'Generating... / Dang tao...' : 'Generate Video / Tao Video'}
          </button>
        </section>

        {status && (
          <section className="status-section">
            <h2>Progress / Tien trinh</h2>
            <div className="progress-container">
              <div
                className="progress-bar"
                style={{ width: `${status.progress || 0}%` }}
              />
            </div>
            <p className="phase">{status.phase}</p>
            {status.status === 'error' && (
              <p className="error">Error: {status.error}</p>
            )}
            {status.status === 'completed' && (
              <div className="completed">
                <p>Video completed! / Video hoan thanh!</p>
                <a
                  href={`${API_URL}/videos/${status.video_path}`}
                  target="_blank"
                  className="download-btn"
                >
                  Download Video
                </a>
              </div>
            )}
          </section>
        )}

        <section className="videos-section">
          <h2>Generated Videos / Video da tao</h2>
          {videos.length === 0 ? (
            <p className="no-videos">No videos yet / Chua co video nao</p>
          ) : (
            <div className="video-list">
              {videos.map((video) => (
                <div key={video.name} className="video-card">
                  <div className="video-info">
                    <span className="video-name">{video.name}</span>
                    <span className="video-size">
                      {(video.size / 1024 / 1024).toFixed(2)} MB
                    </span>
                  </div>
                  <div className="video-actions">
                    <a
                      href={`${API_URL}/videos/${video.name}`}
                      target="_blank"
                      className="action-btn"
                    >
                      View / Xem
                    </a>
                    <a
                      href={`${API_URL}/videos/${video.name}`}
                      download
                      className="action-btn download"
                    >
                      Download / Tai
                    </a>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
      </main>

      <footer className="footer">
        <p>Powered by Google Gemini + Manim Community</p>
      </footer>
    </div>
  )
}

export default App
