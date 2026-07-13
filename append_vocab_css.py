import os

css_code = """
/* Vocabulary Footnotes */
.vocab-notes {
    margin-top: 24px;
    margin-bottom: 40px;
    padding: 20px 24px;
    background: rgba(255, 255, 255, 0.02);
    border-top: 1px dashed var(--border);
    border-radius: 0 0 16px 16px;
}

.vocab-title {
    font-size: 13px;
    font-weight: 800;
    color: var(--ember);
    margin-bottom: 12px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.vocab-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-wrap: wrap;
    gap: 12px 24px;
}

.vocab-list li {
    font-size: 14px;
    color: var(--text-dim);
}

.vocab-list li strong {
    color: var(--text);
    font-weight: 700;
    margin-right: 4px;
}
"""

with open('index.css', 'a', encoding='utf-8') as f:
    f.write(css_code)
