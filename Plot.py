# coding: utf-8
import sys
import plotly
from plotly.offline import init_notebook_mode
import plotly.graph_objs as go
import pandas as pd


def initLikert(serviceIndex,landScapeIndex,socialIndex,filePathName):

    print(plotly.__version__)
    print(sys.version)
    print(str(serviceIndex) + " " + str(landScapeIndex) + " " + str(socialIndex) +
          " " + str(filePathName))

    init_notebook_mode(connected=True)

    # py.sign_in('PauloPimenta', 'dehPQ8xFFpN0VrkIVT9i')
    file = pd.read_excel(filePathName, sheetname="base")
    # file = filePathName

    # LandUse : a - agriculture, f - forest, s- human_settlement, g - grass_land
    # SE : A - Food, B - wood, C- water_supply, D - water_regulation, E-air_quality , F -scenic_beauty

    file.columns = ['id', 'gender', 'age', 'age_class', 'education', 'activity',
                    'attachment', 'agriculture_food', 'agriculture_wood', 'agriculture_water_supply', 'agriculture_regulation', 'agriculture_air_quality', 'agriculture_scenic_beauty',
                    'settlement_food', 'settlement_wood', 'settlement_water_supply','settlement_regulation', 'settlement_air_quality', 'settlement_scenic_beauty',
                    'forest_food', 'forest_wood', 'forest_water_supply', 'forest_regulation', 'forest_air_quality', 'forest_scenic_beauty',
                    'grassland_food', 'grassland_wood', 'grassland_water_supply','grassland_regulation', 'grassland_air_quality', 'grassland_scenic_beauty']

    # Select only the important collums
    # df =  df[['species','Survey_question_ID','sign','is_positive']]

    # Defining our vectors
    social_variables = ['gender',' age', 'age_class', 'education', 'activity']
    land_scape = ['agriculture', 'forest', 'settlement', 'grassland']
    services = ['food', 'wood', 'water_supply', 'regulation', 'air_quality', 'scenic_beauty']
    likert_values = ['No data', 'Very low', 'Low', 'Medium', 'High', 'Very high']

    # Creating vectors of selected variables
    land_scape = [land_scape[landScapeIndex]]
    land_scape_name = land_scape[0]
    services = [services[serviceIndex]]
    serviceName = services[0]
    socialVarName = social_variables[socialIndex]

    colors = ['rgba(38, 24, 74, 0.8)', 'rgba(71, 58, 131, 0.8)',
              'rgba(122, 120, 168, 0.8)', 'rgba(164, 163, 204, 0.85)',
              'rgba(190, 192, 213, 1)','rgba(190, 67, 19, 0.85)']

    # Counting the values, from 1(no_data) to 5
    x_data = []
    x_data_perc = []
    y_data = []
    # Extracting unique values of chosen social variable from file
    variable = file[socialVarName].unique()
    variable = sorted(variable)
    # Creating two empty dataframes : one with absolute and the second percentage values for each landscape
    total_land = pd.DataFrame({socialVarName: variable})
    total_land_perc = pd.DataFrame({socialVarName: variable})
    variable_label = socialVarName.title() + ": "

    for y in range(0, len(variable)):
        y_data.append(variable_label + variable[y])
        continue

    for se in range(0, len(services)):
        service_name = services[se]
        for ls in range(0,len(land_scape)):
            landscape_name = land_scape[ls]
            # y_data.append("Age " + service_name + "<br> in " + landscape_name + " ?")
            for lik_scale in range(0,len(likert_values)):
                landscape_service = landscape_name + '_' + service_name
                count_temp = file[file[landscape_service] == lik_scale]
                count_temp = count_temp.groupby([socialVarName])[landscape_service].count()
                count_temp = count_temp.reset_index(name=landscape_service)
                new_column_name = landscape_service + '_' + likert_values[lik_scale]
                count_temp = count_temp.rename(columns={landscape_service :  new_column_name})
                # Merging before percentage
                total_land = pd.merge(total_land, count_temp, on=socialVarName, how='left').fillna(0)
                # Calculating total
                total_count = count_temp[new_column_name].sum()
                # Calculating percentage
                count_temp[new_column_name] = round(count_temp[new_column_name] * 100 / total_count,2)
                # Merging after percentage
                total_land_perc = pd.merge(total_land_perc, count_temp, on=socialVarName, how='left').fillna(0)
                # x_data.append(count_temp[new_column_name].tolist())
                continue
            continue
        continue

    for row in total_land.iterrows():
        index, data = row
        data = data.tolist()
        del data[0]
        x_data.append(data)
        continue

    for row in total_land_perc.iterrows():
        index, data = row
        data = data.tolist()
        del data[0]
        x_data_perc.append(data)
        continue

    # def createPlotlyTracces() :

    traces = []
    for i in range(0, len(x_data_perc[0])):
        for xd, yd in zip(x_data_perc, y_data):
            traces.append(go.Bar(
                x=[xd[i]],
                y=[yd],
                name= 'total',
                orientation='h',
                marker=dict(
                    color=colors[i],
                    line=dict(
                        color='rgb(248, 248, 249)',
                        width=1)
                )
            ))
    layout = go.Layout(
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            domain=[0.15, 1]),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,),
            barmode='stack',
        paper_bgcolor='rgb(248, 248, 255)',
        plot_bgcolor='rgb(248, 248, 255)',
        margin=dict(l=120,
                    r=10,
                    t=140,
                    b=80),
        showlegend=False,
        title='How much you value ' + services[0] + ' in ' + land_scape[0] + ' ?',
        # height=640,
        # #width=800,
        )

    annotations = []
    for yd, xd in zip(y_data, x_data_perc):
        # labeling the y-axis
        annotations.append(dict(xref='paper',
                                yref='y',
                                x=0.14,
                                y=yd,
                                xanchor='right',
                                text=str(yd),
                                font=dict(family='Arial',
                                          size=14,
                                          color='rgb(67, 67, 67)'),
                                showarrow=False,
                                align='right'))
        # labeling the first percentage of each bar (x_axis)
        annotations.append(dict(xref='x',
                                yref='y',
                                x=xd[0] / 2,
                                y=yd,
                                text=str(xd[0]) + '%',
                                font=dict(family='Arial',
                                          size=14,
                                          color='rgb(248, 248, 255)'),
                                showarrow=False))
        # labeling the first Likert scale (on the top)
        if yd == y_data[-1]:
            annotations.append(dict(xref='x',
                                    yref='paper',
                                    x=xd[0] / 2,
                                    y=1.1,
                                    text=likert_values[0],
                                    font=dict(family='Arial',
                                              size=14,
                                              color='rgb(67, 67, 67)'),
                                    showarrow=False))
        space = xd[0]
        for i in range(1, len(xd)):

            # labeling the rest of percentages for each bar (x_axis)
            annotations.append(dict(xref='x',
                                    yref='y',
                                    x=space + (xd[i]/2),
                                    y=yd,
                                    text=str(xd[i]) + '%',
                                    font=dict(family='Arial',
                                              size=14,
                                              color='rgb(248, 248, 255)'),
                                    showarrow=False))
            # labeling the Likert scale
            if yd == y_data[-1]:
                annotations.append(dict(xref='x',
                                        yref='paper',
                                        x=space + (xd[i]/2),
                                        y=1.1,
                                        text=likert_values[i],
                                        font=dict(family='Arial',
                                                  size=14,
                                                  color='rgb(67, 67, 67)'),
                                        showarrow=False))
            space += xd[i]

    layout['annotations'] = annotations
    fig = go.Figure(data=traces, layout=layout)
    # py.iplot(fig, filename='bar-colorscale')
    htmlName = str(serviceName + '_in_' + land_scape_name + '_per_' + socialVarName + '.html')
    print(htmlName)
    plotly.offline.plot(fig, filename=htmlName,show_link=False)