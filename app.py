from flask import Flask, render_template
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
import pandas as pd
import locale
locale.setlocale( locale.LC_ALL, '' )
pd.options.display.float_format = '${:,.2f}'.format

app = Flask(__name__)

@app.route('/')
def index():
    df_overall = pd.read_json('http://localhost:5001/sales/last/overall')
    df_overall = df_overall[:-1] # remove 2018

    year_average = locale.currency(pd.read_json('http://localhost:5001/sales/summary/year/avg').iloc[0]['AMOUNT'])
    year_sum = locale.currency(pd.read_json('http://localhost:5001/sales/summary/year/sum').iloc[0]['AMOUNT'])
    month_average = locale.currency(pd.read_json('http://localhost:5001/sales/summary/month/avg').iloc[0]['AMOUNT'])
    month_sum = locale.currency(pd.read_json('http://localhost:5001/sales/summary/year/sum').iloc[0]['AMOUNT'])

    top_customer = pd.read_json('http://localhost:5001/sales/top/customer/5')[['NAME','AMOUNT']]
    top_city = pd.read_json('http://localhost:5001/sales/top/city/5')[['NAME','AMOUNT']]
    top_month = pd.read_json('http://localhost:5001/sales/top/month/5')[['MONTH','YEAR','AMMOUNT']]
    top_item = pd.read_json('http://localhost:5001/sales/top/item/5')[['NAME','AMOUNT']]

    # init a basic bar chart:
    # http://bokeh.pydata.org/en/latest/docs/user_guide/plotting.html#bars
    fig = figure(plot_width=1024, plot_height=380,toolbar_location="below")
    fig.vbar(
        x=df_overall['YEAR'],
        width=0.5,
        bottom=0,
        top=df_overall['AMOUNT'],
        color='darkslateblue',
    )

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components(fig)
    html = render_template(
        'index.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
        year_average=year_average,
        year_sum=year_sum,
        month_average=month_average,
        month_sum=month_sum,
        top_customer=top_customer.to_html(classes='table table-striped table-sm',justify='left', index=False, border=0),
        top_city = top_city.to_html(classes='table table-striped table-sm',justify='left', index=False, border=0), 
        top_month = top_month.to_html(classes='table table-striped table-sm',justify='left', index=False, border=0), 
        top_item = top_item.to_html(classes='table table-striped table-sm',justify='left', index=False, border=0), 
    )
    return encode_utf8(html)

if __name__ == '__main__':
    app.run(debug=True)
