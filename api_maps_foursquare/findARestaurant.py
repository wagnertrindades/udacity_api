from geocode import getGeocodeLocation
import json
import httplib2

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = '4JLP013AN3O5OFCGPGRUTWYBWN0T2XFI42NXPJ4JDCFLZEHO'
foursquare_client_secret = 'V3WOJ4MDZC2ED0XDPDDFNHJ5Z0Y4WVYMQUIBO4JH4KKIMABK'

def findARestaurant(mealType,location):
    coordinates = getGeocodeLocation(location)
    latitude = coordinates[0]
    longitude = coordinates[1]

    url = ('https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20130815&ll=%s,%s&query=%s&limit=1&indent=browse'% (foursquare_client_id, foursquare_client_secret, latitude, longitude, mealType))
    result = access_url_and_return_result(url)

    venue = findAFirstVenue(result)

    restaurant_name = findARestaurantName(venue)
    venue_id = findVenueId(venue)
    photo = findAPhoto(venue_id)
    address = findAAddress(venue)

    print_restaurant_info(restaurant_name, address, photo)

def print_restaurant_info(name, address, photo):
    print 'Restaurant Name: ' + name
    print 'Restaurant Address: ' + address
    print 'Image: ' + photo
    print "==========================================="

def findAFirstVenue(venue):
    first_venue = venue['response']['venues'][0]
    return first_venue

def findARestaurantName(restaurant):
    return restaurant['name']

def findVenueId(venue):
    venue_id = venue['id']
    return venue_id

def findAPhoto(venue_id):
    url = ('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&client_secret=%s&v=20140806&m=foursquare&limit=1'% (venue_id, foursquare_client_id, foursquare_client_secret))
    result = access_url_and_return_result(url)
    photo = interpole_photo_url(result)
    return photo

def interpole_photo_url(photo_result):
    try:
        photo = photo_result['response']['photos']['items'][0]
        photo_size = '300x300'
        photo_url = photo['prefix'] + photo_size + photo['suffix']
    except IndexError:
        photo_url = "Not exists photo in restaurant :("

    return photo_url

def access_url_and_return_result(url):
    h = httplib2.Http()
    decoded_request = h.request(url,'GET')[1].decode('UTF-8')
    response = json.loads(decoded_request)
    return response

def findAAddress(venue):
    formatted_address = venue['location']['formattedAddress']
    address = ''

    for field in formatted_address:
        address += field

    return address


	#1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.

	#2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
	#HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi

	#3. Grab the first restaurant
	#4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
	#5. Grab the first image
	#6. If no image is available, insert default a image url
	#7. Return a dictionary containing the restaurant name, address, and image url

if __name__ == '__main__':
	findARestaurant("Pizza", "Tokyo, Japan")
	findARestaurant("Tacos", "Jakarta, Indonesia")
	findARestaurant("Tapas", "Maputo, Mozambique")
	findARestaurant("Falafel", "Cairo, Egypt")
	findARestaurant("Spaghetti", "New Delhi, India")
	findARestaurant("Cappuccino", "Geneva, Switzerland")
	findARestaurant("Sushi", "Los Angeles, California")
	findARestaurant("Steak", "La Paz, Bolivia")
	findARestaurant("Gyros", "Sydney Australia")
