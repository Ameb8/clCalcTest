import webbrowser
import os
import get_report_figures as get


def get_expr_len_stats(test_results):
    if test_results.data.empty:
        return "<h2>Expression Statistics</h2><p>No test data available.</p>"

    mean_length = test_results.data['Length'].mean()
    median_length = test_results.data['Length'].median()
    std_dev_length = test_results.data['Length'].std()

    return f"""
    <h2>Expression Length Statistics</h2>
    <div class="stats-section">
        <p><strong>Mean Length:</strong> {mean_length:.2f}</p>
        <p><strong>Median Length:</strong> {median_length:.2f}</p>
        <p><strong>Standard Deviation:</strong> {std_dev_length:.2f}</p>
    </div>
    """


def get_report(test_results, filename="test_results_report.html"):
    # Initialize the HTML content with a light color scheme
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Test Results Report</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Poppins', sans-serif;
                background-color: #f5f5f5;
                margin: 0;
                padding: 0;
                color: #333;
            }
            .container {
                max-width: 900px;
                margin: auto;
                background: #ffffff;
                padding: 30px;
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
                border-radius: 12px;
                overflow: hidden;
            }
            h1, h2 {
                text-align: center;
                color: #222;
                font-weight: 600;
            }
            h1 { font-size: 2.5em; margin-bottom: 30px; }
            h2 { font-size: 2em; margin-top: 40px; }
            .expression-section {
                margin-bottom: 20px;
                padding: 20px;
                border-radius: 8px;
                background-color: #f0f0f0;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            }
            .expression-header {
                font-size: 1.6em;
                font-weight: 600;
                margin-bottom: 12px;
                padding-bottom: 10px;
                border-bottom: 2px solid #ccc;
            }
            .result-section {
                margin-top: 15px;
                padding-left: 20px;
            }
            .passed { color: #2e7d32; font-weight: 600; }
            .failed { color: #d32f2f; font-weight: 600; }
            .footer {
                text-align: center;
                margin-top: 50px;
                color: #666;
                font-size: 0.9em;
            }
            .footer a {
                color: #3f87f2;
                text-decoration: none;
            }
            .stats-section {
                text-align: center;
                padding: 15px;
                background-color: #e0e0e0;
                border-radius: 8px;
                margin-bottom: 30px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }
            .stats-section p {
                font-size: 1.2em;
                margin: 5px 0;
            }
            details {
                background-color: #f0f0f0;
                border-radius: 8px;
                margin-bottom: 20px;
                padding: 10px;
                cursor: pointer;
            }
            summary {
                font-size: 1.6em;
                font-weight: 600;
                padding: 10px;
                color: #333;
                cursor: pointer;
            }
            details[open] {
                padding-bottom: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Test Results Report</h1>
    """

    # Add the statistics section
    html_content += f'<h3 style="text-align: center;">Test Cases Passed: {len(test_results.data) - test_results.num_failed}/{len(test_results.data)}</h3>'

    # Add collapsible Passed expressions **before** statistics
    html_content += """
        <details>
            <summary>Passed Expressions</summary>
    """
    for _, row in test_results.data.iterrows():
        if row['Passed']:
            html_content += f"""
            <div class="expression-section">
                <div class="expression-header passed">{row['Expression']}</div>
                <div class="result-section">
                    <div>clCalc Result: {row['clCalc Result']}</div>
                    <div>Python Result: {row['Python Result']}</div>
                </div>
            </div>
            """
    html_content += "</details>"

    # Add collapsible Failed expressions **before** statistics
    html_content += """
        <details>
            <summary>Failed Expressions</summary>
    """
    for _, row in test_results.data.iterrows():
        if not row['Passed']:
            html_content += f"""
            <div class="expression-section">
                <div class="expression-header failed">{row['Expression']}</div>
                <div class="result-section">
                    <div>clCalc Result: {row['clCalc Result']}</div>
                    <div>Python Result: {row['Python Result']}</div>
                </div>
            </div>
            """
    html_content += "</details>"

    # Now add statistics
    html_content += get_expr_len_stats(test_results)
    html_content += get.expr_len_bar(test_results)
    html_content += get.num_op_bar(test_results)
    html_content += get.conf_matrix(test_results)
    html_content += get.error_pie(test_results)

    # Add footer
    html_content += """
    </div>
    </body>
    </html>
    """

    # Save and open the report
    with open(filename, 'w') as file:
        file.write(html_content)

    webbrowser.open(f'file://{os.path.abspath(filename)}')



