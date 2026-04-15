const express = require("express");
const multer = require("multer");
const cors = require("cors");
const { exec } = require("child_process");
const path = require("path");
const fs = require("fs");

const app = express();

// ✅ CORS (allow all for dev)
app.use(cors());
app.use(express.json());

// ✅ Upload config
const upload = multer({ dest: "uploads/" });


// 🚀 MAIN API
app.post("/analyze", upload.any(), (req, res) => {

    console.log("🔥 Request received");

    try {
        const projectRoot = path.resolve(__dirname, "..");
        const resumeDir = path.join(projectRoot, "data/resumes");

        // ✅ Ensure folder exists
        if (!fs.existsSync(resumeDir)) {
            fs.mkdirSync(resumeDir, { recursive: true });
        }

        // 🔥 CLEAR OLD FILES (SAFE)
        const files = fs.readdirSync(resumeDir);
        for (const file of files) {
            try {
                fs.unlinkSync(path.join(resumeDir, file));
            } catch (err) {
                console.log("⚠️ File delete error:", err.message);
            }
        }

        // ❌ No files uploaded
        if (!req.files || req.files.length === 0) {
            return res.status(400).json({
                error: "❌ No files uploaded"
            });
        }

        // 🔥 SAVE FILES
        let hasJD = false;

        for (const file of req.files) {

            const filename = file.originalname;

            // ✅ detect JD
            if (filename.toLowerCase().includes("jd")) {
                hasJD = true;
            }

            const newPath = path.join(resumeDir, filename);

            try {
                fs.renameSync(file.path, newPath);
            } catch (err) {
                console.error("❌ File move error:", err.message);
            }
        }

        // ❌ If JD missing
        if (!hasJD) {
            return res.status(400).json({
                error: "❌ Please upload a JD file (filename must contain 'jd')"
            });
        }

        // 🚀 RUN PYTHON (SAFE EXEC)
        const command = `
            cd "${projectRoot}" && 
            ./venv/bin/python main.py
        `;

        exec(
            command,
            {
                maxBuffer: 1024 * 1024 * 10, // 10MB
                timeout: 60000 // 🔥 60 sec timeout
            },
            (error, stdout, stderr) => {

                console.log("STDOUT:", stdout);
                console.log("STDERR:", stderr);

                // ❌ Python crash
                if (error) {
                    console.error("❌ PYTHON ERROR:", error.message);

                    return res.status(500).json({
                        error: "Python execution failed",
                        details: stderr || error.message
                    });
                }

                // ❌ No output
                if (!stdout || stdout.trim() === "") {
                    return res.status(500).json({
                        error: "No output from Python"
                    });
                }

                // 🔥 Validate JSON before sending
                try {
                    JSON.parse(stdout);
                } catch (e) {
                    return res.status(500).json({
                        error: "Invalid JSON from Python",
                        details: stdout
                    });
                }

                // ✅ SUCCESS RESPONSE
                return res.json({
                    result: stdout.trim()
                });
            }
        );

    } catch (err) {
        console.error("❌ SERVER ERROR:", err.message);

        return res.status(500).json({
            error: "Internal server error",
            details: err.message
        });
    }
});


// ✅ Health check route
app.get("/", (req, res) => {
    res.send("✅ Backend running");
});


// 🚀 START SERVER
app.listen(8000, () => {
    console.log("🚀 Server running on http://localhost:8000");
});