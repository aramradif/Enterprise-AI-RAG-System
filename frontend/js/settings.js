export function renderSettingsView(workspace) {
    workspace.innerHTML = `
        <section class="settings-view">
            <div class="page-heading">
                <h2>Platform Settings</h2>
                <p>
                    Review the current AI configuration, knowledge base,
                    conversation features, evaluation tools, and platform status.
                </p>
            </div>

            <div class="settings-grid">
                <div class="settings-card">
                    <h3>AI Configuration</h3>

                    <div class="setting-row">
                        <span>Model</span>
                        <strong>GPT-4o-mini</strong>
                    </div>

                    <div class="setting-row">
                        <span>Streaming</span>
                        <strong>Enabled</strong>
                    </div>

                    <div class="setting-row">
                        <span>Temperature</span>
                        <strong>0.7</strong>
                    </div>

                    <div class="setting-row">
                        <span>Top-K Retrieval</span>
                        <strong>3</strong>
                    </div>
                </div>

                <div class="settings-card">
                    <h3>Knowledge Base</h3>

                    <div class="setting-row">
                        <span>Vector Database</span>
                        <strong>ChromaDB</strong>
                    </div>

                    <div class="setting-row">
                        <span>Embedding Model</span>
                        <strong>text-embedding-3-small</strong>
                    </div>

                    <div class="setting-row">
                        <span>Document Types</span>
                        <strong>PDF, DOCX, TXT, MD</strong>
                    </div>
                </div>

                <div class="settings-card">
                    <h3>Conversation</h3>

                    <div class="setting-row">
                        <span>Conversation Memory</span>
                        <strong>Enabled</strong>
                    </div>

                    <div class="setting-row">
                        <span>Session History</span>
                        <strong>Enabled</strong>
                    </div>

                    <div class="setting-row">
                        <span>AI Summaries</span>
                        <strong>Enabled</strong>
                    </div>
                </div>

                <div class="settings-card">
                    <h3>Evaluation & Observability</h3>

                    <div class="setting-row">
                        <span>Evaluation Metrics</span>
                        <strong>Enabled</strong>
                    </div>

                    <div class="setting-row">
                        <span>Request Logging</span>
                        <strong>Enabled</strong>
                    </div>

                    <div class="setting-row">
                        <span>Cost Tracking</span>
                        <strong>Enabled</strong>
                    </div>
                </div>

                <div class="settings-card">
                    <h3>Platform Information</h3>

                    <div class="setting-row">
                        <span>Platform Version</span>
                        <strong>v1.9.0</strong>
                    </div>

                    <div class="setting-row">
                        <span>Backend</span>
                        <strong>FastAPI</strong>
                    </div>

                    <div class="setting-row">
                        <span>Environment</span>
                        <strong>Development</strong>
                    </div>
                </div>
            </div>
        </section>
    `;
}