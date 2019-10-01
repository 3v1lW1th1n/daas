from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.charts import Bar
from daas_app.utils.statistics_manager import StatisticsManager
from daas_app.utils.configuration_manager import ConfigurationManager
from pyecharts import options as opts


def bar_stack0() -> Bar:
    chart = Bar(init_opts=opts.InitOpts(width="1400px", height="720px"))
    chart.set_global_opts(title_opts=opts.TitleOpts(title="Samples per size"),

                          yaxis_opts=opts.AxisOpts(name='Samples',
                                                   name_textstyle_opts=opts.global_options.TextStyleOpts(font_size=16)),
                          xaxis_opts=opts.AxisOpts(name='Size (kb)',
                                                   name_textstyle_opts=opts.global_options.TextStyleOpts(font_size=16)))

    # Data (y axis)
    range_groups = [StatisticsManager().get_size_statistics_for_file_type(file_type) for file_type in ConfigurationManager().get_identifiers()]
    for range_group in range_groups:
        # Add values on the yaxis for each file type.
        # If the count is 0, replace it by None to avoid overlapped numbers in the chart.
        chart.add_yaxis(range_group.file_type, range_group.counts, category_gap=4, stack="stack1")

    # Captions (x axis)
    chart.add_xaxis(range_groups[0].captions)
    chart.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    return chart
# from daas_app.utils.chart_test import *

#bar_stack0().render()