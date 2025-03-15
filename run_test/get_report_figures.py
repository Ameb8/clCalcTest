import plotly.express as px
import plotly.graph_objects as go

template = 'ggplot2'  # Standard template for all figures

def wrap_graph_in_box(graph_html, title):
    return f"""
    <div style="
        border: 2px solid #333;
        border-radius: 10px;
        padding: 15px;
        margin: 15px 0;
        background-color: #f9f9f9;
        box-shadow: 3px 3px 10px rgba(0,0,0,0.1);
    ">
        <h3 style="text-align: center; margin-top: 0;">{title}</h3>
        {graph_html}
    </div>
    """

def expr_len_bar(test_results):
    """
    Generates a bar chart showing the distribution of expression lengths,
    comparing all expressions to failed expressions.
    """
    all_counts = test_results.data['Length'].value_counts().sort_index()
    failed_counts = test_results.data[test_results.data['Passed'] == False]['Length'].value_counts().sort_index()
    lengths = sorted(set(all_counts.index).union(set(failed_counts.index)))
    all_counts = all_counts.reindex(lengths, fill_value=0)
    failed_counts = failed_counts.reindex(lengths, fill_value=0)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=lengths, y=all_counts, name='All Expressions', marker_color='blue'))
    fig.add_trace(go.Bar(x=lengths, y=failed_counts, name='Failed Expressions', marker_color='red'))

    fig.update_layout(
        template=template,
        barmode='group',
        xaxis_title='Expression Length (number of operators)',
        yaxis_title='Occurrences',
        xaxis=dict(type='category'),
    )

    return wrap_graph_in_box(fig.to_html(full_html=False), "Expression Length Distribution")

def num_op_bar(test_results):
    """
    Generates a bar chart comparing operator usage between all expressions and failed expressions.
    """
    operators = test_results.num_ops['Operators']
    in_all = test_results.num_ops['In All']
    in_failed = test_results.num_ops['In Failed']

    fig = go.Figure()
    fig.add_trace(go.Bar(x=operators, y=in_all, name='In All', marker_color='blue'))
    fig.add_trace(go.Bar(x=operators, y=in_failed, name='In Failed', marker_color='red'))

    fig.update_layout(
        template=template,
        barmode='group',
        xaxis_title='Operator',
        yaxis_title='Occurrences',
        xaxis=dict(type='category')
    )

    return wrap_graph_in_box(fig.to_html(full_html=False), "Operator Usage in Expressions")

def conf_matrix(test_results):
    """
    Generates a confusion matrix heatmap comparing actual errors to those detected by clCalc.
    """
    errors_df = test_results.errors
    fig = px.imshow(errors_df.values,
                    labels={'x': 'clCalc Detected Errors', 'y': 'Actual Errors'},
                    x=errors_df.columns,
                    y=errors_df.index,
                    color_continuous_scale='Blues')

    fig.update_traces(text=errors_df.values,
                      texttemplate='%{text}',
                      textfont=dict(size=16))

    fig.update_layout(
        template=template,
        xaxis_title='clCalc Detected Errors',
        yaxis_title='Actual Errors',
        title_x=0.5,
        title_y=0.95,
        xaxis=dict(showgrid=True, zeroline=False),
        yaxis=dict(showgrid=True, zeroline=False),
        coloraxis_colorbar=dict(title="Counts")
    )

    return wrap_graph_in_box(fig.to_html(full_html=False), "Confusion Matrix of Errors Detected by clCalc")

def error_pie(test_results):
    error_counts = test_results.errors.sum(axis=1)  # Summing across columns to get total occurrences
    labels = error_counts.index
    values = error_counts.values

    fig = px.pie(
        names=labels,
        values=values,
        color_discrete_sequence=['blue', 'red', 'orange']
    )

    fig.update_layout(template=template)

    return wrap_graph_in_box(fig.to_html(full_html=False), "Error Type Distribution")

