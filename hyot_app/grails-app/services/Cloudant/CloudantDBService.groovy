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
}
