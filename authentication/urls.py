from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
     path('match/', views.match_analysis_view, name='match_analysis'),
    path('record/', views.record_view, name='record'),
    path('visualize/', views.visualize_view, name='visualize'),
    path('image/', views.image_view, name='image'),
    path('ballpossession/', views.ballpossession_view, name='ballpossession'),
     path('record_possession/', views.record_possession_data, name='record_possession_data'),
    path('goal/', views.goal_view, name='goal'),
    path('save_goals/', views.save_goals, name='save_goals'),
    path('check_match_number/', views.check_match_number, name='check_match_number'),
    path('penalty/', views.penalty_view, name='penalty'),
    path('save_penalty/', views.save_penalty, name='save_penalty'),
    path('check_match_number1/', views.check_match_number1, name='check_match_number1'),
    path('check_match_number2/', views.check_match_number2, name='check_match_number2'),
    path('api/goals/', views.api_goals, name='api-goals'),
    path('api/possession/', views.api_possession, name='api-possession'),
    path('api/cards/', views.api_cards, name='api-cards'),
    path('api/circle/', views.api_circle, name='api-circle'),
    path('api/penalty/', views.api_penalty, name='api-penalty'),
    path('api/shots/', views.api_shots, name='api-shots'),
    path('matchspecs/', views.matchspecs_view, name='matchspecs'),
    path('api/max_match_number/', views.get_max_match_number, name='max_match_number'),
    path('api/goals/<int:match_number>/', views.get_goal_data, name='get_goal_data'),
    path('api/possession/<int:match_number>/', views.get_possession_data, name='get_possession_data'),
    path('api/card/<int:match_number>/', views.get_card_data, name='get_card_data'),
    path('api/pc/<int:match_number>/', views.get_pc_data, name='get_pc_data'),
    path('api/circle/<int:match_number>/', views.get_circle_data, name='get_circle_data'),
    path('api/shots/<int:match_number>/', views.get_shots_data, name='get_shots_data'),
    path('api/ps/<int:match_number>/', views.get_ps_data, name='get_ps_data'),
    path('standings/', views.standings, name='standings'),
    path('injury/', views.injury_dashboard, name='injury_dashboard'),
    path('delete-injury/<int:pk>/', views.delete_injury, name='delete_injury'),
    path('edit-injury-status/<int:pk>/', views.edit_injury_status, name='edit_injury_status'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('team/<int:team_id>/', views.team_data, name='team_data'),
    path('stats_page/', views.stats_page, name='stats_page'),
    path('api/stats/', views.get_stats, name='get-stats'),     # URL for the API to get stats
    path('game_metrics/', views.game_metrics, name='game_metrics'),
    path('api/fetch_game_data/', views.fetch_game_data, name='fetch-game-data'),
    path('predict/<str:team_name>/', views.predict, name='team_predict'),
    path('predict_result/<str:team_name>/', views.predict_result, name='team_predict_result'),
    path('prediction/', views.prediction, name='prediction'),
    path('logout/', views.logout_view, name='logout'),
    ]
