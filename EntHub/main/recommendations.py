from django.contrib.auth.models import User

# Recommended books
def recommended_books(user, k):
	if user.bookmark_set.exclude(rating=None):
		matrix = {}
		for u in User.objects.all():
			marks = u.bookmark_set.exclude(rating=None)
			ratings = {}
			for m in marks:
				ratings[m.book] = m.rating
			if ratings:
				matrix[u] = ratings
		return recommendations(user, matrix, k)
	else:
		return []

# Recommended movies
def recommended_movies(user, k):
	if user.moviemark_set.exclude(rating=None):
		matrix = {}
		for u in User.objects.all():
			marks = u.moviemark_set.exclude(rating=None)
			ratings = {}
			for m in marks:
				ratings[m.movie] = m.rating
			if ratings:
				matrix[u] = ratings
		return recommendations(user, matrix, k)
	else:
		return []

# Recommended series
def recommended_series(user, k):
	if user.seriesmark_set.exclude(rating=None):
		matrix = {}
		for u in User.objects.all():
			marks = u.seriesmark_set.exclude(rating=None)
			ratings = {}
			for m in marks:
				ratings[m.series] = m.rating
			if ratings:
				matrix[u] = ratings
		return recommendations(user, matrix, k)
	else:
		return []

# Recommended comics
def recommended_comics(user, k):
	if user.comicmark_set.exclude(rating=None):
		matrix = {}
		for u in User.objects.all():
			marks = u.comicmark_set.exclude(rating=None)
			ratings = {}
			for m in marks:
				ratings[m.comic] = m.rating
			if ratings:
				matrix[u] = ratings
		return recommendations(user, matrix, k)
	else:
		return []

# Recommended comicseries
def recommended_comicseries(user, k):
	if user.comicseriesmark_set.exclude(rating=None):
		matrix = {}
		for u in User.objects.all():
			marks = u.comicseriesmark_set.exclude(rating=None)
			ratings = {}
			for m in marks:
				ratings[m.comic] = m.rating
			if ratings:
				matrix[u] = ratings
		return recommendations(user, matrix, k)
	else:
		return []

# Recommended games
def recommended_games(user, k):
	if user.gamemark_set.exclude(rating=None):
		matrix = {}
		for u in User.objects.all():
			marks = u.gamemark_set.exclude(rating=None)
			ratings = {}
			for m in marks:
				ratings[m.game] = m.rating
			if ratings:
				matrix[u] = ratings
		return recommendations(user, matrix, k)
	else:
		return []

# Returns the k recommendated items by colaborative
# filtering based on user's item ratings
def recommendations(user, matrix, k):
	nn = nearest_neighbours(user, matrix, 5)
	# Get the items rated by neighbours but not by user
	items = set()
	sim_sum = 0.0
	for n in nn:
		sim_sum += n[0]
		neighbour = n[1]
		for item in matrix[neighbour].keys():
			if item not in matrix[user].keys():
				items.add(item)
	# Weighted average
	rec = []
	for i in items:
		n_sum = 0.0
		for n in nn:
			n_sum += (n[0] * matrix[n[1]][i])
		rec.append((n_sum/sim_sum, i))
	# Get the k best average rated items by neighbours
	rec.sort(reverse=True)
	return [r[1] for r in rec[0:k]]

# Returns the k nearest neighbours to user (k-NN)
def nearest_neighbours(user, matrix, k):
	nn = []
	for u, ratings in matrix.items():
		if u != user:
			sim = similarity(matrix[user], ratings)
			if sim > 0:
				nn.append((sim, u))
	nn.sort(reverse=True)
	return nn[0:k]

# Returns similarity between user1 and user2 as a value
# between 0 and 1 by MSD (Minimum Square Difference)
def similarity(ratings1, ratings2):
	sumatory = 0.0
	count = 0
	for item in ratings1.keys():
		if item in ratings2.keys():
			sumatory += ((ratings2[item]-ratings1[item])/4.0)**2
			count += 1
	if count == 0:
		similarity = 0
	else:
		similarity = 1 - (sumatory / count)
	return similarity
