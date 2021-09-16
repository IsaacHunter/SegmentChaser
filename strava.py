import requests
import json
import math
# print (response.status_code)

allSegs = []
fullSegs = []

olat1 = 43.19032 # Ottawa: 45.3754687
olong1 = -79.20367 # Ottawa: -75.753441
olat2 = 43.26694 # Ottawa: 45.439570
olong2 = -79.05447 # Ottawa: -75.6331927



sep1 = 0.004 #.004 #Niagara: 0.0188
sep2 = 0.009 #0.01  #Niagara: 0.041

tot1 = (olat2-olat1) / sep1
tot2 = (olong2-olong1) / sep2
for x in range(0,int(math.ceil(tot1))):
	for y in range(0,int(math.ceil(tot2))):

		lat1 = olat1 + sep1*x
		long1 = olong1 + sep2*y
		lat2 = olat1 + (sep1*(x+1))
		long2 = olong1 + (sep2*(y+1))

		print ("%f, %f - %f, %f" % (lat1, long1, lat2, long2))
		url = 'https://www.strava.com/api/v3/segments/explore?bounds=%f%%2C%f%%2C%f%%2C%f&activity_type=running' % (lat1, long1, lat2, long2)
		# url = 'https://lincoln.niagaraevergreen.ca/eg/opac/results?query=sort%%28titlesort%%29%%20item_type%%28a%%29;qtype=keyword;locg=103;_adv=1;page=%d;sort=titlesort;detail_record_view=1' % (x)
		r = requests.get(url, headers={'Authorization': 'Bearer a2759badc7a4f69b092fabb9afaef4dfcbb231f6'})
		data = r.json()
		
		print(data)
		for segment in data["segments"]:
			# print(segment["id"])
			dist = segment["distance"]
			url = 'https://www.strava.com/api/v3/segments/%d' % (segment["id"])
			r = requests.get(url, headers={'Authorization': 'Bearer a2759badc7a4f69b092fabb9afaef4dfcbb231f6'})
			data = r.json()
			timestr = data["xoms"]["kom"].split(":")
			if (len(timestr) > 1):
				print("DATA")
				print(timestr)
				time = (int(timestr[0])*60) + int(timestr[1])
				print(time)
				print("----------------")
			else:
				timestr = data["xoms"]["kom"].split("s")
				print("DATA")
				print(timestr)
				time = int(timestr[0])
				print(time)
				print("----------------")

			mytime = 340*math.pow(dist/1600, 1.06)

			print('%.2f %d:%.2f' % (dist/1000, math.floor(1000*time/(dist*60)),(1000*time/dist)%60))
			if (time > mytime):
				if segment["id"] not in allSegs:
					allSegs.append(segment["id"])
					fullSegs.append({
						"id": segment["id"],
						"distance": dist/1000,
						"pace": ('%d:%.2f' % (math.floor(1000*time/(dist*60)),(1000*time/dist)%60)),
						"name": segment["name"],
						"grade": segment["avg_grade"]
						})


print(fullSegs)