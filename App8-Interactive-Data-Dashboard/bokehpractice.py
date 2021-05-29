#install bokeh, not bokehdev(bokeh for dev not use cdn)

from pandas_datareader import data
from datetime import datetime
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.resources import CDN

start = datetime(2015,11,1)
end = datetime(2016,3,10)
# data_source support : https://pandas-datareader.readthedocs.io/en/latest/remote_data.html#remote-data-access
df=data.DataReader(name="GOOG",data_source="yahoo",start=start, end=end)
df

date_increase = df.index[df.Close > df.Open]
date_decrease = df.index[df.Close < df.Open]

def inc_dec(df_close,df_open):
    if df_close > df_open :
        return "Increase"
    elif df_close < df_open:
        return "Decrease"
    else :
        return "Equal"

df["Status"]=[inc_dec(c,o) for c,o in zip(df.Close,df.Open)]
df["Middle"]=(df.Open+df.Close)/2
df["Height"]=abs(df.Open-df.Close)

# use sizing_mode = "scale_width" instead of responsive=True to scale with window
p = figure(x_axis_type='datetime', width = 1000, height = 300, 
            sizing_mode = "scale_width")
p.title.text ="Candlestick Chart"

# grid transparent from 0->1. 0 is transparent 
p.grid.grid_line_alpha = 0.3

# be rong o vuong
hours_12 = 12*60*60*1000

#add Line into rect
#add before rect so that it will be behind rect
p.segment(df.index, df.High, df.index, df.Low, color="Black")

# x_axis, y_axis, width of rect, height of rect
#p.rect(date_increase,(df.Open+df.Close)/2, hours_12, 
#       abs(df.Open-df.Close),fill_color="green", line_color="black")
#p.rect(date_decrease,(df.Open+df.Close)/2, hours_12, 
#       abs(df.Open-df.Close),fill_color="red", line_color="black")
# use "#"+CSS Colors => "#CCFFFF"
p.rect(df.index[df.Status=="Increase"],df.Middle[df.Status=="Increase"], hours_12, 
        df.Height[df.Status=="Increase"],fill_color="#CCFFFF", line_color="black")
p.rect(df.index[df.Status=="Decrease"],df.Middle[df.Status=="Decrease"], hours_12, 
        df.Height[df.Status=="Decrease"],fill_color="#FF3333", line_color="black")

#scripts used for html. components is tuple
script1, div1 = components(p)
cdn_js = CDN.js_files[0]
cdn_css = CDN.css_files[0]

#use mode = "inline" if bokeh is blank
#output_file("CS.html",mode="inline")
#output_file("CS.html",mode="cdn")
#show(p)