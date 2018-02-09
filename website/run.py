from flask import Flask, render_template
import random, json, sqlalchemy

app = Flask(__name__)

engine = sqlalchemy.create_engine('mysql+pymysql://root:alex349949@127.0.0.1/game_recommendation?charset=utf8mb4')

#with open('./website/steam_user_id.txt','r') as f:
with open('steam_user_id.txt','r') as f:
	lst_user_id = f.readlines()

lst_popularity_based_recommended_games = []
for app_id in [i[0] for i in engine.execute("SELECT steam_appid FROM tbl_results_popularity_based LIMIT 5").fetchall()]:
	app_data = engine.execute("SELECT steam_appid,name,initial_price,header_image FROM tbl_app_info WHERE steam_appid = {};".format(app_id)).first()
	if app_data != None:
		lst_popularity_based_recommended_games.append(app_data)


@app.route('/')
def recommender():
	userid = random.choice(lst_user_id)
	# userid = 76561197960323774 # no purchase info
	favorite_app_id = engine.execute("SELECT `0` FROM tbl_user_favorite_app WHERE steam_user_id={};".format(userid)).first()[0]

	lst_content_based_recommended_games = []
	lst_item_based_recommended_games = []
	lst_als_recommended_games = []

	if favorite_app_id:
		favorite_app_id = int(favorite_app_id)
		favorite_app_data = engine.execute("SELECT steam_appid,name,initial_price,header_image FROM tbl_app_info WHERE steam_appid = {};".format(favorite_app_id)).first()
		
		for app_id in list(engine.execute("SELECT `0`,`1`,`2`,`3`,`4` FROM tbl_results_content_based WHERE steam_appid = {};".format(favorite_app_id)).first()):
			app_data = engine.execute("SELECT steam_appid,name,initial_price,header_image FROM tbl_app_info WHERE steam_appid = {};".format(app_id)).first()
			if app_data != None:
				lst_content_based_recommended_games.append(app_data)

		for app_id in list(engine.execute("SELECT `0`,`1`,`2`,`3`,`4` FROM tbl_results_item_based WHERE steam_appid = {};".format(favorite_app_id)).first()):
			app_data = engine.execute("SELECT steam_appid,name,initial_price,header_image FROM tbl_app_info WHERE steam_appid = {};".format(app_id)).first()
			if app_data != None:
				lst_item_based_recommended_games.append(app_data)	
		
		for app_id in list(engine.execute("SELECT `0`,`1`,`2`,`3`,`4` FROM tbl_results_als_based WHERE steam_user_id={};".format(userid)).first()):
			app_data = engine.execute("SELECT steam_appid,name,initial_price,header_image FROM tbl_app_info WHERE steam_appid = {};".format(app_id)).first()
			if app_data != None:
				lst_als_recommended_games.append(app_data)

	else:
		favorite_app_data = None


	return render_template( 'recommendation.html',
							userid = userid,
							favorite_app_data = favorite_app_data,
							lst_content_based_recommended_games = lst_content_based_recommended_games,
							lst_item_based_recommended_games = lst_item_based_recommended_games,
							lst_als_recommended_games = lst_als_recommended_games,
							lst_popularity_based_recommended_games = lst_popularity_based_recommended_games)


if __name__ == '__main__':
	app.run(debug=True)



