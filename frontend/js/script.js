/**
 * Code2Algo — Intelligent Code-to-Algorithm Generator
 * Frontend Interactive Controller
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Element References
    const languageSelect = document.getElementById('languageSelect');
    const exampleSelect = document.getElementById('exampleSelect');
    const clearBtn = document.getElementById('clearBtn');
    const codeEditor = document.getElementById('codeEditor');
    const lineNumbers = document.getElementById('lineNumbers');
    const charCount = document.getElementById('charCount');
    const generateBtn = document.getElementById('generateBtn');
    
    const detailCards = document.querySelectorAll('.detail-card');
    const engineStatusBadge = document.getElementById('engineStatusBadge');
    const engineStatusText = document.getElementById('engineStatusText');

    const emptyState = document.getElementById('emptyState');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const loadingStatusText = document.getElementById('loadingStatusText');
    const progressBarFill = document.getElementById('progressBarFill');
    const resultsContainer = document.getElementById('resultsContainer');

    // Result Card Elements
    const resultTitle = document.getElementById('resultTitle');
    const resultDetailBadge = document.getElementById('resultDetailBadge');
    const resultEngineBadge = document.getElementById('resultEngineBadge');
    
    const algorithmContent = document.getElementById('algorithmContent');
    const pseudocodeContent = document.getElementById('pseudocodeContent');
    const explanationContent = document.getElementById('explanationContent');
    const inputDescContent = document.getElementById('inputDescContent');
    const outputDescContent = document.getElementById('outputDescContent');
    const timeCompBadge = document.getElementById('timeCompBadge');
    const timeCompExpl = document.getElementById('timeCompExpl');
    const spaceCompBadge = document.getElementById('spaceCompBadge');
    const spaceCompExpl = document.getElementById('spaceCompExpl');
    const conceptsContainer = document.getElementById('conceptsContainer');

    // Action & Layout Buttons
    const btnSplitView = document.getElementById('btnSplitView');
    const btnFullWidthView = document.getElementById('btnFullWidthView');
    const toggleFullscreenBtn = document.getElementById('toggleFullscreenBtn');
    const editorOutputGrid = document.querySelector('.editor-output-grid');
    const outputPanel = document.getElementById('outputPanel');

    const copyAllBtn = document.getElementById('copyAllBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const printBtn = document.getElementById('printBtn');
    const toastContainer = document.getElementById('toastContainer');

    // State Variables
    let selectedDetailLevel = 'professional';
    let cachedExamples = {};
    let currentResultData = null;

    // Initialize Application
    init();

    function init() {
        if (window.mermaid) {
            try {
                mermaid.initialize({
                    startOnLoad: false,
                    suppressErrorRendering: true,
                    theme: 'dark',
                    themeVariables: {
                        darkMode: true,
                        primaryColor: '#6366f1',
                        primaryTextColor: '#ffffff',
                        primaryBorderColor: '#818cf8',
                        lineColor: '#06b6d4',
                        secondaryColor: '#1e293b',
                        tertiaryColor: '#0f172a'
                    },
                    flowchart: {
                        useMaxWidth: true,
                        htmlLabels: true,
                        curve: 'basis'
                    }
                });
            } catch (e) {
                console.warn('Mermaid initialization warning:', e);
            }
        }
        setupEventListeners();
        updateLineNumbers();
        fetchHealthStatus();
        fetchExamples();
    }

    function setupEventListeners() {
        // Detail Level Mode Cards Selection
        detailCards.forEach(card => {
            card.addEventListener('click', () => {
                detailCards.forEach(c => c.classList.remove('active'));
                card.classList.add('active');
                selectedDetailLevel = card.getAttribute('data-mode');
            });
        });

        // Code Editor Line Numbers, Char Counter & Language Auto-Detection
        let detectTimeout = null;
        codeEditor.addEventListener('input', () => {
            updateLineNumbers();
            updateCharCount();
            clearTimeout(detectTimeout);
            detectTimeout = setTimeout(() => {
                autoDetectAndUpdateLanguage(codeEditor.value, false);
            }, 300);
        });

        // Instant Auto-Detection on Paste Event
        codeEditor.addEventListener('paste', () => {
            setTimeout(() => {
                updateLineNumbers();
                updateCharCount();
                autoDetectAndUpdateLanguage(codeEditor.value, true);
            }, 30);
        });

        codeEditor.addEventListener('scroll', () => {
            lineNumbers.scrollTop = codeEditor.scrollTop;
        });

        // Handle Tab key inside code editor
        codeEditor.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                e.preventDefault();
                const start = codeEditor.selectionStart;
                const end = codeEditor.selectionEnd;
                codeEditor.value = codeEditor.value.substring(0, start) + '    ' + codeEditor.value.substring(end);
                codeEditor.selectionStart = codeEditor.selectionEnd = start + 4;
                updateLineNumbers();
                updateCharCount();
            }
        });

        // Language Selector Change
        languageSelect.addEventListener('change', (e) => {
            if (e.target.value === 'auto') {
                const detected = detectLanguage(codeEditor.value);
                if (detected) {
                    languageSelect.value = detected;
                    showToast(`Auto-detected language: ${formatLanguageName(detected)}`, 'info');
                }
            }
        });

        // Clear Code Area
        clearBtn.addEventListener('click', () => {
            codeEditor.value = '';
            exampleSelect.selectedIndex = 0;
            const autoOption = languageSelect.querySelector('option[value="auto"]');
            if (autoOption) autoOption.textContent = '⚡ Auto-Detect';
            updateLineNumbers();
            updateCharCount();
            showToast('Code area cleared', 'info');
        });

        // Example Loader
        exampleSelect.addEventListener('change', (e) => {
            const selectedKey = e.target.value;
            if (cachedExamples[selectedKey]) {
                const ex = cachedExamples[selectedKey];
                codeEditor.value = ex.code;
                languageSelect.value = ex.language;
                updateLineNumbers();
                updateCharCount();
                showToast(`Loaded example: ${ex.title}`, 'success');
            }
        });

        // Generate Algorithm Primary Button
        generateBtn.addEventListener('click', handleGenerateAlgorithm);

        // Copy Card Buttons
        document.querySelectorAll('.copy-card-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const targetId = btn.getAttribute('data-target');
                const targetEl = document.getElementById(targetId);
                if (targetEl) {
                    copyToClipboard(targetEl.innerText, 'Section copied to clipboard!');
                }
            });
        });

        // Layout View Mode Switchers
        if (btnSplitView && btnFullWidthView) {
            btnSplitView.addEventListener('click', () => {
                btnSplitView.classList.add('active');
                btnFullWidthView.classList.remove('active');
                editorOutputGrid.classList.remove('layout-fullwidth');
                showToast('Switched to Side-by-Side Split View', 'info');
            });

            btnFullWidthView.addEventListener('click', () => {
                btnFullWidthView.classList.add('active');
                btnSplitView.classList.remove('active');
                editorOutputGrid.classList.add('layout-fullwidth');
                showToast('Switched to 100% Full Width View', 'success');
            });
        }

        // Fullscreen Toggle
        if (toggleFullscreenBtn && outputPanel) {
            toggleFullscreenBtn.addEventListener('click', () => {
                const isFullscreen = outputPanel.classList.toggle('fullscreen-active');
                if (isFullscreen) {
                    toggleFullscreenBtn.innerHTML = '<i class="fa-solid fa-compress"></i> Exit Fullscreen';
                    showToast('Entered Fullscreen Results (Press Esc to exit)', 'success');
                } else {
                    toggleFullscreenBtn.innerHTML = '<i class="fa-solid fa-expand"></i> Fullscreen';
                }
            });

            // Close fullscreen on Escape key
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && outputPanel.classList.contains('fullscreen-active')) {
                    outputPanel.classList.remove('fullscreen-active');
                    toggleFullscreenBtn.innerHTML = '<i class="fa-solid fa-expand"></i> Fullscreen';
                    showToast('Exited Fullscreen View', 'info');
                }
            });
        }

        // Export Actions
        copyAllBtn.addEventListener('click', handleCopyFullReport);
        downloadBtn.addEventListener('click', handleDownloadReport);
        printBtn.addEventListener('click', () => window.print());
    }

    function updateLineNumbers() {
        const lines = codeEditor.value.split('\n');
        const count = lines.length || 1;
        let numbersHtml = '';
        for (let i = 1; i <= count; i++) {
            numbersHtml += `${i}<br>`;
        }
        lineNumbers.innerHTML = numbersHtml;
    }

    function updateCharCount() {
        const len = codeEditor.value.length;
        charCount.textContent = `${len.toLocaleString()} character${len === 1 ? '' : 's'}`;
    }

    async function fetchHealthStatus() {
        try {
            const resp = await fetch('/api/health');
            if (resp.ok) {
                const data = await resp.json();
                if (data.ai_provider && data.ai_provider !== 'none') {
                    engineStatusBadge.className = 'engine-badge ai';
                    engineStatusText.textContent = `${data.ai_provider.toUpperCase()} AI Active`;
                } else {
                    engineStatusBadge.className = 'engine-badge offline';
                    engineStatusText.textContent = 'Rule-Based Engine';
                }
            }
        } catch (e) {
            engineStatusBadge.className = 'engine-badge offline';
            engineStatusText.textContent = 'Rule-Based Engine';
        }
    }

    async function fetchExamples() {
        try {
            const resp = await fetch('/api/examples');
            if (resp.ok) {
                const data = await resp.json();
                if (data.success && data.examples) {
                    cachedExamples = data.examples;
                }
            }
        } catch (e) {
            console.warn('Could not load server examples:', e);
        }
    }

    async function handleGenerateAlgorithm() {
        const code = codeEditor.value.trim();
        let language = languageSelect.value;
        if (!language || language === 'auto') {
            language = detectLanguage(code) || 'python';
        }

        if (!code) {
            showToast('Please enter or paste source code before generating.', 'error');
            codeEditor.focus();
            return;
        }

        // Show Loading Overlay with Multi-stage animation
        showLoadingState();

        try {
            const payload = {
                language: language,
                code: code,
                detail_level: selectedDetailLevel
            };

            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (response.ok && data.success) {
                currentResultData = data;
                // Transition progress bar to 100%
                updateProgressBar(100, 'Finalizing report generation...');
                setTimeout(() => {
                    hideLoadingState();
                    renderResults(data);
                    showToast('Algorithm generated successfully!', 'success');
                }, 400);
            } else {
                hideLoadingState();
                showToast(data.error || 'Failed to generate algorithm.', 'error');
            }
        } catch (err) {
            hideLoadingState();
            showToast('Network error while reaching server.', 'error');
            console.error('Generation Error:', err);
        }
    }

    function showLoadingState() {
        emptyState.classList.add('hidden');
        resultsContainer.classList.add('hidden');
        loadingOverlay.classList.remove('hidden');

        updateProgressBar(25, 'Analyzing code structures...');

        setTimeout(() => {
            if (!loadingOverlay.classList.contains('hidden')) {
                updateProgressBar(65, 'Evaluating Big-O complexity & loop depth...');
            }
        }, 500);

        setTimeout(() => {
            if (!loadingOverlay.classList.contains('hidden')) {
                updateProgressBar(85, 'Constructing step-by-step algorithm...');
            }
        }, 900);
    }

    function updateProgressBar(percentage, text) {
        progressBarFill.style.width = `${percentage}%`;
        loadingStatusText.textContent = text;
    }

    function hideLoadingState() {
        loadingOverlay.classList.add('hidden');
    }

    function renderResults(data) {
        // Title & Badges
        resultTitle.textContent = data.title || 'Generated Algorithm';
        resultDetailBadge.textContent = `${data.detail_level.toUpperCase()} Mode`;
        resultEngineBadge.textContent = data.engine || 'Rule-Based Engine';

        // 1. Algorithm Steps
        algorithmContent.innerHTML = '';
        const stepsList = document.createElement('div');
        stepsList.className = 'algorithm-step-list';

        if (Array.isArray(data.algorithm)) {
            data.algorithm.forEach((stepText) => {
                const stepEl = document.createElement('div');
                stepEl.className = 'step-item';

                // Format bold terms
                let formatted = stepText.replace(/`([^`]+)`/g, '<code>$1</code>');
                stepEl.innerHTML = formatted;
                stepsList.appendChild(stepEl);
            });
        }
        algorithmContent.appendChild(stepsList);

        // 2. Pseudocode
        pseudocodeContent.textContent = data.pseudocode || 'START\n  PROCESS\nSTOP';

        // 3. Flowchart Diagram
        const flowchartContainer = document.getElementById('flowchartContainer');
        const flowchartRawCode = document.getElementById('flowchartRawCode');
        if (flowchartContainer && data.flowchart) {
            flowchartRawCode.textContent = data.flowchart;
            flowchartContainer.removeAttribute('data-processed');
            flowchartContainer.innerHTML = '';
            
            if (window.mermaid) {
                try {
                    const chartId = 'flowchartSvg_' + Date.now();
                    mermaid.render(chartId, data.flowchart).then(renderResult => {
                        flowchartContainer.innerHTML = renderResult.svg;
                        // Clean up any stray error elements
                        document.querySelectorAll('body > [id^="dmermaid"], body > .error-icon').forEach(el => el.remove());
                    }).catch(err => {
                        console.warn('Mermaid render warning:', err);
                        flowchartContainer.innerHTML = `<pre class="pseudocode-block">${data.flowchart}</pre>`;
                        // Clean up any stray error elements
                        document.querySelectorAll('body > [id^="dmermaid"], body > .error-icon').forEach(el => el.remove());
                    });
                } catch (mErr) {
                    console.warn('Mermaid execution warning:', mErr);
                    flowchartContainer.innerHTML = `<pre class="pseudocode-block">${data.flowchart}</pre>`;
                    document.querySelectorAll('body > [id^="dmermaid"], body > .error-icon').forEach(el => el.remove());
                }
            } else {
                flowchartContainer.innerHTML = `<pre class="pseudocode-block">${data.flowchart}</pre>`;
            }
        }

        // 4. Explanation
        let explFormatted = (data.explanation || '').replace(/`([^`]+)`/g, '<code>$1</code>');
        explFormatted = explFormatted.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
        explanationContent.innerHTML = `<p>${explFormatted}</p>`;

        // 5. Input & Output
        inputDescContent.textContent = data.input || 'Standard functional inputs.';
        outputDescContent.textContent = data.output || 'Calculated return result.';

        // 6. Program Execution Output (Console Preview)
        const sampleOutputContent = document.getElementById('sampleOutputContent');
        if (sampleOutputContent) {
            sampleOutputContent.textContent = data.sample_output || '>> Program output not available.';
        }

        // 7. Complexity Analysis
        timeCompBadge.textContent = data.time_complexity || 'O(1)';
        timeCompExpl.textContent = data.time_explanation || '';

        spaceCompBadge.textContent = data.space_complexity || 'O(1)';
        spaceCompExpl.textContent = data.space_explanation || '';

        // 8. Concept Tags
        conceptsContainer.innerHTML = '';
        const concepts = data.concepts || [];
        if (concepts.length === 0) {
            concepts.push('General Algorithmic Logic');
        }

        concepts.forEach(concept => {
            const pill = document.createElement('span');
            pill.className = 'tag-pill';
            pill.innerHTML = `<i class="fa-solid fa-check"></i> ${concept}`;
            conceptsContainer.appendChild(pill);
        });

        // Reveal Results Container
        resultsContainer.classList.remove('hidden');

        // Scroll into view on mobile
        if (window.innerWidth <= 1024) {
            resultsContainer.scrollIntoView({ behavior: 'smooth' });
        }
    }

    function handleCopyFullReport() {
        if (!currentResultData) return;

        const report = `==================================================
Code2Algo — Generated Algorithm Report
==================================================
Title: ${currentResultData.title}
Detail Level: ${currentResultData.detail_level.toUpperCase()}
Engine: ${currentResultData.engine || 'Rule-Based Engine'}

--------------------------------------------------
STEP-BY-STEP ALGORITHM
--------------------------------------------------
${(currentResultData.algorithm || []).join('\n\n')}

--------------------------------------------------
PSEUDOCODE
--------------------------------------------------
${currentResultData.pseudocode}

--------------------------------------------------
PROGRAM FLOWCHART (MERMAID)
--------------------------------------------------
${currentResultData.flowchart || ''}

--------------------------------------------------
PROGRAM EXPLANATION
--------------------------------------------------
${currentResultData.explanation}

--------------------------------------------------
INPUT & OUTPUT SPECIFICATIONS
--------------------------------------------------
Input: ${currentResultData.input}
Output: ${currentResultData.output}

--------------------------------------------------
PROGRAM EXECUTION OUTPUT (CONSOLE PREVIEW)
--------------------------------------------------
${currentResultData.sample_output || ''}

--------------------------------------------------
COMPLEXITY ANALYSIS
--------------------------------------------------
Time Complexity: ${currentResultData.time_complexity}
Rationale: ${currentResultData.time_explanation}

Space Complexity: ${currentResultData.space_complexity}
Rationale: ${currentResultData.space_explanation}

--------------------------------------------------
DETECTED CONCEPTS
--------------------------------------------------
${(currentResultData.concepts || []).join(', ')}
==================================================
`;

        copyToClipboard(report, 'Full algorithm report copied to clipboard!');
    }

    function handleDownloadReport() {
        if (!currentResultData) return;

        const reportText = `==================================================
Code2Algo — Generated Algorithm Report
==================================================
Title: ${currentResultData.title}
Detail Level: ${currentResultData.detail_level.toUpperCase()}
Engine: ${currentResultData.engine || 'Rule-Based Engine'}

--------------------------------------------------
STEP-BY-STEP ALGORITHM
--------------------------------------------------
${(currentResultData.algorithm || []).join('\n\n')}

--------------------------------------------------
PSEUDOCODE
--------------------------------------------------
${currentResultData.pseudocode}

--------------------------------------------------
PROGRAM FLOWCHART (MERMAID)
--------------------------------------------------
${currentResultData.flowchart || ''}

--------------------------------------------------
PROGRAM EXPLANATION
--------------------------------------------------
${currentResultData.explanation}

--------------------------------------------------
INPUT & OUTPUT SPECIFICATIONS
--------------------------------------------------
Input: ${currentResultData.input}
Output: ${currentResultData.output}

--------------------------------------------------
PROGRAM EXECUTION OUTPUT (CONSOLE PREVIEW)
--------------------------------------------------
${currentResultData.sample_output || ''}

--------------------------------------------------
COMPLEXITY ANALYSIS
--------------------------------------------------
Time Complexity: ${currentResultData.time_complexity}
Rationale: ${currentResultData.time_explanation}

Space Complexity: ${currentResultData.space_complexity}
Rationale: ${currentResultData.space_explanation}

--------------------------------------------------
DETECTED CONCEPTS
--------------------------------------------------
${(currentResultData.concepts || []).join(', ')}
==================================================
`;

        const blob = new Blob([reportText], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `Code2Algo_${currentResultData.title.replace(/\s+/g, '_')}.txt`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);

        showToast('Report downloaded as text file', 'success');
    }

    function copyToClipboard(text, successMsg) {
        navigator.clipboard.writeText(text).then(() => {
            showToast(successMsg, 'success');
        }).catch(err => {
            showToast('Failed to copy text', 'error');
        });
    }

    function showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        
        let iconClass = 'fa-info-circle';
        if (type === 'success') iconClass = 'fa-circle-check';
        if (type === 'error') iconClass = 'fa-circle-xmark';

        toast.innerHTML = `<i class="fa-solid ${iconClass}"></i> <span>${message}</span>`;
        toastContainer.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, 300);
        }, 3000);
    }

    /**
     * Language Auto-Detection & Formatting Functions
     */
    function formatLanguageName(lang) {
        const names = {
            'c': 'C',
            'cpp': 'C++',
            'python': 'Python',
            'javascript': 'JavaScript',
            'typescript': 'TypeScript',
            'java': 'Java',
            'csharp': 'C#',
            'go': 'Go (Golang)',
            'rust': 'Rust',
            'kotlin': 'Kotlin',
            'swift': 'Swift',
            'php': 'PHP',
            'ruby': 'Ruby',
            'dart': 'Dart',
            'scala': 'Scala',
            'r': 'R',
            'sql': 'SQL'
        };
        return names[lang] || (lang ? lang.toUpperCase() : 'Unknown');
    }

    function autoDetectAndUpdateLanguage(code, isPaste = false) {
        if (!code || !code.trim()) return;
        const detected = detectLanguage(code);
        if (detected) {
            const autoOption = languageSelect.querySelector('option[value="auto"]');
            if (autoOption) {
                autoOption.textContent = `⚡ Auto-Detect (${formatLanguageName(detected)})`;
            }
            // Auto switch dropdown when on auto mode or when pasting new code snippet
            if (languageSelect.value === 'auto' || isPaste) {
                languageSelect.value = detected;
                if (isPaste) {
                    showToast(`Auto-detected: ${formatLanguageName(detected)}`, 'info');
                }
            }
        }
    }

    function detectLanguage(code) {
        if (!code || !code.trim()) return null;
        const text = code.trim();

        const scores = {
            c: 0,
            cpp: 0,
            python: 0,
            javascript: 0,
            typescript: 0,
            java: 0,
            csharp: 0,
            php: 0,
            go: 0,
            rust: 0,
            kotlin: 0,
            swift: 0,
            ruby: 0,
            dart: 0,
            scala: 0,
            r: 0,
            sql: 0
        };

        // 1. C & C++
        if (/#include\s*<(stdio|stdlib|string|stdint|stdbool|math|unistd|fcntl|sys\/|errno|ctype|time|assert)\.h>/i.test(text)) {
            scores.c += 35;
        }
        if (/#include\s*<(iostream|vector|string|algorithm|map|set|queue|stack|deque|memory|cmath|cstdio|cstdlib|bits\/stdc\+\+\.h)>/i.test(text)) {
            scores.cpp += 40;
        }
        if (/#include\s*[<"][a-zA-Z0-9_./\\]+[>"]/i.test(text)) {
            scores.c += 10;
            scores.cpp += 10;
        }
        if (/\b(std::|cout\s*<<|cin\s*>>|endl\b|nullptr\b|template\s*<|constexpr\b|class\s+\w+\s*:\s*(public|private|protected))/i.test(text)) {
            scores.cpp += 25;
        }
        if (/\b(printf|scanf|fprintf|sprintf|snprintf|malloc|calloc|realloc|free|memcpy|memset)\s*\(/i.test(text)) {
            scores.c += 18;
            scores.cpp += 8;
        }
        if (/\b(uint8_t|uint16_t|uint32_t|uint64_t|int8_t|int16_t|int32_t|int64_t|size_t|ssize_t|intptr_t|uintptr_t)\b/i.test(text)) {
            scores.c += 20;
            scores.cpp += 10;
        }
        if (/\btypedef\s+struct\b|\bstruct\s+\w+\s*\{/i.test(text)) {
            scores.c += 12;
            scores.cpp += 8;
        }

        // 2. Python
        if (/\bdef\s+[a-zA-Z_]\w*\s*\([^)]*\)\s*:/i.test(text)) scores.python += 25;
        if (/\b(elif|pass|None|True|False|self\.)\b/i.test(text)) scores.python += 15;
        if (/^\s*(import\s+[a-zA-Z_]\w*|from\s+[a-zA-Z_]\w*\s+import)/m.test(text)) scores.python += 20;
        if (/if\s+__name__\s*==\s*['"]__main__['"]\s*:/i.test(text)) scores.python += 30;
        if (/\bprint\s*\([^)]*\)/i.test(text) && !/[;{}]/.test(text)) scores.python += 12;
        if (/\bin\s+range\s*\(/i.test(text)) scores.python += 18;

        // 3. PHP
        if (/<\?php|<\?=/i.test(text)) scores.php += 40;
        if (/\$[a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*/.test(text)) scores.php += 15;
        if (/\b(echo\s+[^;]+;|var_dump\s*\(|print_r\s*\()/i.test(text)) scores.php += 20;

        // 4. Java
        if (/public\s+class\s+\w+|public\s+static\s+void\s+main\s*\(\s*String\s*(\[\s*\]\s*\w+|\w+\s*\[\s*\])\s*\)/i.test(text)) scores.java += 35;
        if (/System\.(out|err)\.(println|print|printf)\s*\(/i.test(text)) scores.java += 30;
        if (/import\s+java\.[a-zA-Z0-9_.*]+;/i.test(text)) scores.java += 30;
        if (/@Override\b/i.test(text)) scores.java += 18;

        // 5. C#
        if (/using\s+System(\.[a-zA-Z0-9_]+)*\s*;/i.test(text)) scores.csharp += 30;
        if (/Console\.(WriteLine|Write|ReadLine)\s*\(/i.test(text)) scores.csharp += 30;
        if (/namespace\s+[a-zA-Z_]\w*(\.[a-zA-Z_]\w*)*\s*\{/i.test(text)) scores.csharp += 20;

        // 6. TypeScript vs JavaScript
        if (/:\s*(string|number|boolean|any|void|never|unknown|object|symbol|bigint)\b|interface\s+[A-Z]\w*\s*\{|type\s+[A-Z]\w*\s*=\s*|as\s+const\b|<[A-Z]\w*>\s*\(|:\s*[A-Z]\w*(\[\])?\s*(=|;|,|\))/i.test(text)) {
            scores.typescript += 25;
        }
        if (/\b(const|let|var)\s+[a-zA-Z_$]\w*\s*=/i.test(text)) {
            scores.javascript += 10;
            scores.typescript += 10;
        }
        if (/console\.(log|warn|error|info|debug)\s*\(/i.test(text)) {
            scores.javascript += 12;
            scores.typescript += 12;
        }
        if (/function\s+[a-zA-Z_$]\w*\s*\([^)]*\)\s*\{/i.test(text)) {
            scores.javascript += 10;
            scores.typescript += 10;
        }
        if (/=>\s*\{|document\.getElementById|window\.addEventListener|export\s+default\b/i.test(text)) {
            scores.javascript += 10;
            scores.typescript += 10;
        }

        // 7. Go
        if (/package\s+main\b/i.test(text)) scores.go += 30;
        if (/import\s*\(\s*["']fmt["']|import\s+["']fmt["']/i.test(text)) scores.go += 25;
        if (/func\s+(main|\([a-zA-Z0-9_* ]+\)\s*\w+|\w+)\s*\([^)]*\)/i.test(text)) scores.go += 20;
        if (/fmt\.(Println|Printf|Sprintf|Print)\s*\(/i.test(text)) scores.go += 25;
        if (/:=/.test(text)) scores.go += 15;

        // 8. Rust
        if (/fn\s+(main|[a-zA-Z_]\w*)\s*\([^)]*\)\s*(->\s*[^{]+)?\s*\{/i.test(text)) scores.rust += 25;
        if (/(println!|eprintln!|format!)\s*\(/i.test(text)) scores.rust += 30;
        if (/\b(let\s+mut\b|pub\s+fn\b|impl\b|match\s+\w+\s*\{)/i.test(text)) scores.rust += 20;

        // 9. Kotlin
        if (/fun\s+(main|[a-zA-Z_]\w*)\s*\([^)]*\)\s*(:\s*[^{]+)?\s*\{/i.test(text)) scores.kotlin += 25;

        // 10. Swift
        if (/import\s+(UIKit|Foundation|SwiftUI)/i.test(text)) scores.swift += 35;
        if (/guard\s+let\b|if\s+let\b/i.test(text)) scores.swift += 20;

        // 11. Ruby
        if (/\bputs\s+[^;]+|\bdef\s+[a-zA-Z_]\w*\s*(\([^)]*\))?\s*[\r\n]+[\s\S]*?\bend\b/i.test(text) && !/[;{}]/.test(text)) scores.ruby += 20;

        // 12. SQL
        if (/^\s*(SELECT|INSERT\s+INTO|UPDATE|DELETE\s+FROM|CREATE\s+TABLE|ALTER\s+TABLE|DROP\s+TABLE)\b/im.test(text)) scores.sql += 35;

        // 13. Dart
        if (/void\s+main\s*\(\s*\)\s*\{|import\s+['"]package:flutter/i.test(text)) scores.dart += 30;

        // 14. R
        if (/<-|library\s*\([a-zA-Z_]\w*\)|ggplot\s*\(/i.test(text)) scores.r += 25;

        // 15. Scala
        if (/object\s+[A-Z]\w*(\s+extends\s+App)?\s*\{|def\s+main\s*\(/i.test(text)) scores.scala += 30;

        let bestLang = null;
        let maxScore = 0;
        for (const [lang, score] of Object.entries(scores)) {
            if (score > maxScore) {
                maxScore = score;
                bestLang = lang;
            }
        }
        return maxScore > 0 ? bestLang : null;
    }
});
