from pymongo.mongo_client import MongoClient
import certifi

# uri = "mongodb+srv://01antizykit:bAkEC1ROZqXYjw29@cluster0.wlwl4hx.mongodb.net/app?retryWrites=true&w=majority&appName=Cluster0"
uri = "mongodb+srv://01antizykit:9qUH8jrZkYUQb7vZ@cluster0.xxtchg2.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
tlsCAFile = certifi.where()
dbClient = MongoClient(uri, tlsCAFile=tlsCAFile)
# Send a ping to confirm a successful connection
try:
    dbClient.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = dbClient['app']
