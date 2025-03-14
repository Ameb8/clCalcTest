import plotly.graph_objects as go
import plotly.express as px
from test_results import TestResults
import pandas as pd

template = 'ggplot2'

def expr_len_bar(test_results):
    # Count occurrences of each length for all expressions
    all_counts = test_results.data['Length'].value_counts().sort_index()
    failed_counts = test_results.data[test_results.data['Passed'] == False]['Length'].value_counts().sort_index()

    # Ensure both series have the same indices
    lengths = sorted(set(all_counts.index).union(set(failed_counts.index)))
    all_counts = all_counts.reindex(lengths, fill_value=0)
    failed_counts = failed_counts.reindex(lengths, fill_value=0)

    # Create bar chart
    fig = go.Figure()
    fig.add_trace(go.Bar(x=lengths, y=all_counts, name='All Expressions', marker_color='blue'))
    fig.add_trace(go.Bar(x=lengths, y=failed_counts, name='Failed Expressions', marker_color='red'))

    # Update layout
    fig.update_layout(
        template=template,
        barmode='group',  # Side-by-side bars
        title='Expression Length Distribution',
        xaxis_title='Expression Length',
        yaxis_title='Occurrences',
        xaxis=dict(type='category'),
    )

    return fig.to_html(full_html=False)

import plotly.graph_objects as go

def num_op_bar(test_results):
    # Extract data
    operators = test_results.num_ops['Operators']
    in_all = test_results.num_ops['In All']
    in_failed = test_results.num_ops['In Failed']

    # Create bar chart
    fig = go.Figure()
    fig.add_trace(go.Bar(x=operators, y=in_all, name='In All', marker_color='blue'))
    fig.add_trace(go.Bar(x=operators, y=in_failed, name='In Failed', marker_color='red'))

    # Update layout
    fig.update_layout(
        template=template,
        barmode='group',  # Side-by-side bars
        title='Operator Usage in Expressions',
        xaxis_title='Operator',
        yaxis_title='Occurrences',
        xaxis=dict(type='category')
    )

    return fig.to_html(full_html=False)

def conf_matrix(test_results):
    errors_df = test_results.errors
    # Create a heatmap using Plotly
    fig = px.imshow(errors_df.values,
                    labels={'x': 'clCalc Detected Errors', 'y': 'Actual Errors'},
                    x=errors_df.columns,
                    y=errors_df.index,
                    color_continuous_scale='Blues',
                    title='Confusion Matrix of Errors Detected by clCalc')

    # Add text annotations for each cell (the actual counts)
    fig.update_traces(text=errors_df.values,  # Set the text to be the actual values
                      texttemplate='%{text}',    # Display the text exactly as it is
                      textfont=dict(size=16))    # Font size for the text

    # Customize layout to add a better title and grid lines
    fig.update_layout(
        template=template,
        xaxis_title='clCalc Detected Errors',
        yaxis_title='Actual Errors',
        title_x=0.5,  # Center the title
        title_y=0.95,
        xaxis=dict(showgrid=True, zeroline=False),
        yaxis=dict(showgrid=True, zeroline=False),
        coloraxis_colorbar=dict(title="Counts")  # Move coloraxis_colorbar here
    )

    return fig.to_html(full_html=False)
