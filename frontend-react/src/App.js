import React, { useState } from "react";
import axios from "axios";

function App() {
  const [jd, setJd] = useState(null);
  const [resumes, setResumes] = useState([]);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!jd || resumes.length === 0) {
      alert("⚠️ Please upload JD and resumes");
      return;
    }

    const formData = new FormData();
    formData.append("files", jd);

    resumes.forEach((file) => {
      formData.append("files", file);
    });

    setLoading(true);
    setResults([]); // 🔥 reset old results

    try {
      const response = await axios.post(
        "http://localhost:8000/analyze",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          timeout: 60000, // 🔥 prevent hanging
        }
      );

      console.log("API RESPONSE:", response.data);

      let parsed = [];

      try {
        parsed = JSON.parse(response.data.result);
      } catch (e) {
        alert("❌ Invalid response from backend");
        console.error("Parse error:", e);
      }

      if (Array.isArray(parsed)) {
        setResults(parsed);
      } else {
        alert(parsed.error || "Unknown backend error");
      }

    } catch (err) {
      console.error("ERROR:", err);

      if (err.response) {
        alert(err.response.data?.error || "Backend error");
      } else if (err.request) {
        alert("❌ Cannot connect to backend (Is server running?)");
      } else {
        alert("Unexpected error");
      }
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial", maxWidth: "900px", margin: "auto" }}>
      
      <h1 style={{ textAlign: "center" }}>
        🚀 Intelligent Resume Screening System
      </h1>

      {/* Upload Section */}
      <div style={{ marginTop: "30px" }}>
        <h3>📄 Upload Job Description</h3>
        <input type="file" onChange={(e) => setJd(e.target.files[0])} />

        <h3 style={{ marginTop: "20px" }}>📂 Upload Resumes</h3>
        <input
          type="file"
          multiple
          onChange={(e) => setResumes(Array.from(e.target.files))}
        />
      </div>

      <br />

      <button
        onClick={handleSubmit}
        style={{
          padding: "12px 25px",
          backgroundColor: "#4CAF50",
          color: "white",
          border: "none",
          borderRadius: "6px",
          cursor: "pointer",
          fontSize: "16px"
        }}
      >
        🔍 Analyze Candidates
      </button>

      {loading && (
        <p style={{ marginTop: "20px", fontWeight: "bold" }}>
          🤖 AI is analyzing resumes...
        </p>
      )}

      {/* RESULTS */}
      <div style={{ marginTop: "40px" }}>

        {results.length > 0 && (
          <h2 style={{ borderBottom: "2px solid #ddd", paddingBottom: "10px" }}>
            📊 Candidate Ranking
          </h2>
        )}

        {results.map((c, index) => (
          <div
            key={index}
            style={{
              border: "1px solid #ddd",
              padding: "20px",
              marginTop: "15px",
              borderRadius: "12px",
              boxShadow: "0px 4px 12px rgba(0,0,0,0.1)",
              backgroundColor: "#fff"
            }}
          >
            <h3>📄 {c.name}</h3>

            <p><b>Score:</b> {c.score}%</p>
            <p><b>AI Score:</b> {c.ai_score}</p>
            <p><b>Experience:</b> {c.experience} years</p>
            <p><b>Company Score:</b> {c.company_score}</p>

            <p>
              <b>Education:</b>{" "}
              {Array.isArray(c.education) && c.education.length > 0
                ? c.education.join(", ")
                : "None"}
            </p>

            <p>
              <b>Matched Skills:</b>{" "}
              {Array.isArray(c.matched_skills)
                ? c.matched_skills.join(", ")
                : "None"}
            </p>

            <p><b>Reason:</b> {c.reason}</p>

            {/* 🔥 AI BADGE */}
            <div style={{ marginTop: "10px" }}>
              {c.ai_score >= 80 ? (
                <span style={{ color: "green", fontWeight: "bold" }}>
                  🔥 Highly Recommended
                </span>
              ) : c.ai_score >= 60 ? (
                <span style={{ color: "orange", fontWeight: "bold" }}>
                  👍 Good Fit
                </span>
              ) : (
                <span style={{ color: "red", fontWeight: "bold" }}>
                  ⚠️ Needs Improvement
                </span>
              )}
            </div>

            {/* 🔥 AI FEEDBACK */}
            <details style={{ marginTop: "15px" }}>
              <summary style={{ cursor: "pointer", fontWeight: "bold" }}>
                🤖 View AI Feedback
              </summary>
              <pre style={{ whiteSpace: "pre-wrap", marginTop: "10px" }}>
                {c.ai_feedback}
              </pre>
            </details>
          </div>
        ))}

      </div>

    </div>
  );
}

export default App;