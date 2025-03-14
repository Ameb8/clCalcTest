import plotly.graph_objects as go

import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# Function to create confusion matrix plot from test_metrics
def get_conf_matrix(test_metrics):
    # Extract values from test_metrics
    math_errs = test_metrics.err_rates.math_errs
    syntax_errs = test_metrics.err_rates.syntax_errs

    missed_math = test_metrics.missed_errs.math_errs
    missed_syntax = test_metrics.missed_errs.syntax_errs

    false_pos_math = test_metrics.false_pos.math_errs
    false_pos_syntax = test_metrics.false_pos.syntax_errs

    # Create the confusion matrix as a 3x3 matrix
    confusion_matrix = np.array([
        [math_errs, false_pos_syntax, missed_math],  # Row for Math Error (Actual)
        [false_pos_math, syntax_errs, missed_syntax],  # Row for Syntax Error (Actual)
        [0, 0, (test_metrics.num_tests() - (
                    math_errs + syntax_errs + missed_math + missed_syntax + false_pos_math + false_pos_syntax))]
        # Row for No Error (Actual)
    ])

    # Define labels for rows and columns
    labels = ['Detected Math Error', 'Detected Syntax Error', 'No Error Detected']

    # Create the Plotly confusion matrix heatmap
    fig = px.imshow(
        confusion_matrix,
        labels=dict(x="Predicted", y="Actual", color="Count"),
        x=labels,
        y=labels,
        color_continuous_scale="Blues",
        title="Confusion Matrix",
        text_auto=True  # Add numbers to each square of the matrix
    )

    # Create the HTML section for the confusion matrix
    confusion_html = f"""
    <h2>Confusion Matrix</h2>
    <div class="chart-container">
        {fig.to_html(full_html=False, include_plotlyjs='cdn')}
    </div>
    """

    return confusion_html

def get_op_types(ops):
    fig = get_bar_chart(ops, ['Blue', 'Red'], 'Operator Occurrences in Expressions')
    return f"""
    <h2>Operator Types</h2>
    <div class="chart-container">
        {fig.to_html(full_html=False, include_plotlyjs='cdn')}
    </div>
    """

def get_bar_chart(df, colors, title):
    fig = go.Figure()

    x_labels = df.iloc[:, 0]  # First column as x-axis labels
    num_cols = len(df.columns) - 1

    for i in range(num_cols):
        fig.add_trace(go.Bar(
            x=x_labels,
            y=df.iloc[:, i + 1],  # Each subsequent column as y values
            name=df.columns[i + 1],  # Column name as legend
            marker_color=colors[i]  # Assign color from list
        ))

    fig.update_layout(
        title=title,
        xaxis_title=df.columns[0],
        yaxis_title="Values",
        barmode="group"  # Ensure bars are adjacent
    )

    return fig


