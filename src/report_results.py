import plotly.graph_objects as go
import webbrowser
import os
import numpy as np
from report_content import get_conf_matrix, get_op_types
from test_metrics import TestMetrics

def get_result(test_metrics):
    # Get the total number of tests and the number of failed tests
    total_tests = test_metrics.num_tests()
    failed_tests = len(test_metrics.failed_expr)
    passed_tests = total_tests - failed_tests

    # Format the string in HTML
    test_case_status_html = f"""
    <div class="test-case-status">
        <h3>Test Cases Passed: {passed_tests} / {total_tests}</h3>
    </div>
    """
    return test_case_status_html

def get_expr_stats(test_metrics):
    expr_lens = test_metrics.expr_lens
    abs_expr_lens = np.abs(expr_lens)  # Take the absolute values of expr_lens

    # Calculate statistics
    mean_expr_len = np.mean(abs_expr_lens)
    median_expr_len = np.median(abs_expr_lens)
    std_dev_expr_len = np.std(abs_expr_lens)

    # Create the "Expression Length Statistics" section
    expr_stats_html = f"""
    <h2>Expression Length Statistics</h2>
    <p><strong>Mean Expression Length:</strong> {mean_expr_len:.2f}</p>
    <p><strong>Median Expression Length:</strong> {median_expr_len}</p>
    <p><strong>Standard Deviation of Expression Lengths:</strong> {std_dev_expr_len:.2f}</p>
    """

    return expr_stats_html


def expr_length_bar(data):
    abs_data = np.abs(data)

    # Manually count occurrences of each absolute value
    value_counts = {}
    original_signs = {}

    # Count values and track their original signs
    for original, abs_val in zip(data, abs_data):
        value_counts[abs_val] = value_counts.get(abs_val, 0) + 1
        if abs_val not in original_signs:
            original_signs[abs_val] = []
        original_signs[abs_val].append('red' if original < 0 else 'blue')

    # Prepare the sorted values and their counts
    sorted_x = sorted(value_counts.keys())  # Sorted absolute values
    sorted_y = [value_counts[x] for x in sorted_x]  # Corresponding counts

    # Prepare color list for each bar, with special handling for -12
    sorted_colors = []
    for x in sorted_x:
        color_list = original_signs[x]
        if x == 12:
            # If the value is 12, make the last occurrence red (if negative)
            if color_list.count('red') > 0:
                color_list[-1] = 'red'
            else:
                color_list = ['blue'] * len(color_list)  # If no red, all blue
        sorted_colors.extend(color_list)

    # Create the bar chart
    fig = go.Figure(data=[
        go.Bar(
            x=sorted_x,
            y=sorted_y,
            marker=dict(color=sorted_colors)
        )
    ])

    fig.update_layout(
        title="Bar Chart of Absolute Expression Lengths",
        xaxis_title="Absolute Expression Length",
        yaxis_title="Count"
    )

    return fig.to_html(full_html=False, include_plotlyjs='cdn')


def expr_length_barchart(data):
    abs_data = np.abs(data)

    # Manually count occurrences of each absolute value
    value_counts = {}
    original_signs = {}

    for original, abs_val in zip(data, abs_data):
        value_counts[abs_val] = value_counts.get(abs_val, 0) + 1
        if abs_val not in original_signs:
            original_signs[abs_val] = 'red' if original < 0 else 'blue'  # Assign color based on first occurrence

    # Convert counts to sorted lists for plotting
    sorted_x = sorted(value_counts.keys())  # Sorted absolute values
    sorted_y = [value_counts[x] for x in sorted_x]  # Corresponding counts
    sorted_colors = [original_signs[x] for x in sorted_x]  # Colors based on original values

    # Create bar chart
    fig = go.Figure(data=[
        go.Bar(
            x=sorted_x,
            y=sorted_y,
            marker=dict(color=sorted_colors)
        )
    ])

    fig.update_layout(
        title="Bar Chart of Absolute Expression Lengths",
        xaxis_title="Absolute Expression Length",
        yaxis_title="Count"
    )

    return fig.to_html(full_html=False, include_plotlyjs='cdn')


def expr_length_histogram(data):
    abs_data = np.abs(data)
    colors = ['red' if x < 0 else 'blue' for x in data]

    fig = go.Figure()
    fig.add_trace(go.Histogram(x=abs_data, marker=dict(color=colors)))
    return fig.to_html(full_html=False, include_plotlyjs='cdn')

def get_report(test_metrics, debug=False):
    expr_lens = expr_length_bar(test_metrics.expr_lens)

    # DEBUG
    if debug:
        print(f"failed_expr: {test_metrics.failed_expr}")
        print(f"failed_clc: {test_metrics.failed_clc}")
        print(f"failed_sympy: {test_metrics.failed_sympy}")
    # END DEBUG

    # Create the "Failed Expressions" section if there are failed expressions
    failed_expr_html = ""
    failed_section = ""
    if test_metrics.failed_expr:
        for expr, clc, sympy in zip(test_metrics.failed_expr, test_metrics.failed_clc, test_metrics.failed_sympy):
            failed_expr_html += f"""
            <div class="card">
                <h3>{expr}</h3>
                <p><strong>clCalc Result:</strong> {clc}</p>
                <p><strong>SymPy Result:</strong> {sympy}</p>
            </div>
            """
        failed_section = f"""
        <h2>Failed Expressions</h2>
        {failed_expr_html}
        """

    # Define where to save the HTML file
    html_file_name = "clCalc_test_results.html"

    # Create the HTML report structure
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Test Metrics Report</title>
        <style>
            body {{
                font-family: 'Inter', sans-serif;
                background-color: #f4f4f9;
                color: #333;
                margin: 0;
                padding: 20px;
                text-align: center;
            }}
            .container {{
                max-width: 900px;
                margin: auto;
                background: white;
                padding: 20px;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
                border-radius: 10px;
            }}
            h1 {{
                color: #0056b3;
            }}
            h2 {{
                border-bottom: 2px solid #0056b3;
                padding-bottom: 5px;
            }}
            .chart-container {{
                margin: 20px 0;
                padding: 10px;
                background: #fff;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            .card {{
                background: white;
                padding: 15px;
                border-radius: 8px;
                box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
                margin-bottom: 15px;
                text-align: left;
            }}
            .card h3 {{
                color: #d9534f;
                margin-bottom: 5px;
            }}
            p {{
                margin: 5px 0;
            }}
        </style>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    </head>
    <body>
        <div class="container">
            <h1>Test Metrics Report</h1>
            {get_result(test_metrics)}
            {get_expr_stats(test_metrics)}

            <h2>Expression Length Distribution</h2>
            <div class="chart-container">
                {expr_lens}
            </div>
            
            {get_op_types(test_metrics.num_ops)}
            
            <div class="chart-container">
                {get_conf_matrix(test_metrics)}
            </div>
            
            <h2>Failed Expressions</h2>
            {failed_expr_html}
        </div>
    </body>
    </html>
    """

    # Get the absolute path where the file is saved
    file_path = os.path.abspath(html_file_name)

    # Save to an HTML file
    with open(file_path, "w") as f:
        f.write(html_content)

    print("HTML report generated: test_metrics_report.html")

    # Open the file automatically in the default browser
    webbrowser.open("file://" + file_path)