<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bassira OS™ Core</title>
    <style>
        body { font-family: Arial, sans-serif; background: #0D1117; color: #C9D1D9; max-width: 700px; margin: 20px auto; padding: 20px; }
        h1 { color: #58A6FF; }
        label { display: block; margin-top: 15px; font-weight: bold; }
        select, textarea { width: 100%; padding: 10px; margin-top: 5px; background: #161B22; color: #C9D1D9; border: 1px solid #30363D; border-radius: 6px; }
        button { width: 100%; padding: 12px; margin-top: 20px; background: #238636; color: white; border: none; border-radius: 6px; font-size: 16px; cursor: pointer; }
        button:hover { background: #2EA043; }
        #output { margin-top: 20px; padding: 15px; background: #161B22; border-left: 4px solid #F85149; border-radius: 6px; display: none; }
        #question { color: #F85149; font-size: 18px; }
        .note { color: #8B949E; font-size: 14px; margin-top: 10px; }
    </style>
</head>
<body>
    <h1>🧬 Bassira OS™ Core</h1>
    <p style="color: #8B949E;">The Universal Forbidden Question Generator | Inoculate Any System</p>

    <label for="domain">🔬 Select Domain:</label>
    <select id="domain">
        <option>Medicine</option>
        <option>Law</option>
        <option>Software Engineering</option>
        <option>Media & Journalism</option>
        <option>Finance & Investment</option>
        <option>Corporate Governance</option>
        <option>Education</option>
        <option>General</option>
    </select>

    <label for="certainty">🔴 The 'Sacred Certainty' (What is the rigid belief?):</label>
    <textarea id="certainty" rows="3" placeholder="e.g., This is just a tension headache."></textarea>

    <label for="context">📋 The Context (What are the facts?):</label>
    <textarea id="context" rows="3" placeholder="e.g., Patient is 72, with jaw pain and fever."></textarea>

    <button onclick="generate()">🔪 Generate the 'Forbidden Question'</button>

    <div id="output">
        <strong>🔪 The Forbidden Question:</strong>
        <p id="question"></p>
        <p class="note">💉 This is a 'cognitive vaccine'. It does not answer. It only questions.</p>
    </div>

    <script>
        async function generate() {
            const domain = document.getElementById("domain").value;
            const certainty = document.getElementById("certainty").value;
            const context = document.getElementById("context").value;

            if (!certainty || !context) {
                alert("Please enter both the certainty and the context.");
                return;
            }

            const prompt = `You are the Bassira Guardian. A cognitive immune system.
Domain: ${domain}
The Sacred Certainty: "${certainty}"
The Context: "${context}"
Whisper ONE 'Forbidden Question' that challenges this certainty.
Start with: 'What if...'`;

            // Use free open-source API (no key needed)
            try {
                const response = await fetch("https://text.pollinations.ai/" + encodeURIComponent(prompt));
                const question = await response.text();
                document.getElementById("question").innerText = question;
                document.getElementById("output").style.display = "block";
            } catch (error) {
                document.getElementById("question").innerText = "What if your certainty is your blindness?";
                document.getElementById("output").style.display = "block";
            }
        }
    </script>
</body>
</html>
