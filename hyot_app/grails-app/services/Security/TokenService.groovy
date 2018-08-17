package Security

import grails.gorm.transactions.Transactional
import org.jasypt.encryption.pbe.StandardPBEStringEncryptor

/**
 * Service that manages the token.
 */
@Transactional
class TokenService {

    def grailsApplication

    /**
     * It saves the token in database.
     *
     * @param token Token.
     * @return true If token is saved successful in database.
     */
    def save(token) {
        token.save(flush: true, failOnError: true)
    }

    /**
     * It encrypts the email address.
     *
     * @param email User's email address.
     * @return email Email address encrypted of the user.
     */
    def encrypt(String email){

        // It obtains the configuration
        def jasyptConfig    = grailsApplication.config.jasypt

        def stringEncryptor = new StandardPBEStringEncryptor(jasyptConfig)

        return stringEncryptor.encrypt(email)
    }
}