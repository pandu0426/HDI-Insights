/* ==========================================================================
   HDI INSIGHT AI - COMPLETE SPA FRONT-END CONTROLLER (V2.1.0)
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Preset country profiles
    const countryPresets = {
        switzerland: { Name: "Switzerland", life: 83.9, expected: 16.5, mean: 13.9, gni: 69600 },
        norway: { Name: "Norway", life: 83.2, expected: 18.0, mean: 13.0, gni: 66100 },
        singapore: { Name: "Singapore", life: 83.5, expected: 16.4, mean: 11.9, gni: 90000 },
        united_states: { Name: "United States", life: 77.2, expected: 16.3, mean: 13.4, gni: 64700 },
        china: { Name: "China", life: 78.2, expected: 14.2, mean: 8.1, gni: 17500 },
        brazil: { Name: "Brazil", life: 72.8, expected: 15.6, mean: 8.1, gni: 14600 },
        egypt: { Name: "Egypt", life: 70.2, expected: 13.8, mean: 7.4, gni: 12000 },
        india: { Name: "India", life: 67.2, expected: 11.9, mean: 6.7, gni: 6590 },
        vietnam: { Name: "Vietnam", life: 73.6, expected: 13.0, mean: 8.4, gni: 7900 },
        sierra_leone: { Name: "Sierra Leone", life: 60.1, expected: 9.5, mean: 3.5, gni: 1600 },
        niger: { Name: "Niger", life: 62.1, expected: 7.0, mean: 2.1, gni: 1200 },
        central_african: { Name: "Central African Republic", life: 53.9, expected: 8.0, mean: 4.3, gni: 960 },
        japan: { Name: "Japan", life: 84.8, expected: 15.2, mean: 12.8, gni: 42200 },
        germany: { Name: "Germany", life: 80.8, expected: 17.0, mean: 14.1, gni: 54500 },
        australia: { Name: "Australia", life: 83.2, expected: 21.0, mean: 12.7, gni: 49200 },
        nepal: { Name: "Nepal", life: 69.0, expected: 12.2, mean: 5.1, gni: 3850 },
        bangladesh: { Name: "Bangladesh", life: 72.4, expected: 12.4, mean: 6.2, gni: 5490 },
        nigeria: { Name: "Nigeria", life: 52.7, expected: 9.8, mean: 5.2, gni: 4800 },
        south_africa: { Name: "South Africa", life: 62.3, expected: 13.6, mean: 10.2, gni: 12900 }
    };

    // Collection of 30 HDI facts
    const hdiFacts = [
        "HDI evaluates health, education, and income together rather than economic growth alone.",
        "The index was developed by Pakistani economist Mahbub ul Haq and Indian economist Amartya Sen.",
        "Expected schooling represents years a child of school entrance age can expect to spend at school.",
        "Mean schooling is the average number of education years completed by a country's adult population.",
        "GNI per capita represents total national wealth divided by the midyear population.",
        "A logarithmic transformation is applied to GNI per capita because the value of income diminishes as countries get richer.",
        "Countries with HDI scores above 0.800 are categorized as having Very High human development.",
        "Sub-Saharan Africa has seen some of the fastest improvements in HDI scores since 1990.",
        "Life expectancy at birth of 80+ years is typical for countries in the Very High HDI tier.",
        "Norway, Switzerland, and Ireland consistently rank near the top of the global HDI table.",
        "Gender Inequality Index (GII) is a separate UNDP measure tracking disparities between men and women.",
        "HDI scores range from 0.000 (minimum development) to 1.000 (maximum development).",
        "Education scores are calculated as the arithmetic mean of expected and mean schooling.",
        "Imputing country-specific medians prevents dropping records that have partial missing entries.",
        "Outliers are data points that lie far outside the range of standard observations.",
        "A StandardScaler centers feature variables to have zero mean and unit variance.",
        "Support Vector Machines use hyperplanes to separate category boundaries in multi-dimensional space.",
        "Random Forests combine multiple decision trees to produce robust, generalized predictions.",
        "In machine learning, stratification keeps category ratios balanced in train and test splits.",
        "Pearson correlation measures the strength of linear relationships between indicators.",
        "Logarithmic scales are highly useful when graphing indicators with extreme ranges like GNI.",
        "Logistic regression predicts categorical probabilities using sigmoid mathematical functions.",
        "An F1-score balances precision and recall to evaluate classifier reliability.",
        "Confusion matrices show true versus predicted classification errors in table formats.",
        "Intelligent advisors recommend targeted solutions based on lagging country features.",
        "Feature selection filters columns that are highly correlated with target outcomes.",
        "KNN classifiers assign categories based on the closest records in the training set.",
        "ReportLab generates compiled, printable PDF reports directly in python streams.",
        "Live simulation sliders send asynchronous REST requests to Flask without reloading pages.",
        "The Inequality-adjusted Human Development Index (IHDI) discounts HDI values based on inequality."
    ];

    // Global state
    let activeCharts = {};
    let dsCurrentPage = 1;
    const dsPerPage = 12;
    let cachedHistoryRecords = [];

    // Toast Alert Helper
    function showToast(message, type = 'success') {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        container.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
    }

    // 2. Light & Dark Mode Controller
    const themeToggleBtn = document.getElementById('btn-theme-toggle');
    const sunIcon = themeToggleBtn.querySelector('.sun-icon');
    const moonIcon = themeToggleBtn.querySelector('.moon-icon');

    function getChartThemeColors() {
        const isDark = document.body.classList.contains('dark-theme');
        return {
            textColor: isDark ? '#9ca3af' : '#475569',
            gridColor: isDark ? '#1f2937' : '#e2e8f0',
            barBgA: 'rgba(99, 102, 241, 0.8)',
            barBgB: 'rgba(13, 148, 136, 0.8)'
        };
    }

    function toggleTheme() {
        const body = document.body;
        const isDark = body.classList.contains('dark-theme');
        
        if (isDark) {
            body.classList.remove('dark-theme');
            sunIcon.classList.remove('hidden');
            moonIcon.classList.add('hidden');
            localStorage.setItem('theme', 'light');
            showToast("Light Mode Enabled");
        } else {
            body.classList.add('dark-theme');
            sunIcon.classList.add('hidden');
            moonIcon.classList.remove('hidden');
            localStorage.setItem('theme', 'dark');
            showToast("Dark Mode Enabled");
        }

        // Re-render currently visible charts to adapt colors
        const activePanel = document.querySelector('.panel.active');
        if (activePanel) {
            if (activePanel.id === 'panel-home') {
                renderHomeDistributionChart();
            } else if (activePanel.id === 'panel-model-performance') {
                loadModelPerformance();
            } else if (activePanel.id === 'panel-comparison') {
                runComparison();
            } else if (activePanel.id === 'panel-trend') {
                runTrendProjection();
            }
        }
    }

    themeToggleBtn.addEventListener('click', toggleTheme);

    // Initial Theme Load
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
        sunIcon.classList.add('hidden');
        moonIcon.classList.remove('hidden');
    }

    // 3. SPA Navigation Control
    const menuItems = document.querySelectorAll('.menu-item');
    const panels = document.querySelectorAll('.panel');
    const pageHeaderTitle = document.getElementById('page-header-title');

    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            const targetPanel = item.getAttribute('data-target');
            switchPanel(targetPanel, item.querySelector('span').textContent);
        });
    });

    function switchPanel(panelId, labelText) {
        // Toggle active menu highlight
        menuItems.forEach(m => {
            if (m.getAttribute('data-target') === panelId) {
                m.classList.add('active');
            } else {
                m.classList.remove('active');
            }
        });

        // Toggle panels
        panels.forEach(p => {
            if (p.id === panelId) {
                p.classList.add('active');
            } else {
                p.classList.remove('active');
            }
        });

        pageHeaderTitle.textContent = labelText;

        // Trigger data loads
        if (panelId === 'panel-home') {
            loadDashboardHome();
        } else if (panelId === 'panel-explorer') {
            loadDatasetExplorer();
        } else if (panelId === 'panel-model-performance') {
            loadModelPerformance();
        } else if (panelId === 'panel-history') {
            loadHistory();
        } else if (panelId === 'panel-comparison') {
            runComparison();
        } else if (panelId === 'panel-trend') {
            runTrendProjection();
        }

        // Close sidebar on mobile
        document.querySelector('.app-layout').classList.remove('sidebar-open');
    }

    // Mobile Sidebar toggle
    const toggleBtn = document.getElementById('btn-sidebar-toggle');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            document.querySelector('.app-layout').classList.toggle('sidebar-open');
        });
    }

    // Close sidebar on click outside
    document.addEventListener('click', (e) => {
        const layout = document.querySelector('.app-layout');
        if (layout.classList.contains('sidebar-open') && !e.target.closest('.sidebar') && !e.target.closest('.sidebar-toggle')) {
            layout.classList.remove('sidebar-open');
        }
    });

    // 4. Bidirectional Sliders Synchronization for Simulator
    const simulatorInputs = [
        { slider: 'slider-life', num: 'Life_Expectancy' },
        { slider: 'slider-expected', num: 'Expected_Schooling' },
        { slider: 'slider-mean', num: 'Mean_Schooling' },
        { slider: 'slider-gni', num: 'GNI_Per_Capita' }
    ];

    simulatorInputs.forEach(pair => {
        const slider = document.getElementById(pair.slider);
        const num = document.getElementById(pair.num);

        slider.addEventListener('input', () => {
            num.value = slider.value;
            runLivePrediction();
        });

        num.addEventListener('input', () => {
            slider.value = num.value;
            runLivePrediction();
        });
    });

    // Presets dropdown loader
    const presetSelect = document.getElementById('country-preset');
    presetSelect.addEventListener('change', () => {
        const key = presetSelect.value;
        loadProfileValues(key);
    });

    function loadProfileValues(key, runPredict = true) {
        if (!key || !countryPresets[key]) return;
        
        const data = countryPresets[key];
        document.getElementById('Country').value = data.Name;
        
        document.getElementById('slider-life').value = data.life;
        document.getElementById('Life_Expectancy').value = data.life;
        
        document.getElementById('slider-expected').value = data.expected;
        document.getElementById('Expected_Schooling').value = data.expected;
        
        document.getElementById('slider-mean').value = data.mean;
        document.getElementById('Mean_Schooling').value = data.mean;
        
        document.getElementById('slider-gni').value = data.gni;
        document.getElementById('GNI_Per_Capita').value = data.gni;

        if (runPredict) runLivePrediction();
    }

    // Reset Form button
    document.getElementById('btn-reset-form').addEventListener('click', () => {
        presetSelect.value = "";
        document.getElementById('Country').value = "Custom Country";
        
        document.getElementById('slider-life').value = 70.0;
        document.getElementById('Life_Expectancy').value = 70.0;
        
        document.getElementById('slider-expected').value = 12.0;
        document.getElementById('Expected_Schooling').value = 12.0;
        
        document.getElementById('slider-mean').value = 8.0;
        document.getElementById('Mean_Schooling').value = 8.0;
        
        document.getElementById('slider-gni').value = 15000;
        document.getElementById('GNI_Per_Capita').value = 15000;

        runLivePrediction();
    });

    // Run Analysis button manual trigger
    document.getElementById('btn-trigger-prediction').addEventListener('click', () => {
        runLivePrediction(true);
    });

    // Circular Confidence Gauge Animator
    function setConfidenceGauge(val) {
        const circle = document.getElementById('c-gauge-fill');
        const pctEl = document.getElementById('res-confidence-pct');
        const lblEl = document.getElementById('res-confidence-lbl');
        
        // Circumference of r=40 is 251.2
        const circ = 251.2;
        const offset = circ - (circ * val / 100);
        
        circle.style.strokeDashoffset = offset;
        pctEl.textContent = `${val.toFixed(0)}%`;
        
        // Define color and label based on threshold
        let color = '#dc2626'; // low (Red)
        let label = 'Low Confidence';
        
        if (val >= 80) {
            color = '#059669'; // high (Green)
            label = 'High Confidence';
        } else if (val >= 50) {
            color = '#d97706'; // medium (Orange)
            label = 'Medium Confidence';
        }
        
        circle.style.stroke = color;
        lblEl.textContent = label;
        lblEl.style.color = color;
    }

    // "Did You Know?" Fact Selector
    function showRandomFact() {
        const factText = document.getElementById('hdi-fact-text');
        const idx = Math.floor(Math.random() * hdiFacts.length);
        factText.textContent = hdiFacts[idx];
    }

    // Core Live Predict Execution
    let predictTimeout;
    function runLivePrediction(showAlert = false) {
        clearTimeout(predictTimeout);
        predictTimeout = setTimeout(() => {
            const country = document.getElementById('Country').value;
            const le = parseFloat(document.getElementById('Life_Expectancy').value);
            const eys = parseFloat(document.getElementById('Expected_Schooling').value);
            const mys = parseFloat(document.getElementById('Mean_Schooling').value);
            const gni = parseFloat(document.getElementById('GNI_Per_Capita').value);

            if (isNaN(le) || isNaN(eys) || isNaN(mys) || isNaN(gni)) {
                if (showAlert) showToast("Invalid numeric values.", "error");
                return;
            }

            fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    Country: country,
                    Life_Expectancy: le,
                    Expected_Schooling: eys,
                    Mean_Schooling: mys,
                    GNI_Per_Capita: gni
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    // Update outputs
                    document.getElementById('res-score').textContent = data.prediction.toFixed(3);
                    document.getElementById('res-score-bar').style.width = `${data.prediction * 100}%`;
                    
                    // Circular Gauge Confidence update
                    setConfidenceGauge(data.confidence);
                    
                    const badge = document.getElementById('res-badge');
                    badge.textContent = data.category;
                    
                    // Explanation
                    document.getElementById('res-explanation').innerHTML = data.explanation;
                    
                    // Indicators
                    const posUl = document.getElementById('res-pos-indicators');
                    posUl.innerHTML = "";
                    data.pos_indicators.forEach(i => {
                        const li = document.createElement('li');
                        li.innerHTML = `<span>✓</span> ${i}`;
                        posUl.appendChild(li);
                    });

                    const weakUl = document.getElementById('res-weak-indicators');
                    weakUl.innerHTML = "";
                    data.weak_indicators.forEach(i => {
                        const li = document.createElement('li');
                        li.innerHTML = `<span>⚠</span> ${i}`;
                        weakUl.appendChild(li);
                    });

                    // Recommendations
                    const recsBox = document.getElementById('res-recommendations');
                    recsBox.innerHTML = "";
                    data.recommendations.forEach(r => {
                        const item = document.createElement('div');
                        item.className = "rec-item";
                        item.innerHTML = `
                            <div class="rec-icon">⚡</div>
                            <div class="rec-text">${r}</div>
                        `;
                        recsBox.appendChild(item);
                    });

                    // Show Random Fact
                    showRandomFact();

                    // Adapt dynamic theme class on body
                    document.body.className = `${savedTheme === 'dark' ? 'dark-theme' : ''} theme-${data.category.toLowerCase().replace(' ', '-')}`;
                    
                    if (showAlert) showToast("Analysis updated successfully.");
                } else {
                    if (showAlert) showToast(data.error, "error");
                }
            })
            .catch(err => {
                console.error(err);
                if (showAlert) showToast("Network error running prediction.", "error");
            });
        }, 300);
    }

    // 5. Download PDF Action
    document.getElementById('btn-download-pdf').addEventListener('click', () => {
        const country = document.getElementById('Country').value;
        const le = document.getElementById('Life_Expectancy').value;
        const eys = document.getElementById('Expected_Schooling').value;
        const mys = document.getElementById('Mean_Schooling').value;
        const gni = document.getElementById('GNI_Per_Capita').value;
        
        const params = new URLSearchParams({
            Country: country,
            Life_Expectancy: le,
            Expected_Schooling: eys,
            Mean_Schooling: mys,
            GNI_Per_Capita: gni
        });
        
        window.open(`/download_report?${params.toString()}`);
    });



    // 7. Dashboard Home Loader
    function loadDashboardHome() {
        fetch(`/dataset?page=1&per_page=1`)
        .then(res => res.json())
        .then(data => {
            if (data.success && data.insights) {
                const ins = data.insights;
                document.getElementById('kpi-countries').textContent = ins.total_countries;
                document.getElementById('kpi-life').textContent = ins.average_life_expectancy;
                document.getElementById('kpi-hdi').textContent = ins.average_hdi.toFixed(3);
                document.getElementById('kpi-gni').textContent = ins.median_gni.toLocaleString();
                
                document.getElementById('ins-max-gni-country').textContent = ins.highest_gni.country;
                document.getElementById('ins-max-gni-val').textContent = `$${ins.highest_gni.val.toLocaleString()}`;
                
                document.getElementById('ins-max-edu-country').textContent = ins.highest_education.country;
                document.getElementById('ins-max-edu-val').textContent = ins.highest_education.val;
                
                document.getElementById('ins-best-country').textContent = ins.best_indicators.country;
                document.getElementById('ins-best-val').textContent = ins.best_indicators.val.toFixed(3);
                
                document.getElementById('ins-worst-country').textContent = ins.lowest_indicators.country;
                document.getElementById('ins-worst-val').textContent = ins.lowest_indicators.val.toFixed(3);
                
                // Draw Global Category Distribution Chart
                renderHomeDistributionChart();
            }
        });
    }

    function renderHomeDistributionChart() {
        if (activeCharts['home-dist']) {
            activeCharts['home-dist'].destroy();
        }
        
        const colors = getChartThemeColors();
        const ctx = document.getElementById('chart-home-distribution').getContext('2d');
        activeCharts['home-dist'] = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Very High Development', 'High Development', 'Medium Development', 'Low Development'],
                datasets: [{
                    data: [35, 25, 20, 20],
                    backgroundColor: ['#2563eb', '#059669', '#d97706', '#dc2626'],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: colors.textColor }
                    }
                }
            }
        });
    }

    // 8. Dataset Explorer Loader
    function loadDatasetExplorer() {
        const search = document.getElementById('ds-search').value;
        const cat = document.getElementById('ds-category-filter').value;
        
        fetch(`/dataset?page=${dsCurrentPage}&per_page=${dsPerPage}&search=${search}&category=${cat}`)
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                const tbody = document.getElementById('dataset-table-body');
                tbody.innerHTML = "";
                
                data.rows.forEach(r => {
                    const tr = document.createElement('tr');
                    const catMap = { 0: 'Low', 1: 'Medium', 2: 'High', 3: 'Very High' };
                    const catLabel = catMap[r.HDI_Category] || 'Unknown';
                    const catBadgeClass = catLabel.toLowerCase().replace(' ', '-');
                    
                    tr.innerHTML = `
                        <td><strong>${r.Country}</strong></td>
                        <td>${r.Year}</td>
                        <td class="text-right">${r.Life_Expectancy.toFixed(1)}</td>
                        <td class="text-right">${r.Expected_Schooling.toFixed(1)}</td>
                        <td class="text-right">${r.Mean_Schooling.toFixed(1)}</td>
                        <td class="text-right">$${r.GNI_Per_Capita.toLocaleString()}</td>
                        <td class="text-right"><span class="badge badge-${catBadgeClass}">${r.HDI.toFixed(3)} (${catLabel})</span></td>
                    `;
                    tbody.appendChild(tr);
                });
                
                const pag = data.pagination;
                document.getElementById('ds-pag-info').textContent = 
                    `Showing rows ${((pag.current_page - 1) * pag.per_page) + 1} - ${Math.min(pag.current_page * pag.per_page, pag.total_rows)} of ${pag.total_rows}`;
                
                document.getElementById('btn-ds-prev').disabled = pag.current_page === 1;
                document.getElementById('btn-ds-next').disabled = pag.current_page === pag.total_pages;
            }
        });
    }

    document.getElementById('btn-apply-ds-filters').addEventListener('click', () => {
        dsCurrentPage = 1;
        loadDatasetExplorer();
    });

    document.getElementById('btn-ds-prev').addEventListener('click', () => {
        if (dsCurrentPage > 1) {
            dsCurrentPage--;
            loadDatasetExplorer();
        }
    });

    document.getElementById('btn-ds-next').addEventListener('click', () => {
        dsCurrentPage++;
        loadDatasetExplorer();
    });

    // 9. Model Performance Page Loader
    function loadModelPerformance() {
        fetch('/model_stats')
        .then(res => res.json())
        .then(data => {
            if (data.success && data.stats) {
                const stats = data.stats;
                
                // Renders Active Model Stats KPIs
                document.getElementById('perf-kpi-best').textContent = stats.best_model;
                document.getElementById('perf-kpi-train-size').textContent = stats.dataset_sizes.train_size.toLocaleString();
                document.getElementById('perf-kpi-test-size').textContent = stats.dataset_sizes.test_size.toLocaleString();
                document.getElementById('perf-kpi-file-size').textContent = stats.models[stats.best_model].file_size_kb.toFixed(1);
                
                // Speed Benchmarks
                document.getElementById('perf-kpi-train-time').textContent = stats.models[stats.best_model].training_time_s.toFixed(4);
                document.getElementById('perf-kpi-pred-time').textContent = stats.models[stats.best_model].prediction_time_s.toFixed(4);
                
                // Populate Table
                const tbody = document.getElementById('model-comparison-table-body');
                tbody.innerHTML = "";
                
                const labels = [];
                const accuracies = [];
                const f1Scores = [];
                
                Object.keys(stats.models).forEach(name => {
                    const m = stats.models[name];
                    const isBest = name === stats.best_model ? "<strong>(Active Best)</strong>" : "";
                    
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td><strong>${name}</strong> ${isBest}</td>
                        <td class="text-right">${(m.accuracy * 100).toFixed(1)}%</td>
                        <td class="text-right">${(m.precision * 100).toFixed(1)}%</td>
                        <td class="text-right">${(m.recall * 100).toFixed(1)}%</td>
                        <td class="text-right">${(m.f1_score * 100).toFixed(1)}%</td>
                    `;
                    tbody.appendChild(tr);
                    
                    labels.push(name);
                    accuracies.push(m.accuracy * 100);
                    f1Scores.push(m.f1_score * 100);
                });
                
                // Renders Bar Chart Comparison
                renderPerformanceChart(labels, accuracies, f1Scores);
                
                // Renders Feature Importance Radar
                renderFeatureImportanceChart(stats.feature_importances);
                
                // Render Confusion Matrix
                const bestModelData = stats.models[stats.best_model];
                if (bestModelData && bestModelData.confusion_matrix) {
                    renderConfusionMatrix(bestModelData.confusion_matrix, stats.class_names);
                }

                // Render Algorithm Cards
                renderAlgorithmCards(stats.models, stats.best_model);
            }
        });
    }

    function renderPerformanceChart(labels, accuracies, f1Scores) {
        if (activeCharts['perf']) {
            activeCharts['perf'].destroy();
        }
        const colors = getChartThemeColors();
        const ctx = document.getElementById('chart-model-accuracy').getContext('2d');
        activeCharts['perf'] = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Accuracy (%)',
                        data: accuracies,
                        backgroundColor: 'rgba(79, 70, 229, 0.7)',
                        borderColor: '#4f46e5',
                        borderWidth: 1
                    },
                    {
                        label: 'F1 Score (%)',
                        data: f1Scores,
                        backgroundColor: 'rgba(13, 148, 136, 0.7)',
                        borderColor: '#0d9488',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { labels: { color: colors.textColor } }
                },
                scales: {
                    x: { ticks: { color: colors.textColor }, grid: { color: colors.gridColor } },
                    y: { min: 80, max: 100, ticks: { color: colors.textColor }, grid: { color: colors.gridColor } }
                }
            }
        });
    }

    function renderFeatureImportanceChart(importances) {
        if (activeCharts['feat-imp']) {
            activeCharts['feat-imp'].destroy();
        }
        
        const colors = getChartThemeColors();
        const labels = Object.keys(importances).map(l => l.replace('_', ' '));
        const values = Object.values(importances).map(v => v * 100);
        
        const ctx = document.getElementById('chart-feature-importance').getContext('2d');
        activeCharts['feat-imp'] = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Relative Predictive Power (%)',
                    data: values,
                    backgroundColor: 'rgba(79, 70, 229, 0.2)',
                    borderColor: '#4f46e5',
                    pointBackgroundColor: '#4f46e5',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { labels: { color: colors.textColor } }
                },
                scales: {
                    r: { 
                        max: 100, 
                        min: 0, 
                        grid: { color: colors.gridColor }, 
                        angleLines: { color: colors.gridColor },
                        pointLabels: { color: colors.textColor }
                    }
                }
            }
        });
    }

    function renderConfusionMatrix(matrix, classes) {
        const grid = document.getElementById('confusion-matrix-grid');
        grid.innerHTML = "";
        
        const space = document.createElement('div');
        space.className = "cm-cell cm-header";
        space.textContent = "Act \\ Pred";
        grid.appendChild(space);
        
        classes.forEach(c => {
            const h = document.createElement('div');
            h.className = "cm-cell cm-header";
            h.textContent = c;
            grid.appendChild(h);
        });
        
        matrix.forEach((row, i) => {
            const rowLabel = document.createElement('div');
            rowLabel.className = "cm-cell cm-header";
            rowLabel.textContent = classes[i];
            grid.appendChild(rowLabel);
            
            row.forEach((val, j) => {
                const cell = document.createElement('div');
                cell.className = `cm-cell cm-value ${i === j ? 'cm-diag' : ''}`;
                cell.textContent = val;
                grid.appendChild(cell);
            });
        });
    }

    function renderAlgorithmCards(modelsData, bestModel) {
        const grid = document.getElementById('algorithm-cards-grid');
        grid.innerHTML = "";

        const descriptions = {
            'Logistic Regression': 'A linear classification model that estimates the probability of category classes using logistic functions.',
            'Decision Tree': 'A tree-structured classifier where leaf nodes represent classifications and branches represent splits.',
            'Random Forest': 'An ensemble model fitting multiple decision trees to yield robust average votes.',
            'Support Vector Machine': 'Finds hyperplanes in multi-dimensional space to maximize boundaries between development categories.',
            'K-Nearest Neighbors': 'Assigns developmental categories based on proximity to nearest training records.'
        };

        const configSettings = {
            'Logistic Regression': 'max_iter=1000, multi_class=multinomial',
            'Decision Tree': 'criterion=gini, random_state=42',
            'Random Forest': 'n_estimators=100, random_state=42',
            'Support Vector Machine': 'C=1.0, kernel=rbf, probability=True',
            'K-Nearest Neighbors': 'n_neighbors=5, weights=uniform'
        };

        Object.keys(modelsData).forEach(name => {
            const m = modelsData[name];
            const isBest = name === bestModel;
            
            const card = document.createElement('div');
            card.className = `algo-card ${isBest ? 'recommended-best' : ''}`;
            card.innerHTML = `
                ${isBest ? '<span class="algo-badge">Active Best</span>' : ''}
                <h3>${name}</h3>
                <p class="text-xs text-secondary mb-12">${descriptions[name] || ''}</p>
                
                <div class="metric-bar-group">
                    <div class="metric-bar-label">
                        <span>Accuracy Score</span>
                        <span>${(m.accuracy * 100).toFixed(1)}%</span>
                    </div>
                    <div class="progress-bar-container">
                        <div class="progress-bar-fill" style="width: ${m.accuracy * 100}%"></div>
                    </div>
                </div>
                
                <div class="metric-bar-group">
                    <div class="metric-bar-label">
                        <span>F1 Score (Weighted)</span>
                        <span>${(m.f1_score * 100).toFixed(1)}%</span>
                    </div>
                    <div class="progress-bar-container">
                        <div class="progress-bar-fill accent" style="width: ${m.f1_score * 100}%"></div>
                    </div>
                </div>

                <div class="algo-stats-row">
                    <span>Train Time: ${m.training_time_s.toFixed(4)}s</span>
                    <span>Size: ${m.file_size_kb.toFixed(1)} KB</span>
                </div>
                <div class="text-xs text-muted mt-5" style="border-top: 1px dashed var(--border-color); padding-top: 6px; font-family: monospace;">
                    Params: ${configSettings[name]}
                </div>
            `;
            grid.appendChild(card);
        });
    }

    // 10. History Log Loader
    function loadHistory() {
        const search = document.getElementById('hist-search').value;
        const category = document.getElementById('hist-category-filter').value;
        const sort = document.getElementById('hist-sort').value;
        
        const params = new URLSearchParams({
            search: search,
            category: category,
            sort_by: sort
        });
        
        fetch(`/history?${params.toString()}`)
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                cachedHistoryRecords = data.records; // cache for CSV export
                const tbody = document.getElementById('history-table-body');
                tbody.innerHTML = "";
                
                data.records.forEach(r => {
                    const tr = document.createElement('tr');
                    const badgeClass = r.predicted_category.toLowerCase().replace(' ', '-');
                    
                    tr.innerHTML = `
                        <td>${r.timestamp}</td>
                        <td><strong>${r.country}</strong></td>
                        <td class="text-right">${r.life_expectancy.toFixed(1)}</td>
                        <td class="text-right">${r.mean_schooling.toFixed(1)} / ${r.expected_schooling.toFixed(1)}</td>
                        <td class="text-right">$${r.gni_per_capita.toLocaleString()}</td>
                        <td class="text-right"><span class="badge badge-${badgeClass}">${r.hdi_score.toFixed(3)} (${r.predicted_category})</span></td>
                        <td class="text-right">${r.prediction_confidence.toFixed(1)}%</td>
                        <td class="text-center">
                            <button class="btn btn-secondary btn-sm delete-hist-btn" data-id="${r.id}">Delete</button>
                        </td>
                    `;
                    tbody.appendChild(tr);
                });
                
                // Add delete handlers
                document.querySelectorAll('.delete-hist-btn').forEach(btn => {
                    btn.addEventListener('click', (e) => {
                        const id = e.target.getAttribute('data-id');
                        if (confirm("Are you sure you want to delete this prediction from log history?")) {
                            fetch(`/history/delete/${id}`, { method: 'POST' })
                            .then(res => res.json())
                            .then(d => {
                                if (d.success) {
                                    showToast("Record deleted.");
                                    loadHistory();
                                }
                            });
                        }
                    });
                });
            }
        });
    }

    document.getElementById('hist-search').addEventListener('input', loadHistory);
    document.getElementById('hist-category-filter').addEventListener('change', loadHistory);
    document.getElementById('hist-sort').addEventListener('change', loadHistory);
    
    document.getElementById('btn-clear-history').addEventListener('click', () => {
        if (confirm("Are you sure you want to clear all history records?")) {
            fetch('/history/clear', { method: 'POST' })
            .then(res => res.json())
            .then(d => {
                if (d.success) {
                    showToast("History cleared.");
                    loadHistory();
                }
            });
        }
    });

    // CSV Exporter logic (client side export)
    document.getElementById('btn-export-csv').addEventListener('click', () => {
        if (!cachedHistoryRecords || cachedHistoryRecords.length === 0) {
            showToast("No history records to export.", "error");
            return;
        }

        let csvContent = "data:text/csv;charset=utf-8,";
        
        // Headers
        const headers = [
            "Prediction Date", 
            "Country Name", 
            "Life Expectancy", 
            "Mean Years of Schooling", 
            "Expected Years of Schooling", 
            "GNI per Capita", 
            "Estimated HDI Score", 
            "Predicted HDI Category", 
            "Prediction Confidence"
        ];
        
        csvContent += headers.map(h => `"${h}"`).join(",") + "\r\n";
        
        // Rows
        cachedHistoryRecords.forEach(r => {
            const rowData = [
                r.timestamp,
                r.country,
                r.life_expectancy.toFixed(1),
                r.mean_schooling.toFixed(1),
                r.expected_schooling.toFixed(1),
                r.gni_per_capita.toFixed(0),
                r.hdi_score.toFixed(3),
                r.predicted_category,
                `${r.prediction_confidence.toFixed(1)}%`
            ];
            csvContent += rowData.map(d => `"${d}"`).join(",") + "\r\n";
        });
        
        // Create trigger link and download
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        const timestamp = new Date().toISOString().slice(0,19).replace(/[:T]/g, "-");
        
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", `HDI_Prediction_History_Export_${timestamp}.csv`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        showToast("CSV Export downloaded successfully.");
    });

    // 11. Country Comparison Logic
    const compPresetA = document.getElementById('comp-preset-a');
    const compPresetB = document.getElementById('comp-preset-b');

    function syncCompPreset(selectEl, prefix) {
        const key = selectEl.value;
        if (!key || !countryPresets[key]) return;
        const profile = countryPresets[key];
        
        document.getElementById(`comp-life-${prefix}`).value = profile.life;
        document.getElementById(`comp-exp-${prefix}`).value = profile.expected;
        document.getElementById(`comp-mean-${prefix}`).value = profile.mean;
        document.getElementById(`comp-gni-${prefix}`).value = profile.gni;
    }

    compPresetA.addEventListener('change', () => syncCompPreset(compPresetA, 'a'));
    compPresetB.addEventListener('change', () => syncCompPreset(compPresetB, 'b'));

    function runComparison() {
        const nameA = compPresetA.options[compPresetA.selectedIndex].text;
        const nameB = compPresetB.options[compPresetB.selectedIndex].text;
        
        const payload = {
            country_a: {
                Name: nameA,
                Life_Expectancy: parseFloat(document.getElementById('comp-life-a').value),
                Expected_Schooling: parseFloat(document.getElementById('comp-exp-a').value),
                Mean_Schooling: parseFloat(document.getElementById('comp-mean-a').value),
                GNI_Per_Capita: parseFloat(document.getElementById('comp-gni-a').value)
            },
            country_b: {
                Name: nameB,
                Name: nameB,
                Life_Expectancy: parseFloat(document.getElementById('comp-life-b').value),
                Expected_Schooling: parseFloat(document.getElementById('comp-exp-b').value),
                Mean_Schooling: parseFloat(document.getElementById('comp-mean-b').value),
                GNI_Per_Capita: parseFloat(document.getElementById('comp-gni-b').value)
            }
        };

        fetch('/compare', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                const ca = data.country_a;
                const cb = data.country_b;
                
                document.getElementById('comp-name-a').textContent = ca.name;
                document.getElementById('comp-score-a').textContent = ca.prediction.toFixed(3);
                document.getElementById('comp-cat-a').textContent = ca.category;
                document.getElementById('comp-conf-a').textContent = `${ca.confidence.toFixed(1)}% Conf.`;
                
                document.getElementById('comp-name-b').textContent = cb.name;
                document.getElementById('comp-score-b').textContent = cb.prediction.toFixed(3);
                document.getElementById('comp-cat-b').textContent = cb.category;
                document.getElementById('comp-conf-b').textContent = `${cb.confidence.toFixed(1)}% Conf.`;
                
                renderComparisonChart(ca, cb);
            }
        });
    }

    document.getElementById('btn-run-comparison').addEventListener('click', runComparison);

    function renderComparisonChart(ca, cb) {
        if (activeCharts['compare']) {
            activeCharts['compare'].destroy();
        }
        
        const colors = getChartThemeColors();
        const norm = (val, min, max) => ((val - min) / (max - min)) * 100;
        
        const valsA = [
            norm(parseFloat(ca.inputs.Life_Expectancy), 20, 100),
            norm(parseFloat(ca.inputs.Expected_Schooling), 0, 22),
            norm(parseFloat(ca.inputs.Mean_Schooling), 0, 20),
            norm(Math.log(parseFloat(ca.inputs.GNI_Per_Capita)), Math.log(100), Math.log(150000))
        ];
        
        const valsB = [
            norm(parseFloat(cb.inputs.Life_Expectancy), 20, 100),
            norm(parseFloat(cb.inputs.Expected_Schooling), 0, 22),
            norm(parseFloat(cb.inputs.Mean_Schooling), 0, 20),
            norm(Math.log(parseFloat(cb.inputs.GNI_Per_Capita)), Math.log(100), Math.log(150000))
        ];
        
        const ctx = document.getElementById('chart-comparison-metrics').getContext('2d');
        activeCharts['compare'] = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Life Expectancy', 'Expected Schooling', 'Mean Schooling', 'Log GNI (Wealth)'],
                datasets: [
                    {
                        label: ca.name,
                        data: valsA,
                        backgroundColor: 'rgba(79, 70, 229, 0.8)',
                        borderColor: '#4f46e5',
                        borderWidth: 1
                    },
                    {
                        label: cb.name,
                        data: valsB,
                        backgroundColor: 'rgba(13, 148, 136, 0.8)',
                        borderColor: '#0d9488',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { labels: { color: colors.textColor } }
                },
                scales: {
                    x: { ticks: { color: colors.textColor }, grid: { color: colors.gridColor } },
                    y: { max: 100, min: 0, ticks: { color: colors.textColor }, grid: { color: colors.gridColor }, title: { display: true, text: 'Normalized Contribution (%)', color: colors.textColor } }
                }
            }
        });
    }

    // 12. Trend Projections Logic
    const trendPreset = document.getElementById('trend-preset');
    const trendInputs = ['slider-trend-life', 'slider-trend-expected', 'slider-trend-mean', 'slider-trend-gni'];

    trendPreset.addEventListener('change', runTrendProjection);
    trendInputs.forEach(id => {
        document.getElementById(id).addEventListener('input', (e) => {
            const val = parseFloat(e.target.value);
            let suffix = "";
            if (id === 'slider-trend-gni') suffix = "%";
            else suffix = " years";
            
            const sign = val >= 0 ? "+" : "";
            document.getElementById(id.replace('slider-', '') + '-val').textContent = `${sign}${val}${suffix}`;
            
            runTrendProjection();
        });
    });

    function runTrendProjection() {
        const countryKey = trendPreset.value;
        if (!countryPresets[countryKey]) return;
        
        const profile = countryPresets[countryKey];
        
        const dLife = parseFloat(document.getElementById('slider-trend-life').value);
        const dExpected = parseFloat(document.getElementById('slider-trend-expected').value);
        const dMean = parseFloat(document.getElementById('slider-trend-mean').value);
        const dGniPct = parseFloat(document.getElementById('slider-trend-gni').value);
        
        const lifeCurr = profile.life;
        const expCurr = profile.expected;
        const meanCurr = profile.mean;
        const gniCurr = profile.gni;
        
        const lifeFuture = Math.max(20, Math.min(100, lifeCurr + dLife));
        const expFuture = Math.max(0, Math.min(22, expCurr + dExpected));
        const meanFuture = Math.max(0, Math.min(20, meanCurr + dMean));
        const gniFuture = Math.max(100, Math.min(150000, gniCurr * (1 + (dGniPct / 100))));
        
        Promise.all([
            fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ Life_Expectancy: lifeCurr, Expected_Schooling: expCurr, Mean_Schooling: meanCurr, GNI_Per_Capita: gniCurr })
            }).then(r => r.json()),
            fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ Life_Expectancy: lifeFuture, Expected_Schooling: expFuture, Mean_Schooling: meanFuture, GNI_Per_Capita: gniFuture })
            }).then(r => r.json())
        ])
        .then(([resCurr, resFuture]) => {
            if (resCurr.success && resFuture.success) {
                document.getElementById('trend-score-curr').textContent = resCurr.prediction.toFixed(3);
                document.getElementById('trend-cat-curr').className = `badge badge-${resCurr.category.toLowerCase().replace(' ', '-')}`;
                document.getElementById('trend-cat-curr').textContent = resCurr.category;
                
                document.getElementById('trend-score-future').textContent = resFuture.prediction.toFixed(3);
                document.getElementById('trend-cat-future').className = `badge badge-${resFuture.category.toLowerCase().replace(' ', '-')}`;
                document.getElementById('trend-cat-future').textContent = resFuture.category;
                
                const diff = resFuture.prediction - resCurr.prediction;
                const sign = diff >= 0 ? "+" : "";
                document.getElementById('trend-improvement').textContent = `${sign}${diff.toFixed(3)}`;
                
                renderTrendChart(resCurr.prediction, resFuture.prediction);
            }
        });
    }

    function renderTrendChart(curr, future) {
        if (activeCharts['trend']) {
            activeCharts['trend'].destroy();
        }
        
        const colors = getChartThemeColors();
        const ctx = document.getElementById('chart-trend-projection').getContext('2d');
        activeCharts['trend'] = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Current Baseline State', 'Projected Target State'],
                datasets: [{
                    label: 'Human Development Index (HDI) Growth',
                    data: [curr, future],
                    borderColor: '#4f46e5',
                    backgroundColor: 'rgba(79, 70, 229, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.2,
                    pointRadius: 6,
                    pointBackgroundColor: '#4f46e5'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { labels: { color: colors.textColor } }
                },
                scales: {
                    x: { ticks: { color: colors.textColor }, grid: { color: colors.gridColor } },
                    y: { min: 0.4, max: 1.0, ticks: { color: colors.textColor }, grid: { color: colors.gridColor } }
                }
            }
        });
    }

    // 13. ML Workflow Panel Expand/Collapse (Accordion)
    document.querySelectorAll('.toggle-step-detail').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const stepEl = e.target.closest('.pipeline-step');
            const descEl = stepEl.querySelector('.step-long-desc');
            const isHidden = descEl.classList.contains('hidden');
            
            if (isHidden) {
                descEl.classList.remove('hidden');
                e.target.textContent = "Close Details ▴";
            } else {
                descEl.classList.add('hidden');
                e.target.textContent = "Learn More ▾";
            }
        });
    });

    // Initialize first load
    loadDashboardHome();
    runLivePrediction();
});
