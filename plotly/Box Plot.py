import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

#______________________________________________________________________________________________________________________
#_____START OF DATA EXTRACTION_____#

def get_football_season_links(country):
    countries = ['england', 'germany', 'italy', 'spain', 'france', 'netherlands', 'belgium', 'portugal', 'turkey']
    if country in countries:
        webpage_res = requests.get(f'https://www.football-data.co.uk/{country}m.php')
        webpage = webpage_res.content
        soup = BeautifulSoup(webpage, 'html.parser')
        data_table = soup.find_all('tr')
        data_table_links = soup.find_all('a', )
        for link in data_table_links:
            if 'csv' in str(link):
                print(link)
    else:
        country = input(f"Please select a country from the following list: {countries}")




# Get football results into a data frame
def football_results_df(country, year):
    country.lower()
    countries = {'germany': '/D1', 'spain': '/SP1', 'england': '/E0', 'italy': '/I1'}
    years = ['2021', '1920', '1819', '1718']
    if country in countries.keys() and year in years:
        df = pd.read_csv(f'https://www.football-data.co.uk/mmz4281/{year}{countries.get(country)}.csv')
        return df
    else:
        country = input(f"Please select a country from the following list: {countries.keys()}")

#_____END OF DATA EXTRACTION_____#
#_____________________________________________________________________________________________________________________

#_____START OF DATA MANIPULATION_____#
#_____________________________________________________________________________________________________________________

def match_results(result):
    if result == 'A':
        return "Away Team Win"
    elif result == 'H':
        return "Away Team Win"
    elif result == 'D':
        return "Draw"
# Helper functions - End

###RAW DATA###
bundesliga = football_results_df('germany', '2021')
la_liga = football_results_df('spain', '2021')
serie_a = football_results_df('italy', '2021')
premier_league = football_results_df('england', '2021')

main_table = pd.concat([bundesliga, la_liga, serie_a, premier_league])
main_table['id'] = main_table['Div'] + "_" + main_table['HomeTeam'] + "_" + main_table['AwayTeam'] + "_" + main_table['Date']
main_table['total_goal_difference'] = main_table['FTHG'] - main_table['FTAG']
main_table['is_draw'] = main_table['FTR'].apply(lambda x: 1 if x == 'D' else 0)
columns = [x for x in main_table.columns][:23]
###END RAW DATA###

###DRAWS BY LEAGUE AGGREGATE###
draws_by_league = main_table.groupby("Div", as_index=False)['is_draw'].sum() \
    .rename(columns={'Div': 'European_leagues', 'is_draw': 'total_draws'}) \
    .replace({'D1': 'Bundesliga (DE)', 'E0': 'Premier League (EN)', "I1": 'Serie A (IT)', 'SP1': 'La Liga (ES)'})
###END DRAWS BY LEAGUE AGGREGATE###

###DRAWS BY HOME TEAM AGGREGATE###
draws_by_home_team = main_table.groupby(["HomeTeam"], as_index=False)[['is_draw', "FTHG", 'FTAG']].sum()\
    .rename(columns={'HomeTeam': 'teams', 'is_draw': 'total_draws', 'FTHG': 'goals_scored', 'FTAG': 'goals_conceded'})\
    .sort_values(by='total_draws', ascending=False)
draws_by_home_team['goal_difference'] = draws_by_home_team['goals_scored'] - draws_by_home_team['goals_conceded']
draws_by_home_team['draws_index'] = draws_by_home_team['total_draws'] / draws_by_home_team['total_draws'].max()
draws_by_home_team['goal_difference_index'] = 1-((1/draws_by_home_team['goal_difference'].abs().max())*draws_by_home_team['goal_difference'].abs())
draws_by_home_team['overall_index'] = (draws_by_home_team['draws_index'] + draws_by_home_team['goal_difference_index'])/2
draws_by_home_team['overall_rank'] = draws_by_home_team['overall_index'].rank(method='dense', ascending=False)
###END DRAWS BY HOME TEAM AGGREGATE###

###DRAWS BY AWAY TEAM AGGREGATE###
draws_by_away_team = main_table.groupby("AwayTeam", as_index=False)[['is_draw', "FTHG", 'FTAG']].sum() \
    .rename(columns={'AwayTeam': 'teams', 'is_draw': 'total_draws', 'FTAG': 'goals_scored', 'FTHG': 'goals_conceded'}) \
    .sort_values(by='total_draws', ascending=False)
draws_by_away_team['goal_difference'] = draws_by_away_team['goals_scored'] - draws_by_away_team['goals_conceded']
draws_by_away_team['draws_index'] = draws_by_away_team['total_draws'] / draws_by_away_team['total_draws'].max()
draws_by_away_team['goal_difference_index'] = 1-((1/draws_by_away_team['goal_difference'].abs().max())*draws_by_away_team['goal_difference'].abs())
draws_by_away_team['overall_index'] = (draws_by_away_team['draws_index'] + draws_by_away_team['goal_difference_index'])/2
draws_by_away_team['overall_rank'] = draws_by_away_team['overall_index'].rank(method='dense', ascending=False)
###END DRAWS BY AWAY TEAM AGGREGATE###

###ALL DATA BY TEAM###
total_draws_by_team = draws_by_home_team.merge(draws_by_away_team, on="teams", suffixes=("_home", "_away"))\
     .rename(columns={'total_draws_home': 'home_draws', 'total_draws_away': 'away_draws'})
