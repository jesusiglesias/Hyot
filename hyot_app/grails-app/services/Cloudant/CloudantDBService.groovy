package Cloudant

import grails.gorm.transactions.Transactional
import com.cloudant.client.api.ClientBuilder
import com.cloudant.client.api.CloudantClient
import com.cloudant.client.api.Database
import com.cloudant.client.api.model.FindByIndexOptions
import com.cloudant.client.api.query.QueryBuilder
import com.cloudant.client.api.query.QueryResult
import com.cloudant.client.api.query.Sort
import com.cloudant.client.api.views.Key

/**
 * Service to make requests to the Cloudant NoSQL DB.
 */
@Transactional
class CloudantDBService {

    def grailsApplication
    CloudantClient client
    Database db

    /**
     * Initiates the instance of this service and opens the database to use.
     */
    def init() {

        if (client == null && db == null) {

            client = ClientBuilder.account(grailsApplication.config.cloudant.account)
                    .username(grailsApplication.config.cloudant.username)
                    .password(grailsApplication.config.cloudant.password)
                    .build()

            // Get a List of all the databases this Cloudant account
            // List<String> databases = client.getAllDbs()
            // log.debug("All my databases : ")
            // for ( String db : databases ) {
            //    log.debug(db)
            // }

            db = client.database(grailsApplication.config.cloudant.database, false)
        }
    }

    /**
     * Gets all documents
     *
     * @return List<HashMap> with all documents
     */
    def getAllDocs() {

        init()

        String selector="\"selector\": { \"_id\": { \"\$gt\": \"0\" }}"

        List<HashMap> alldocs = db.findByIndex(selector, HashMap.class)

        return alldocs
    }

    /**
     * Gets all documents of a specific user
     *
     * @param username Name of the user
     *
     * @return List<HashMap> with all documents of this user
     */
    def getAllDocsUser(username) {

        init()

        String selector="\"selector\": { \"_id\": { \"\$gt\": \"0\" }, \"owner\": { \"\$eq\": \"" + username + "\" }}"

        List<HashMap> alldocsUser = db.findByIndex(selector, HashMap.class)

        return alldocsUser
    }


    /*

     def measurements = db.findAll()
     System.out.println("medidas " + measurements)
     //def measurementsDHT11 = db.find
     System.out.println(db.listIndexes().allIndexes())
     //System.out.println(db.findByIndex())

     InputStream inputStream = null;
     inputStream = db.find("5460d4d3-0d6e-4bff-a763-102275aa7137")

     System.out.println(inputStream);

     HashMap<String, Object> obj = db.find(HashMap.class, "5460d4d3-0d6e-4bff-a763-102275aa7137");
     System.out.println(obj);
     System.out.println(obj.temperature_field);

     //String selector="\"selector\": {\"_id\": {\"$gt\": 0}}";
     String selector="\"selector\": {\"_id\": {\"\$gt\": 0}}";

     List<HashMap> obj2 = db.findByIndex(selector, HashMap.class,
             new FindByIndexOptions().fields("_id").fields("threshold_value").
                     fields("mailto").fields("sensor_origin").fields("alert_triggered").
                     fields("distance_field").fields("datetime_field").fields("link").
                     fields("owner_alert").fields("event_origin").fields("temperature_field").fields("humidity_field")

     )
     System.out.println(obj2)
     System.out.println(obj2.size())

//Map<String, Object> query = new HashMap<String, Object>();




     /*List<String> list = db.getViewRequestBuilder("ddoc","find-by-product-name")
             .newRequest(Key.Type.STRING, Object.class)
             .limit(10)
             .includeDocs(true)
             .build()
             .getResponse()
             .getKeys();*/

    // It
    //def alertsJson = new JsonSlurper().parseText(alerts)
    //def totalAlerts = alertsJson.size()


}
