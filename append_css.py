import os

css_code = """
/* Core Insights Article Styling */
.insight-article {
    margin: 40px auto 80px;
    max-width: 800px;
    font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Pretendard Variable", Pretendard, Roboto, "Noto Sans KR", "Segoe UI", "Malgun Gothic", "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", sans-serif;
    color: var(--text);
}

.insight-intro {
    font-size: 22px;
    line-height: 1.6;
    color: var(--text);
    margin-bottom: 60px;
    padding-bottom: 40px;
    border-bottom: 2px solid var(--border);
    word-break: keep-all;
}

.insight-intro strong {
    color: var(--ember);
    font-weight: 800;
}

.insight-h2 {
    font-size: 26px;
    font-weight: 800;
    margin: 60px 0 24px;
    color: var(--text);
    letter-spacing: -0.02em;
    padding-left: 14px;
    border-left: 4px solid var(--ember);
}

.insight-p {
    font-size: 16px;
    line-height: 1.7;
    color: var(--text-dim);
    margin-bottom: 24px;
    word-break: keep-all;
}

.insight-box {
    background: var(--surface);
    border-radius: 16px;
    padding: 24px 30px;
    margin-bottom: 30px;
    border: 1px solid var(--border);
    font-size: 15px;
    line-height: 1.6;
    color: var(--text-dim);
}

.highlight-box {
    background: rgba(82, 183, 136, 0.03);
    border: 1px solid rgba(82, 183, 136, 0.2);
}

.highlight-box strong {
    color: var(--accent);
}

.quote-text {
    font-size: 24px;
    font-weight: 800;
    color: var(--text);
    margin: 16px 0;
    letter-spacing: -0.01em;
}

.ascii-art-box {
    background: #0f172a;
    border-radius: 16px;
    padding: 30px;
    margin: 40px 0;
    color: #e2e8f0;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
    position: relative;
    overflow: hidden;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
}

.ascii-title {
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #64748b;
    margin-bottom: 16px;
    font-weight: 700;
    font-family: -apple-system, sans-serif;
}

.ascii-art-box pre {
    margin: 0;
    font-size: 16px;
    line-height: 1.4;
    color: #38bdf8;
    white-space: pre-wrap;
}

.ascii-footer {
    margin-top: 20px;
    padding-top: 16px;
    border-top: 1px dashed #334155;
    font-size: 13px;
    color: #94a3b8;
    font-family: -apple-system, sans-serif;
}

.example-group {
    background: rgba(255,255,255,0.015);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 40px;
    border-left: 3px solid var(--accent);
}

.ex-en {
    font-size: 20px;
    font-weight: 800;
    color: var(--text);
    margin-bottom: 6px;
}

.ex-ko {
    font-size: 14px;
    color: var(--text-dim);
}

.flow-box {
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--surface);
    padding: 20px;
    border-radius: 12px;
    border: 1px solid var(--border);
    font-size: 16px;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 40px;
    letter-spacing: 0.05em;
    text-align: center;
}

.compare-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    margin-bottom: 40px;
}

@media (max-width: 600px) {
    .compare-grid {
        grid-template-columns: 1fr;
    }
}

.compare-col {
    background: var(--surface);
    padding: 24px;
    border-radius: 16px;
    border: 1px solid var(--border);
}

.c-title {
    font-size: 18px;
    font-weight: 800;
    color: var(--text);
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border);
}

.compare-col p {
    font-size: 14px;
    color: var(--text-dim);
    line-height: 1.6;
    margin-bottom: 12px;
}

.compare-col p strong {
    color: var(--text);
    display: block;
    margin-bottom: 2px;
    font-size: 15px;
}

.c-tag {
    display: inline-block;
    padding: 6px 12px;
    background: rgba(255,255,255,0.05);
    border-radius: 6px;
    font-size: 12px;
    font-weight: 700;
    color: var(--accent);
    margin-top: 8px;
    margin-right: 8px;
}

.insight-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 40px;
    background: var(--surface);
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid var(--border);
}

.insight-table th {
    background: rgba(255,255,255,0.03);
    padding: 16px;
    text-align: left;
    font-size: 14px;
    color: var(--text-dim);
    font-weight: 700;
    border-bottom: 1px solid var(--border);
}

.insight-table td {
    padding: 16px;
    font-size: 15px;
    color: var(--text);
    border-bottom: 1px solid var(--border);
}

.insight-table tr:last-child td {
    border-bottom: none;
}

.summary-list {
    list-style: none;
    padding: 0;
    margin: 20px 0 0 0;
}

.summary-list li {
    font-size: 15px;
    color: var(--text-dim);
    margin-bottom: 8px;
}

.summary-list li strong {
    color: var(--text);
    font-size: 16px;
}
"""

with open('index.css', 'a', encoding='utf-8') as f:
    f.write(css_code)