total_draws_by_team['total_draws'] = total_draws_by_team['home_draws'] + total_draws_by_team['away_draws']
total_draws_by_team['total_goals_scored'] = total_draws_by_team['goals_scored_home'] + total_draws_by_team['goals_scored_away']
total_draws_by_team['total_goals_conceded'] = total_draws_by_team['goals_conceded_home'] + total_draws_by_team['goals_conceded_away']
total_draws_by_team['goal_difference'] = total_draws_by_team['total_goals_scored'] - total_draws_by_team['total_goals_conceded']
total_draws_by_team['draws_index'] = total_draws_by_team['total_draws']  / total_draws_by_team['total_draws'].max()
total_draws_by_team['goal_difference_index'] = 1-((1/total_draws_by_team['goal_difference'].abs().max())*total_draws_by_team['goal_difference'].abs())
total_draws_by_team['overall_index'] = (total_draws_by_team['draws_index'] + total_draws_by_team['goal_difference_index'])/2
total_draws_by_team['overall_rank'] = total_draws_by_team['overall_index'].rank(method='dense', ascending=False).astype('int64')
###END OF ALL DATA BY TEAM###

#_____END OF DATA MANIPULATION_____#
#_____________________________________________________________________________________________________________________


#_____START OF BOX PLOT____#
#______________________________________________________________________________________________________________________


# box_plot = px.box(top_15, y='draws_index')
# #box_plot.update_traces(marker=dict(color="crimson"), selector=dict(type='box'))
# box_plot.show()
data_prep = pd.pivot_table(total_draws_by_team, values=['draws_index', 'goal_difference_index'],
                                 index=['teams'], aggfunc=np.sum).reset_index()
data_prep['draw_inx']=data_prep['draws_index'].astype(float)
data_prep['goal_difference_inx']=data_prep['goal_difference_index'].astype(float)

box_plot_draw_data = pd.pivot_table(data_prep, values=['draw_inx'],
                                 index=['teams'], aggfunc=np.sum).reset_index().sort_values(by='draw_inx', ascending=True)
box_plot_goal_difference_data = pd.pivot_table(data_prep, values=['goal_difference_inx'],
                                 index=['teams'], aggfunc=np.sum).reset_index().sort_values(by='goal_difference_inx', ascending=True)

box_plot = go.Figure()

box_plot.add_trace(go.Box(y=box_plot_draw_data['draw_inx'],
                          name="Draws Index",
                          marker=dict(color="rgb(245,164,37)"),
                          text=box_plot_draw_data['teams'],
                          boxmean='sd'
                          ))
box_plot.add_trace(go.Box(y=box_plot_goal_difference_data['goal_difference_inx'],
                          name='Goal Difference Index',
                          marker=dict(color="lightblue"),
                          text=box_plot_goal_difference_data['teams'],
                          boxmean='sd',
                          ))
box_plot.update_yaxes(matches="y")
box_plot.update_layout( ###BOXPLOT MODE###
                        yaxis_title='Indexes',
                        ###TITLE###
                        title_text='DISTRIBUTION OF TEAMS BY INDEXES',
                        title_font_family='Arial, sans-serif, PT Sans Narrow',
                        title_font_size= 24,
                        title_font_color='rgb(245,164,37)',
                        title_y = 0.95,
                        title_x = 0.40,
                        title_yanchor = 'top',
                        title_xanchor='center',
                        ###LEGEND###
                        legend_title_text ='LEGEND',
                        legend_title_font_family = 'Arial, sans-serif, PT Sans Narrow',
                        legend_title_font_size= 14,
                        legend_title_font_color='rgb(245,164,37)',
                        legend_font_family='Arial, sans-serif, PT Sans Narrow',
                        legend_font_size = 12,
                        legend_font_color = '#fff',
                        legend_bgcolor='rgb(23,34,56)',
                        legend_bordercolor='rgb(245,164,37)',
                        legend_borderwidth= 2,
                        ###MARGIN###
                        margin_r= 10,
                        margin_l= 20,
                        margin_t= 60,
                        margin_b= 40,
                        margin_pad= 2,
                        ###AXES###
                        xaxis = {'showgrid': False},
                        yaxis = {'showgrid': False},
                        ###SIZE###
                        width=800,
                        height= 500,
                        ###FONT###
                        font_family='Arial, sans-serif, PT Sans Narrow',
                        font_size=12,
                        font_color='#fff',
                        ###SEPARATORS###
                        separators = '. ',
                        ###BACKGROUND###
                        paper_bgcolor='rgb(23,34,56)',
                        plot_bgcolor='rgb(23,34,56)',
                        #colorway='#fff',
                        modebar_bgcolor='rgb(23,34,56)',
                        modebar_color='#fff',
                        modebar_activecolor='rgb(245,164,37)',
                        ###HOVERLABEL###
                        hoverlabel_bgcolor='rgb(23,34,56)',
                        hoverlabel_bordercolor='rgb(245,164,37)',
                        hoverlabel_font_family='Arial, sans-serif, PT Sans Narrow',
                        hoverlabel_font_size=12,
                        hoverlabel_font_color='#fff'



)
box_plot.write_html("./graphs_html/Box Plot - Football Team Draw Indexes.html")
#_____END OF BOX PLOT____#

box_plot.show()