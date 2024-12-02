{% extends 'base.html' %}

{% block title %}Network Vulnerability Scanner{% endblock %}

{% block content %}
<div class="container">
    <header>
            <div class="header-text">
                <h2>Network Vulnerability Scanner</h2>
                <p>T The Network Vulnerability Scanner is a highly accurate tool that detects 12.073 CVEs in extensively used software products and technologies.

                    With daily vulnerability updates and a very low rate of false positives, the scanner provides reliable results for your next move.</p>
            </div>
            <img class="header-image" src="{{ url_for('static', filename='images/net.jpg') }}" alt="Authenticated Scanning">
        </header>

    <form id="scanner-form" action="{{ url_for('network_scanner') }}" method="POST">
        <label for="scan_type">Scan Type:</label>
        <select id="scan_type" name="scan_type" required>
            <option value="single">Single IP</option>
            <option value="range">IP Range</option>
        </select>

        <div id="single-scan">
            <label for="target_ip">Target IP Address:</label>
            <input type="text" id="target_ip" name="target_ip" placeholder="e.g., 192.168.1.1">
        </div>

        <div id="range-scan" style="display: none;">
            <label for="start_ip">Start IP:</label>
            <input type="text" id="start_ip" name="start_ip" placeholder="e.g., 192.168.1.1">
            <label for="end_ip">End IP:</label>
            <input type="text" id="end_ip" name="end_ip" placeholder="e.g., 192.168.1.255">
        </div>

        <label for="start_port">Start Port:</label>
        <input type="number" id="start_port" name="start_port" value="1" required>

        <label for="end_port">End Port:</label>
        <input type="number" id="end_port" name="end_port" value="65535" required>

        <input type="checkbox" id="authorized" name="authorized" required>
        <label for="authorized">
            I agree to the <a href="#">Terms of Service</a>.
        </label>

        <button type="submit">Start Scan</button>
    </form>

    <!-- Scanning Icon -->
    <div id="scanning-icon" class="hidden">
        <img src="{{ url_for('static', filename='images/scanning.gif') }}" alt="Scanning Icon" />
        <p>Scanning in progress... Please wait.</p>
    </div>

    <!-- Results Dropdown -->
    <div id="results">
        <h3>Scan Results:</h3>
        <button id="toggle-results" class="hidden">Show Results</button>
        <div id="results-content" class="hidden">
            <pre>No results yet. Start a scan to view results.</pre>
        </div>
    </div>
</div>

<script>
    const form = document.getElementById('scanner-form');
    const scanningIcon = document.getElementById('scanning-icon');
    const resultsDiv = document.getElementById('results');
    const toggleResults = document.getElementById('toggle-results');
    const resultsContent = document.getElementById('results-content');
    const scanType = document.getElementById('scan_type');
    const singleScan = document.getElementById('single-scan');
    const rangeScan = document.getElementById('range-scan');

    // Show/hide scan options
    scanType.addEventListener('change', () => {
        if (scanType.value === 'single') {
            singleScan.style.display = 'block';
            rangeScan.style.display = 'none';
        } else {
            singleScan.style.display = 'none';
            rangeScan.style.display = 'block';
        }
    });

    // Handle form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        scanningIcon.classList.remove('hidden'); // Show scanning icon
        resultsContent.innerHTML = "<pre>Scanning...</pre>"; // Update pre element
        toggleResults.classList.add('hidden'); // Hide toggle button

        const formData = new FormData(form);
        const response = await fetch(form.action, {
            method: form.method,
            body: formData,
        });

        scanningIcon.classList.add('hidden'); // Hide scanning icon

        if (response.ok) {
            const data = await response.json();
            resultsContent.innerHTML = `
                <pre>${data.output}</pre>
                <p><a href="${data.pdf_link}" target="_blank">Download PDF Report</a></p>
                <p><a href="${data.word_link}" target="_blank">Download Word Report</a></p>
            `;
            toggleResults.classList.remove('hidden'); // Show toggle button
        } else {
            const errorData = await response.json();
            resultsContent.innerHTML = `
                <pre>${errorData.error}</pre>
            `;
        }
    });

    // Handle dropdown toggle
    toggleResults.addEventListener('click', (e) => {
        if (resultsContent.classList.contains('hidden')) {
            resultsContent.classList.remove('hidden');
            e.target.textContent = 'Hide Results';
        } else {
            resultsContent.classList.add('hidden');
            e.target.textContent = 'Show Results';
        }
    });
</script>

<style>
    .hidden {
        display: none;
    }

    #scanning-icon {
        text-align: center;
        margin: 20px 0;
    }

    #scanning-icon img {
        width: 50px; /* Adjust size as needed */
    }

    #results-content {
        background-color: #f9f9f9;
        border: 1px solid #ddd;
        padding: 10px;
        margin-top: 10px;
        max-height: 300px;
        overflow-y: auto; /* Scrollable if results are large */
    }

    #toggle-results {
        background-color: #007bff;
        color: white;
        padding: 10px 15px;
        border: none;
        cursor: pointer;
        border-radius: 5px;
        margin-top: 10px;
    }

    #toggle-results:hover {
        background-color: #0056b3;
    }
</style>
{% endblock %}
